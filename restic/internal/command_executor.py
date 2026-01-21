import logging
import subprocess
import time
from collections import deque

import restic.errors

logger = logging.getLogger(__name__)


def execute(cmd, max_stdout_lines: int = 1000, print_interval: float = 1.0):
    """
    Execute a restic command, stream stdout live with throttled logging,
    keep last `max_stdout_lines` in memory for returning or debugging.
    """
    logger.debug("Executing restic command: %s", str(cmd))

    last_stdout_lines = deque(maxlen=max_stdout_lines)
    last_print_time = 0.0
    last_logged_line = None
    last_line = None

    try:
        with subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
        ) as process:

            # Stream stdout live
            for line in process.stdout:
                line = line.rstrip()
                last_stdout_lines.append(line)
                last_line = line

                now = time.time()
                if now - last_print_time >= print_interval:
                    logger.debug(line)
                    last_logged_line = line
                    last_print_time = now

            process.wait()

            logger.debug(
                "Restic command completed with return code %d",
                process.returncode,
            )

            if process.returncode != 0:
                stderr_output = process.stderr.read()
                raise restic.errors.ResticFailedError(
                    f"Restic failed with exit code {process.returncode}:\n"
                    f"STDOUT (last {max_stdout_lines} lines):\n" +
                    "\n".join(last_stdout_lines) +
                    f"\nSTDERR:\n{stderr_output}")

    except FileNotFoundError as e:
        raise restic.errors.NoResticBinaryEror(
            "Cannot find restic installed") from e

    # Ensure the final line is logged exactly once
    if last_line and last_line != last_logged_line:
        logger.debug(last_line)

    return "\n".join(last_stdout_lines)
