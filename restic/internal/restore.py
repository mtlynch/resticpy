from restic.internal import command_executor


def run(restic_base_command,
        snapshot_id='latest',
        include=None,
        target_dir=None):
    cmd = restic_base_command + ['restore', snapshot_id]

    if include:
        cmd.extend(['--include', include])

    if target_dir:
        cmd.extend(['--target', target_dir])

    return command_executor.execute(cmd)
