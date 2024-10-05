import unittest
from unittest import mock

import restic
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
    def test_restore_specific_snapshot_id_and_exclude(self, mock_execute):
        restic.restore(snapshot_id='dummy-snapshot-id', exclude='exclude-path')
        mock_execute.assert_called_with([
            'restic', '--json', 'restore', 'dummy-snapshot-id', '--exclude',
            'exclude-path'
        ])
