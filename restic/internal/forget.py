import json

import restic.errors
from restic.internal import command_executor


def run(restic_base_command,
        dry_run=None,
        group_by=None,
        tags=None,
        host=None,
        keep_last=None,
        keep_hourly=None,
        keep_daily=None,
        keep_weekly=None,
        keep_monthly=None,
        keep_yearly=None,
        keep_within=None,
        prune=False):
    cmd = restic_base_command + ['forget']

    if dry_run:
        cmd.extend(['--dry-run'])

    if group_by:
        cmd.extend(['--group-by', group_by])

    if tags:
        for tag in tags:
            cmd.extend(['--tag', tag])

    if host:
        cmd.extend(['--host', host])

    if keep_last:
        cmd.extend(['--keep-last', str(keep_last)])

    if keep_hourly:
        cmd.extend(['--keep-hourly', str(keep_hourly)])

    if keep_daily:
        cmd.extend(['--keep-daily', str(keep_daily)])

    if keep_weekly:
        cmd.extend(['--keep-weekly', str(keep_weekly)])

    if keep_monthly:
        cmd.extend(['--keep-monthly', str(keep_monthly)])

    if keep_yearly:
        cmd.extend(['--keep-yearly', str(keep_yearly)])

    if keep_within:
        cmd.extend(['--keep-within', str(keep_within)])

    if prune:
        cmd.extend(['--prune'])

    return _parse_result(command_executor.execute(cmd))


def _parse_result(result):
    # The result is JSON followed by 0 or more non-JSON lines.
    result_lines = result.split('\n')
    try:
        # forget result can be empty
        if result_lines[0]:
            return json.loads(result_lines[0])
        return {}
    except json.decoder.JSONDecodeError as e:
        raise restic.errors.UnexpectedResticResponse(
            'Unexpected result from restic. Expected JSON, got: ' +
            result_lines[0]) from e
