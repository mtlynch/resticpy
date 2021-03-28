import json

from restic.internal import command_executor


def run(restic_base_command, group_by=None):
    cmd = restic_base_command + ['snapshots']

    if group_by:
        cmd.extend(['--group-by', group_by])

    return json.loads(command_executor.execute(cmd))
