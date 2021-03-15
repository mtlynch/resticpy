from restic.internal import command_executor


def run(restic_base_command, paths, exclude_patterns=None, exclude_files=None):
    cmd = restic_base_command + ['backup'] + paths

    if exclude_patterns:
        for exclude_pattern in exclude_patterns:
            cmd.extend(['--exclude', exclude_pattern])

    if exclude_files:
        for exclude_file in exclude_files:
            cmd.extend(['--exclude-file', exclude_file])

    return command_executor.execute(cmd)
