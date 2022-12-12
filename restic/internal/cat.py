import json

from restic.internal import command_executor


class Cat:

    def __init__(self, restic_base_command):
        self.base_command = restic_base_command

    def _run(self, subcommand, id_=None, json_encode=True, binary_mode=False):
        cmd = self.base_command() + ['cat', subcommand]

        if id_:
            cmd.extend([id_])

        result = command_executor.execute(cmd, binary_mode=binary_mode)

        if json_encode:
            result = json.loads(result)
        return result

    def pack(self, id_):
        return self._run('pack', id_, json_encode=False, binary_mode=True)

    def blob(self, id_):
        return self._run('blob', id_)

    def snapshot(self, id_):
        return self._run('snapshot', id_)

    def index(self, id_):
        return self._run('index', id_)

    def key(self, id_):
        return self._run('key', id_)

    def masterkey(self):
        return self._run('masterkey')

    def config(self):
        return self._run('config')

    def lock(self, id_):
        return self._run('lock', id_)
