import unittest
from unittest import mock

import restic
from restic.errors import Error
from restic.internal import restore


class RestoreTest(unittest.TestCase):

    @mock.patch.object(restore.command_executor, 'execute')
    def test_restore_with_no_snapshot_id(self, mock_execute):
        restic.restore()
        mock_execute.assert_called_with(
            ['restic', '--json', 'restore', 'latest'])

    @mock.patch.object(restore.command_executor, 'execute')
    def test_restore_specific_snapshot_id(self, mock_execute):
        restic.restore('dummy-snapshot-id')
        mock_execute.assert_called_with(
            ['restic', '--json', 'restore', 'dummy-snapshot-id'])

    @mock.patch.object(restore.command_executor, 'execute')
    def test_restore_specific_snapshot_id_and_target(self, mock_execute):
        restic.restore(snapshot_id='dummy-snapshot-id',
                       target_dir='/tmp/restore')
        mock_execute.assert_called_with([
            'restic', '--json', 'restore', 'dummy-snapshot-id', '--target',
            '/tmp/restore'
        ])

    @mock.patch.object(restore.command_executor, 'execute')
    def test_restore_specific_snapshot_id_and_include(self, mock_execute):
        restic.restore(snapshot_id='dummy-snapshot-id', include='include-path')
        mock_execute.assert_called_with([
            'restic', '--json', 'restore', 'dummy-snapshot-id', '--include',
            'include-path'
        ])

    @mock.patch.object(restore.command_executor, 'execute')
    def test_restore_exclude_string_instead_of_list(self, mock_execute):
        mock_execute.return_value = ''
        with self.assertRaises(Error):
            restic.restore(snapshot_id='dummy-snapshot-id',
                           exclude='exclude-path')

    @mock.patch.object(restore.command_executor, 'execute')
    def test_restore_specific_snapshot_id_and_exclude_multiple_paths(
            self, mock_execute):
        restic.restore(snapshot_id='dummy-snapshot-id',
                       exclude=['exclude-path', 'another-path'])
        mock_execute.assert_called_with([
            'restic', '--json', 'restore', 'dummy-snapshot-id', '--exclude',
            'exclude-path', '--exclude', 'another-path'
        ])
