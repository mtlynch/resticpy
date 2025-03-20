import asyncio
import logging
import sys
from typing import Any, Callable, Coroutine, List, Optional

import restic.errors

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def _strip_terminal_characters(
        line: bytes | Coroutine[Any, Any, bytes]) -> bytes:
    """
    Removes Windows terminal character '\x1b[2K' from the front of a byte line.
    If no terminal characters are found, the line is returned as is.
    Returns:
        line without leading terminal character.
    """
    if len(line) > 3 and line[:4]==b'\x1b[2K':
        return line[4:]
    return line


async def _monitor_stream(stream: asyncio.StreamReader,
                          lines_agg: Optional[List],
                          on_new_line: Optional[Callable[[str], None]]=None,
                          ) -> None:
    """
    Monitors a stream (e.g. stdout) and waits until full lines are written.
    Windows terminal characters are removed from the beginning of the line.
    The lines are appended to lines_agg (with line-endings) if lines_agg is
    a list. Finally, for each line,  on_new_line is called, if not None.
    """
    async for byte_line in stream:
        byte_line = _strip_terminal_characters(byte_line)
        line = byte_line.decode('utf-8')
        if lines_agg is not None:
            lines_agg.append(line)
        if on_new_line:
            on_new_line(line.rstrip('\n'))

async def execute_async(cmd,
                        on_stdout : Optional[Callable[[str], None]]=None,
                        on_stderr : Optional[Callable[[str], None]]=None,
                        ) -> List[str]:
    """
    Asynchronous execution of cmd with command line arguments.

    Arguments:
        on_stdout : If not None, is called for each line that the command
                    outputs to stdout.
        on_stderr: If not None, is called for each line that the command
                    outputs to stderr.

    Returns:
        string with aggregated output to stdout
    """

    logger.debug('Executing restic command: %s', str(cmd))
    try:
        process = await asyncio.create_subprocess_exec(
            cmd[0],
            *cmd[1:],
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
    except FileNotFoundError as e:
        raise restic.errors.NoResticBinaryError(
            'Cannot find restic installed') from e

    logger.debug('Process started. Now monitoring output.')
    stdout_output = []
    stderr_output = []

    stdout_monitor = asyncio.create_task(_monitor_stream(process.stdout,
                                                       stdout_output,
                                                       on_stdout))
    stderr_monitor = asyncio.create_task(_monitor_stream(process.stderr,
                                                       stderr_output,
                                                       on_stderr))

    while process.returncode is None:
        await asyncio.sleep(0.1)

    await asyncio.gather(stdout_monitor, stderr_monitor)

    logger.debug('Restic command completed with return code %i',
                 process.returncode)

    if process.returncode != 0:
        raise restic.errors.ResticFailedError(
            f'Restic failed with exit code {process.returncode}: \n'
            + ''.join(stderr_output))
    return stdout_output


def execute(cmd,
            on_stdout : Optional[Callable[[str], None]]=None,
            on_stderr : Optional[Callable[[str], None]]=None):
    std_output_list = asyncio.run(execute_async(cmd,
                                                on_stdout=on_stdout,
                                                on_stderr=on_stderr))
    return ''.join(std_output_list)
