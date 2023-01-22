import unittest
from unittest import mock

import restic
from restic.internal import rewrite


class RewriteTest(unittest.TestCase):

    @mock.patch.object(rewrite.command_executor, 'execute')
    def test_rewrite_single_path(self, mock_execute):
        restic.rewrite(exclude=['/foo/bar'])
        mock_execute.assert_called_with(
            ['restic', '--json', 'rewrite', '--exclude', '/foo/bar'])

    @mock.patch.object(rewrite.command_executor, 'execute')
    def test_rewrite_multiple_paths(self, mock_execute):
        restic.rewrite(exclude=['/foo/bar', '/biz/baz'])
        mock_execute.assert_called_with([
            'restic', '--json', 'rewrite', '--exclude', '/foo/bar', '--exclude',
            '/biz/baz'
        ])

    @mock.patch.object(rewrite.command_executor, 'execute')
    def test_rewrite_specific_snapshot_id(self, mock_execute):
        restic.rewrite(exclude=['/foo/bar'], snapshot_id='dummy-snapshot-id')
        mock_execute.assert_called_with([
            'restic', '--json', 'rewrite', '--exclude', '/foo/bar',
            'dummy-snapshot-id'
        ])

    @mock.patch.object(rewrite.command_executor, 'execute')
    def test_rewrite_and_forget_specific_snapshot_id(self, mock_execute):
        restic.rewrite(exclude=['/foo/bar'],
                       forget=True,
                       snapshot_id='dummy-snapshot-id')
        mock_execute.assert_called_with([
            'restic', '--json', 'rewrite', '--exclude', '/foo/bar', '--forget',
            'dummy-snapshot-id'
        ])

    @mock.patch.object(rewrite.command_executor, 'execute')
    def test_rewrite_from_exclude_file(self, mock_execute):
        restic.rewrite(exclude_file='/data/excludes.txt')
        mock_execute.assert_called_with([
            'restic', '--json', 'rewrite', '--exclude-file',
            '/data/excludes.txt'
        ])

    @mock.patch.object(rewrite.command_executor, 'execute')
    def test_rewrite_as_dry_run(self, mock_execute):
        restic.rewrite(exclude=['/foo/bar'],
                       dry_run=True,
                       snapshot_id='dummy-snapshot-id')
        mock_execute.assert_called_with([
            'restic',
            '--json',
            'rewrite',
            '--exclude',
            '/foo/bar',
            '--dry-run',
            'dummy-snapshot-id',
        ])
