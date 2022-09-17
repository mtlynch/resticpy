import unittest
from unittest import mock

import restic
from restic.internal import init


class InitTest(unittest.TestCase):

    @mock.patch.object(init.command_executor, 'execute')
    def test_init_with_no_parameters(self, mock_execute):
        mock_execute.return_value = (
            'created restic repository 054ed643d8 at /media/backup1')

        repository_id = restic.init()

        self.assertEqual('054ed643d8', repository_id)
        mock_execute.assert_called_with(['restic', '--json', 'init'])

    @mock.patch.object(init.command_executor, 'execute')
    def test_init_with_secondary_repository(self, mock_execute):
        mock_execute.return_value = (
            'created restic repository 054ed643d8 at /media/backup1')

        repository_id = restic.init(
            copy_chunker_params=True,
            repo2='s3:https://some.backend.com/mybucket')

        self.assertEqual('054ed643d8', repository_id)
        mock_execute.assert_called_with([
            'restic', '--json', 'init', '--copy-chunker-params', '--repo2',
            's3:https://some.backend.com/mybucket'
        ])
