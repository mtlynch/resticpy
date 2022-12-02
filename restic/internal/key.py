import json

from restic.internal import command_executor


def run(restic_base_command,
        subcommand,
        host=None,
        new_password_file=None,
        user=None,
        key_id=None):
    cmd = restic_base_command + ['key', subcommand]

    if host:
        cmd.extend(['--host', host])

    if new_password_file:
        cmd.extend(['--new-password-file', new_password_file])

    if user:
        cmd.extend(['--user', user])

    if key_id:
        cmd.extend([key_id])

    result = command_executor.execute(cmd)
    if subcommand == 'list':
        return json.loads(result)
    return result
