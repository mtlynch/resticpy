import json

from restic.internal import command_executor


def run(restic_base_command, mode=None, tags=None, host=None):
    cmd = restic_base_command + ['stats']

    if mode:
        cmd.extend(['--mode', mode])

    if tags:
        for tag in tags:
            cmd.extend(['--tag', tag])

    if host:
        cmd.extend(['--host', host])

    return json.loads(command_executor.execute(cmd))
