from restic.internal import command_executor


def run(restic_base_command):
    cmd = restic_base_command + ['self-update']
    command_executor.execute(cmd)
