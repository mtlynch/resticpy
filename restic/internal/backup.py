import json

from restic.internal import command_executor


class Error(Exception):
    pass


class UnexpectedResticResult(Error):
    pass


def run(restic_base_command,
        paths,
        exclude_patterns=None,
        exclude_files=None,
        tags=None,
        dry_run=None,
        host=None,
        scan=True):
    cmd = restic_base_command + ['backup'] + paths

    if exclude_patterns:
        for exclude_pattern in exclude_patterns:
            cmd.extend(['--exclude', exclude_pattern])

    if exclude_files:
        for exclude_file in exclude_files:
            cmd.extend(['--exclude-file', exclude_file])

    if tags:
        for tag in tags:
            cmd.extend(['--tag', tag])

    if dry_run:
        cmd.extend(['--dry-run'])

    if host:
        cmd.extend(['--host', host])

    if not scan:
        cmd.extend(['--no-scan'])

    result_raw = command_executor.execute(cmd)
    return _parse_result(result_raw)


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
