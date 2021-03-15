import re

from restic.internal import command_executor


def run(restic_base_command):
    cmd = restic_base_command + ['version']
    out = command_executor.execute(cmd)
    match = re.match((r'restic ([0-9\.]+) compiled with go([0-9\.]+) '
                      'on ([a-zA-Z0-9]+)/([a-zA-Z0-9]+)'), out)
    return {
        'restic_version': match.group(1),
        'go_version': match.group(2),
        'platform_version': match.group(3),
        'architecture': match.group(4)
    }
