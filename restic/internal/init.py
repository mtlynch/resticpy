import re

from restic.internal import command_executor


def run(restic_base_command):
    cmd = restic_base_command + ['init']

    return _parse_result(command_executor.execute(cmd))


def _parse_result(result):
    return re.match(r'created restic repository ([a-z0-9]+) at .+',
                    result).group(1)
