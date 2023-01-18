import json
import re

from restic.internal import command_executor


def run(restic_base_command,
        copy_chunker_params=False,
        from_repo=None,
        from_password_file=None):
    cmd = restic_base_command + ['init']

    if copy_chunker_params:
        cmd.append('--copy-chunker-params')

    if from_repo:
        cmd.extend(['--from-repo', from_repo])

    if from_password_file:
        cmd.extend(['--from-password-file', from_password_file])

    return _parse_result(command_executor.execute(cmd))


def _parse_result(result):
    try:
        return json.loads(result)['id']
    except json.decoder.JSONDecodeError:
        return _parse_plaintext_result(result)


def _parse_plaintext_result(result):
    """Parse legacy plaintext result.

    Prior to restic 0.15.0, restic returned a plaintext response even when the
    caller specified --json.
    """
    return re.match(r'created restic repository ([a-z0-9]+) at .+',
                    result).group(1)
