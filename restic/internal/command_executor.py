import logging
import subprocess

logger = logging.getLogger(__name__)


def execute(cmd):
    logger.debug('Executing restic command: %s', str(cmd))
    try:
        process = subprocess.run(cmd,
                                 capture_output=True,
                                 text=True,
                                 encoding='utf-8')
    except FileNotFoundError as e:
        raise RuntimeError('Cannot find restic installed') from e

    logger.debug('Restic command completed with return code %d',
                 process.returncode)

    if process.returncode != 0:
        raise RuntimeError('Restic failed with exit code %s: %s' %
                           (process.returncode, process.stderr))

    return process.stdout
