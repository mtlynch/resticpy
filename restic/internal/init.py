import re

from restic.internal import command_executor


def run(restic_base_command,
        copy_chunker_params=False,
        from_repo=None,
        from_password_file=None,
        repo2=None):  # FIXME: remove repo2 in next major version
    cmd = restic_base_command + ['init']

    if copy_chunker_params:
        cmd.append('--copy-chunker-params')

    if repo2:  # FIXME: remove in next major version
        print('Arg repo2 has been deprecated, use from-repo instead')
        cmd.extend(['--repo2', repo2])

    if from_repo:
        cmd.extend(['--from-repo', from_repo])

    if from_password_file:
        cmd.extend(['--from-password-file', from_password_file])

    return _parse_result(command_executor.execute(cmd))


def _parse_result(result):
    return re.match(r'created restic repository ([a-z0-9]+) at .+',
                    result).group(1)
