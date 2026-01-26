import logging
import selectors
import subprocess
import time
from collections import deque
from dataclasses import dataclass
from typing import Callable
from typing import Deque

import restic.errors

logger = logging.getLogger(__name__)


@dataclass
class StreamState:
    """
    Holds the state for streaming and buffering of subprocess output.
    """
    stream: bool
    on_line: Callable[[str], None] | None
    stdout_buffer: Deque[str]
    stderr_buffer: Deque[str]


def get_stdout_result(stdout_buffer: Deque[str], stream: bool) -> str:
    """
    Return the appropriate stdout result.

    - In streaming mode, return only the last non-empty line
      (expected to be the final JSON summary from restic).
    - In non-streaming mode, return full stdout.
    """
    if not stdout_buffer:
        return ""

    if stream:
        # Return last meaningful line
        for line in reversed(stdout_buffer):
            if line.strip():
                return line
        return ""

    return "\n".join(stdout_buffer)


def handle_line(source: str, line: str, state: StreamState) -> None:
    """
    Process a single line of output from stdout or stderr.

    - Forwards the line to the callback if streaming is enabled.
    - Catches and logs any exceptions from the callback.
    - Stores the line in the appropriate bounded buffer.
    """
    if state.stream and state.on_line:
        try:
            state.on_line(line)
        except Exception as e:  # pylint: disable=W0703
            # Keep loop running if callback fails
            logger.exception("Exception in on_line callback (ignored): %s", e)

    if source == "stdout":
        state.stdout_buffer.append(line)
    else:
        state.stderr_buffer.append(line)


def safe_drain(pipe, source: str, state: StreamState) -> None:
    """
    Drain remaining lines from a pipe without failing
    if it is already closed.
    """
    try:
        if pipe and not pipe.closed:
            for line in pipe:
                handle_line(source, line.rstrip(), state)
    except ValueError:
        # Pipe already closed – safe to ignore
        pass


def execute(
    cmd,
    *,
    stream: bool = False,
    on_line: Callable[[str], None] | None = None,
    timeout: float | None = None,
    buffer_limit: int = 1000,
) -> str:
    """
    Execute a restic command and return its stdout output.

    Uses subprocess.Popen to run the command and selectors to consume
    stdout and stderr concurrently without blocking.

    - Supports optional real-time streaming via `on_line`.
    - Bounded buffers prevent unbounded memory growth.
    - Exceptions in the callback are logged but do not interrupt execution.
    - Optional timeout terminates the process if exceeded.
    - Stdout is always returned as a single string for backward compatibility.

    Args:
        cmd (list[str]): Full restic command to execute.
        stream (bool): Enable real-time streaming of output lines.
        on_line (Callable[[str], None] | None): Optional line callback.
        timeout (float | None): Maximum execution time in seconds.
        buffer_limit (int): Maximum number of lines kept in memory.

    Returns:
        str: Collected stdout output.

    Raises:
        NoResticBinaryError: If restic binary is not found.
        ResticFailedError: If restic exits with a non-zero exit code.
        TimeoutError: If execution exceeds the specified timeout.
    """
    logger.debug("Executing restic command: %s", cmd)

    if timeout is not None and timeout < 0:
        raise ValueError(f"timeout must be non-negative, got {timeout}")

    try:
        # Start the process using a context manager for automatic cleanup.
        with subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                encoding="utf-8",
        ) as process:

            # Use selectors to read stdout and stderr concurrently.
            selector = selectors.DefaultSelector()
            if process.stdout:
                selector.register(process.stdout, selectors.EVENT_READ,
                                  "stdout")
            if process.stderr:
                selector.register(process.stderr, selectors.EVENT_READ,
                                  "stderr")

            # Initialize bounded buffers to prevent unbounded memory usage.
            stdout_buffer = deque(maxlen=buffer_limit)
            stderr_buffer = deque(maxlen=buffer_limit)

            # Create a StreamState object to pass to handle_line.
            state = StreamState(
                stream=stream,
                on_line=on_line,
                stdout_buffer=stdout_buffer,
                stderr_buffer=stderr_buffer,
            )

            start_time = time.monotonic()

            # Main loop: read available lines from stdout/stderr.
            try:
                while selector.get_map():
                    # Enforce timeout if requested.
                    if timeout is not None and time.monotonic(
                    ) - start_time > timeout:
                        process.kill()
                        raise TimeoutError(
                            f"Restic command timed out after {timeout} seconds")

                    # Wait briefly for any stream to be ready.
                    for key, _ in selector.select(timeout=0.1):
                        stream_obj = key.fileobj
                        source = key.data

                        line = stream_obj.readline()
                        if not line:
                            # EOF reached for this stream, unregister and close.
                            selector.unregister(stream_obj)
                            continue

                        # Process the line using the shared state object.
                        handle_line(source, line.rstrip(), state)

                    # Exit once process is done and no streams are registered
                    if process.poll() is not None and not selector.get_map():
                        break

            finally:
                selector.close()

            returncode = process.wait()

            # Final drain to catch last buffered lines (e.g. restic summary)
            safe_drain(process.stdout, "stdout", state)
            safe_drain(process.stderr, "stderr", state)

    except FileNotFoundError as e:
        raise restic.errors.NoResticBinaryError(
            "Cannot find restic installed") from e

    logger.debug("Restic command completed with return code %d", returncode)

    if returncode != 0:
        stderr_text = "\n".join(stderr_buffer)
        raise restic.errors.ResticFailedError(
            f"Restic failed with exit code {returncode}: {stderr_text}")

    result = get_stdout_result(stdout_buffer, stream)
    return result
