import json

from restic.internal import command_executor


class Key:

    def __init__(self, restic_base_command):
        self.base_command = restic_base_command

    def list(self):
        cmd = self.base_command() + ['key', 'list']

        result = command_executor.execute(cmd)
        return json.loads(result)

    def add(self, host=None, new_password_file=None, user=None):
        cmd = self.base_command() + ['key', 'add']

        if host:
            cmd.extend(['--host', host])

        if new_password_file:
            cmd.extend(['--new-password-file', new_password_file])

        if user:
            cmd.extend(['--user', user])

        return command_executor.execute(cmd)

    def remove(self, key_id):
        cmd = self.base_command() + ['key', 'remove', key_id]

        return command_executor.execute(cmd)

    def passwd(self, new_password_file=None):
        cmd = self.base_command() + ['key', 'passwd']

        if new_password_file:
            cmd.extend(['--new-password-file', new_password_file])

        return command_executor.execute(cmd)
