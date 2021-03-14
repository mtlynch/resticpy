from restic.internal import command_executor


def run(restic_base_command, paths, exclude_patterns=[]):
    cmd = restic_base_command + ['backup'] + paths

    if exclude_patterns:
        for exclude_pattern in exclude_patterns:
            cmd.extend(['--exclude', exclude_pattern])

    return command_executor.execute(cmd)
