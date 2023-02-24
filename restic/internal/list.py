from restic.internal import command_executor


class List:

    def __init__(self, restic_base_command):
        self.base_command = restic_base_command

    def locks(self):
        cmd = self.base_command() + ['list', 'locks']
        return self.run(cmd)

    def run(self, cmd):
        result = command_executor.execute(cmd)

        return result.splitlines()
