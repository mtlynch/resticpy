from restic.internal import command_executor


def run(restic_base_command, repo2=None, password_file2=None):
    cmd = restic_base_command + ['copy']

    if repo2:
        cmd.extend(['--repo2', repo2])

    if password_file2:
        cmd.extend(['--password-file2', password_file2])

    return command_executor.execute(cmd)
