from restic.internal import command_executor


def run(restic_base_command, read_data=False):
    cmd = restic_base_command + ['check']

    if read_data:
        cmd.append('--read-data')

    return command_executor.execute(cmd)
