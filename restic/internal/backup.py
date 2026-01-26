import json

from restic.internal import command_executor


class Error(Exception):
    pass


class UnexpectedResticResult(Error):
    pass


def run(restic_base_command,
        paths=None,
        files_from=None,
        exclude_patterns=None,
        exclude_files=None,
        tags=None,
        dry_run=None,
        host=None,
        scan=True,
        group_by=None,
        skip_if_unchanged=False,
        timeout=None,
        progress_callback=None):
    cmd = restic_base_command + ['backup']

    if paths is None and files_from is None:
        raise ValueError('No input given as argument. '
                         'Please specify `paths` or `files_from`')

    if paths:
        cmd += paths

    _extend_cmd_with_list(cmd, '--files-from', files_from)
    _extend_cmd_with_list(cmd, '--exclude', exclude_patterns)
    _extend_cmd_with_list(cmd, '--exclude-file', exclude_files)
    _extend_cmd_with_list(cmd, '--tag', tags)

    if dry_run:
        cmd.extend(['--dry-run'])

    if host:
        cmd.extend(['--host', host])

    if not scan:
        cmd.extend(['--no-scan'])

    # Explicitly check for None, as empty lists and None have different
    # meanings.
    if group_by is not None:
        cmd.extend(['--group-by', ','.join(group_by)])

    if skip_if_unchanged:
        cmd.extend(['--skip-if-unchanged'])

    if progress_callback is not None:
        return command_executor.execute(cmd,
                                        stream=True,
                                        on_line=progress_callback,
                                        timeout=timeout)

    result_raw = command_executor.execute(cmd, timeout=timeout)
    return _parse_result(result_raw)


def _extend_cmd_with_list(cmd, cli_option, arg_list):
    if arg_list is None:
        return
    for item in arg_list:
        cmd.extend([cli_option, item])


def _parse_result(result):
    # On Windows, terminal markers appear at the beginning of each line.
    terminal_markers = '\x1b[2K'
    lines = [
        line.strip().strip(terminal_markers)
        for line in result.split('\n')
        if line.strip()
    ]

    try:
        return json.loads(lines[-1])
    except json.decoder.JSONDecodeError as e:
        raise UnexpectedResticResult(
            'Expected valid JSON response from restic, got ' + result) from e
