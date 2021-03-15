import unittest
from unittest import mock

import restic
from restic.internal import backup

# Ignore suggestions to turn methods into functions.
# pylint: disable=R0201


class BackupTest(unittest.TestCase):

    @mock.patch.object(backup.command_executor, 'execute')
    def test_backup_single_path(self, mock_execute):
        restic.backup(['/tmp/dummy-file.txt'])
        mock_execute.assert_called_with(
            ['restic', '--json', 'backup', '/tmp/dummy-file.txt'])

    @mock.patch.object(backup.command_executor, 'execute')
    def test_backup_multiple_paths(self, mock_execute):
        restic.backup(['/tmp/dummy-file-1.txt', '/tmp/dummy-file-2.txt'])
        mock_execute.assert_called_with([
            'restic', '--json', 'backup', '/tmp/dummy-file-1.txt',
            '/tmp/dummy-file-2.txt'
        ])

    @mock.patch.object(backup.command_executor, 'execute')
    def test_excludes_single_pattern(self, mock_execute):
        restic.backup(['/data/music'], exclude_patterns=['Justin Bieber*'])
        mock_execute.assert_called_with([
            'restic', '--json', 'backup', '/data/music', '--exclude',
            'Justin Bieber*'
        ])

    @mock.patch.object(backup.command_executor, 'execute')
    def test_excludes_multiple_patterns(self, mock_execute):
        restic.backup(['/data/music'],
                      exclude_patterns=['Justin Bieber*', 'Selena Gomez*'])
        mock_execute.assert_called_with([
            'restic', '--json', 'backup', '/data/music', '--exclude',
            'Justin Bieber*', '--exclude', 'Selena Gomez*'
        ])

    @mock.patch.object(backup.command_executor, 'execute')
    def test_excludes_single_exclude_file(self, mock_execute):
        restic.backup(['/data/music'], exclude_files=['bad-songs.txt'])
        mock_execute.assert_called_with([
            'restic', '--json', 'backup', '/data/music', '--exclude-file',
            'bad-songs.txt'
        ])
