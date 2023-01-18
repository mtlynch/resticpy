import unittest
from unittest import mock

import restic
from restic.internal import init


class InitTest(unittest.TestCase):

    @mock.patch.object(init.command_executor, 'execute')
    def test_init_with_no_parameters(self, mock_execute):
        mock_execute.return_value = """
{"message_type":"initialized","id":"d0c84a66bffea61b4cbb88c39cea742127699b3f3af71127b68edcc142edff48","repository":"/tmp/tmp.lNaHYLGR7F"}
""".strip()

        repository_id = restic.init()

        self.assertEqual(
            'd0c84a66bffea61b4cbb88c39cea742127699b3f3af71127b68edcc142edff48',
            repository_id)
        mock_execute.assert_called_with(['restic', '--json', 'init'])

    # Prior to restic 0.15.0, restic responded with plaintext instead of JSON.
    @mock.patch.object(init.command_executor, 'execute')
    def test_init_legacy_format(self, mock_execute):
        mock_execute.return_value = (
            'created restic repository 054ed643d8 at /media/backup1')

        repository_id = restic.init()

        self.assertEqual('054ed643d8', repository_id)
        mock_execute.assert_called_with(['restic', '--json', 'init'])

    @mock.patch.object(init.command_executor, 'execute')
    def test_init_with_secondary_repository(self, mock_execute):
        mock_execute.return_value = """
{"message_type":"initialized","id":"d0c84a66bffea61b4cbb88c39cea742127699b3f3af71127b68edcc142edff48","repository":"/tmp/tmp.lNaHYLGR7F"}
""".strip()

        repository_id = restic.init(
            copy_chunker_params=True,
            from_repo='s3:https://some.backend.com/mybucket')

        self.assertEqual(
            'd0c84a66bffea61b4cbb88c39cea742127699b3f3af71127b68edcc142edff48',
            repository_id)
        mock_execute.assert_called_with([
            'restic', '--json', 'init', '--copy-chunker-params', '--from-repo',
            's3:https://some.backend.com/mybucket'
        ])
