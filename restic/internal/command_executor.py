import logging
import subprocess

import restic.errors

logger = logging.getLogger(__name__)


def execute(cmd):
    logger.debug('Executing restic command: %s', str(cmd))
    try:
        process = subprocess.run(cmd,
                                 capture_output=True,
                                 text=True,
                                 check=False,
                                 encoding='utf-8')
    except FileNotFoundError as e:
        raise restic.errors.NoResticBinaryEror(
            'Cannot find restic installed') from e

    logger.debug('Restic command completed with return code %d',
                 process.returncode)

    if process.returncode != 0:
        raise restic.errors.ResticFailedError(
            f'Restic failed with exit code {process.returncode}: ' +
            process.stderr)

    return process.stdout
