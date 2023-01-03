from restic.internal import command_executor


def run(restic_base_command,
        repo2=None,
        password_file2=None,
        from_repo=None,
        from_password_file=None
       ):  # FIXME: remove repo2, password_file2 in next major version

    cmd = restic_base_command + ['copy']

    if repo2:  # FIXME: remove in next major version
        print('Arg repo2 has been deprecated, use from-repo instead')
        cmd.extend(['--repo2', repo2])

    if password_file2:  # FIXME: remove in next major version
        print(
            'Arg password_file2 has been deprecated, use from-password-file instead'  # pylint: disable=C0301
        )
        cmd.extend(['--password-file2', password_file2])

    if from_repo:
        cmd.extend(['--from-repo', from_repo])

    if from_password_file:
        cmd.extend(['--from-password-file', from_password_file])

    return command_executor.execute(cmd)
