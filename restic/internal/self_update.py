from restic.internal import command_executor


def run(restic_base_command):
    cmd = restic_base_command + ['self-update']
    return command_executor.execute(cmd)
