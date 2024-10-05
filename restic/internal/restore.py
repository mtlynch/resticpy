from restic.internal import command_executor


class Error(Exception):
    pass


class LegacySemanticsError(Error):
    pass


def run(restic_base_command,
        snapshot_id='latest',
        include=None,
        exclude=None,
        target_dir=None):
    cmd = restic_base_command + ['restore', snapshot_id]

    if include:
        cmd.extend(['--include', include])

    if exclude:
        if isinstance(exclude, str):
            raise LegacySemanticsError(
                'As of resticpy 1.2.0, the `exclude` parameter must be a list '
                'not a string')
        for exclude_path in exclude:
            cmd.extend(['--exclude', exclude_path])

    if target_dir:
        cmd.extend(['--target', target_dir])

    return command_executor.execute(cmd)
