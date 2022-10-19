import json

from restic.internal import command_executor


def run(restic_base_command, pattern):
    cmd = restic_base_command + ['find', pattern]

    return json.loads(command_executor.execute(cmd))
