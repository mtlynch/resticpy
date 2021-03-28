import unittest
from unittest import mock

import restic
from restic.internal import snapshots

# Ignore suggestions to turn methods into functions.
# pylint: disable=R0201


class SelfUpdateTest(unittest.TestCase):

    @mock.patch.object(snapshots.command_executor, 'execute')
    def test_snapshots_simple(self, mock_execute):
        mock_execute.return_value = '{}'

        restic.snapshots()

        mock_execute.assert_called_with(['restic', '--json', 'snapshots'])

    @mock.patch.object(snapshots.command_executor, 'execute')
    def test_snapshots_group_by_host(self, mock_execute):
        mock_execute.return_value = '{}'

        restic.snapshots(group_by='host')

        mock_execute.assert_called_with(
            ['restic', '--json', 'snapshots', '--group-by', 'host'])
