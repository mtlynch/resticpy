import re

from restic.internal import command_executor


def run(restic_base_command, copy_chunker_params=False, repo2=None):
    cmd = restic_base_command + ['init']

    if copy_chunker_params:
        cmd.append('--copy-chunker-params')

    if repo2:
        cmd.extend(['--repo2', repo2])

    return _parse_result(command_executor.execute(cmd))


def _parse_result(result):
    return re.match(r'created restic repository ([a-z0-9]+) at .+',
                    result).group(1)
