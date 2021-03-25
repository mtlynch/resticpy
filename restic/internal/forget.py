import json

from restic.internal import command_executor
from restic.internal import errors


def run(restic_base_command,
        prune=False,
        keep_daily=None,
        keep_within=None,
        group_by=None):
    cmd = restic_base_command + ['forget']

    if prune:
        cmd.extend(['--prune'])

    if keep_daily is not None:
        cmd.extend(['--keep-daily', str(keep_daily)])

    if keep_within is not None:
        cmd.extend(['--keep-within', keep_within])

    if group_by is not None:
        cmd.extend(['--group-by', group_by])

    return _parse_result(command_executor.execute(cmd))


def _parse_result(result):
    # The result is JSON followed by 0 or more non-JSON lines.
    result_lines = result.split('\n')
    try:
        return json.loads(result_lines[0])
    except json.decoder.JSONDecodeError as e:
        raise errors.UnexpectedResticResponse(
            'Unexpected result from restic. Expected JSON, got: %s' %
            result_lines[0]) from e
