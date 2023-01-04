from restic.internal import command_executor


def run(restic_base_command, from_repo=None, from_password_file=None):

    cmd = restic_base_command + ['copy']

    if from_repo:
        cmd.extend(['--from-repo', from_repo])

    if from_password_file:
        cmd.extend(['--from-password-file', from_password_file])

    return command_executor.execute(cmd)
