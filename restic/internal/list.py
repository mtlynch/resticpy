from restic.internal import command_executor


class List:

    def __init__(self, restic_base_command):
        self.base_command = restic_base_command

    def blobs(self):
        cmd = self.base_command() + ['list', 'blobs']

        result = self.run(cmd)
        parsed_result = [
            dict(zip(('type', 'id'), l.split(' '))) for l in result
        ]

        return parsed_result

    def packs(self):
        cmd = self.base_command() + ['list', 'packs']
        return self.run(cmd)

    def index(self):
        cmd = self.base_command() + ['list', 'index']
        return self.run(cmd)

    def snapshots(self):
        cmd = self.base_command() + ['list', 'snapshots']
        return self.run(cmd)

    def keys(self):
        cmd = self.base_command() + ['list', 'keys']
        return self.run(cmd)

    def locks(self):
        cmd = self.base_command() + ['list', 'locks']
        return self.run(cmd)

    def run(self, cmd):
        result = command_executor.execute(cmd)

        return result.splitlines()
