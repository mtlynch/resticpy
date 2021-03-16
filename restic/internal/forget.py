import json

from restic.internal import command_executor


def run(restic_base_command, prune=False, keep_daily=None):
    cmd = restic_base_command + ['forget']

    if prune:
        cmd.extend(['--prune'])

    if keep_daily is not None:
        cmd.extend(['--keep-daily', str(keep_daily)])

    return json.loads(command_executor.execute(cmd))
