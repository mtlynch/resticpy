from restic.config import restic_bin
from restic.internal import command_executor


def run():
    cmd = [restic_bin, 'self-update']
    command_executor.execute(cmd)
