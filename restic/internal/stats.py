import json

from restic.internal import command_executor


def run(restic_base_command):
    cmd = restic_base_command + ['stats']
    return json.loads(command_executor.execute(cmd))
