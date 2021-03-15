import logging
import subprocess

logger = logging.getLogger(__name__)


def execute(cmd):
    logger.debug('Executing restic command: %s', str(cmd))
    out = ''
    err = ''
    try:
        with subprocess.Popen(cmd,
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              encoding='utf-8',
                              text=True) as proc:
            out, err = proc.communicate()
            if err is not None:
                raise RuntimeError('Command runtime failure')
            proc.wait()
            if proc.returncode != 0:
                raise RuntimeError(f'Return code {proc.returncode} is not zero')
    except FileNotFoundError as e:
        raise RuntimeError('Cannot find restic installed') from e

    return out
