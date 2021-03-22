import json

from restic.internal import command_executor


def run(restic_base_command, mode=None):
    cmd = restic_base_command + ['stats']

    if mode:
        cmd.extend(['--mode', mode])

    return json.loads(command_executor.execute(cmd))
