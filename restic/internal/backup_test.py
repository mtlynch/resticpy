import unittest
from unittest import mock

import restic
from restic.internal import backup


class BackupTest(unittest.TestCase):

    @mock.patch.object(backup.command_executor, 'execute')
    def test_backup_single_path(self, mock_execute):
        restic.backup(['/tmp/dummy-file.txt'])
        mock_execute.assert_called_with(
            ['restic', 'backup', '/tmp/dummy-file.txt'])

    @mock.patch.object(backup.command_executor, 'execute')
    def test_backup_multiple_paths(self, mock_execute):
        restic.backup(['/tmp/dummy-file-1.txt', '/tmp/dummy-file-2.txt'])
        mock_execute.assert_called_with([
            'restic', 'backup', '/tmp/dummy-file-1.txt', '/tmp/dummy-file-2.txt'
        ])
