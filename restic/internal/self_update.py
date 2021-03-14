from restic.internal import command_executor


def run(restic_binary_path):
    cmd = [restic_binary_path, 'self-update']
    command_executor.execute(cmd)
