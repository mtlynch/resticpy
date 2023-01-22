from restic.internal import command_executor


def run(restic_base_command,
        exclude=None,
        exclude_file=None,
        forget=False,
        dry_run=False,
        snapshot_id=None):
    cmd = restic_base_command + ['rewrite']

    if exclude:
        for exclude_path in exclude:
            cmd.extend(['--exclude', exclude_path])

    if exclude_file:
        cmd.extend(['--exclude-file', exclude_file])

    if forget:
        cmd.append('--forget')

    if dry_run:
        cmd.append('--dry-run')

    if snapshot_id:
        cmd.append(snapshot_id)

    return command_executor.execute(cmd)
