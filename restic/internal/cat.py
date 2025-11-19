import json

from restic.internal import command_executor


class Cat:

    def __init__(self, restic_base_command):
        self.base_command = restic_base_command

    def masterkey(self):
        cmd = self.base_command() + ['cat', 'masterkey']
        return self.run(cmd)

    def config(self):
        cmd = self.base_command() + ['cat', 'config']
        return self.run(cmd)

    def lock(self, lock_id):
        cmd = self.base_command() + ['cat', 'lock', lock_id, '--no-lock']  # pylint: disable=C0301
        return self.run(cmd)

    def run(self, cmd):
        return json.loads(command_executor.execute(cmd))
