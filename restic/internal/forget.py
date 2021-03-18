import json

from restic.internal import command_executor
from restic.internal import errors


def run(restic_base_command, prune=False, keep_daily=None):
    cmd = restic_base_command + ['forget']

    if prune:
        cmd.extend(['--prune'])

    if keep_daily is not None:
        cmd.extend(['--keep-daily', str(keep_daily)])

    result = command_executor.execute(cmd)
    try:
        return json.loads(result)
    except json.decoder.JSONDecodeError as e:
        raise errors.UnexpectedResticResponse(
            'Unexpected result from restic. Expected JSON, got: %s' %
            result) from e
