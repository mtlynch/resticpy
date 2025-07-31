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
        snapshot_id=None,
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

    _add_keep_option(cmd, '--keep-last', keep_last)
    _add_keep_option(cmd, '--keep-hourly', keep_hourly)
    _add_keep_option(cmd, '--keep-daily', keep_daily)
    _add_keep_option(cmd, '--keep-weekly', keep_weekly)
    _add_keep_option(cmd, '--keep-monthly', keep_monthly)
    _add_keep_option(cmd, '--keep-yearly', keep_yearly)
    _add_keep_option(cmd, '--keep-within', keep_within)

    if prune:
        cmd.extend(['--prune'])

    if snapshot_id:
        # The -- tells restic to treat the subsequent param
        # as a literal string even if it begins with "-".
        cmd.extend(['--', snapshot_id])

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


def _add_keep_option(cmd, option, value):
    if value:
        cmd.extend([option, str(value)])
