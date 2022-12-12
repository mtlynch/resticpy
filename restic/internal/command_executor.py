import logging
import subprocess

import restic.errors

logger = logging.getLogger(__name__)


def execute(cmd, binary_mode=False):
    logger.debug('Executing restic command: %s', str(cmd))
    try:
        subprocess_args = {
            'capture_output': True,
            'check': False,
            'text': True,
            'encoding': 'utf-8'
        }
        if binary_mode:
            subprocess_args.pop('text')
            subprocess_args.pop('encoding')

        process = subprocess.run(cmd, **subprocess_args)
    except FileNotFoundError as e:
        raise restic.errors.NoResticBinaryEror(
            'Cannot find restic installed') from e

    logger.debug('Restic command completed with return code %d',
                 process.returncode)

    if process.returncode != 0:
        raise restic.errors.ResticFailedError(
            f'Restic failed with exit code {process.returncode}: ' +
            str(process.stderr))

    return process.stdout
