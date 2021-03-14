from restic.internal import command_executor


def run(restic_base_command, paths):
    cmd = restic_base_command + ['backup'] + paths

    return command_executor.execute(cmd)
