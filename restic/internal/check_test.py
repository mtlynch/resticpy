import unittest
from unittest import mock

import restic
from restic.internal import check
from restic.internal import command_executor

# Ignore suggestions to turn methods into functions.
# pylint: disable=R0201


class CheckTest(unittest.TestCase):

    @mock.patch.object(check.command_executor, 'execute')
    def test_check_simple(self, mock_execute):
        restic.check()

        mock_execute.assert_called_with(['restic', '--json', 'check'])

    @mock.patch.object(check.command_executor, 'execute')
    def test_check_and_read_data(self, mock_execute):
        restic.check(read_data=True)

        mock_execute.assert_called_with(
            ['restic', '--json', 'check', '--read-data'])

    @mock.patch.object(check.command_executor, 'execute')
    def test_check_returns_none_on_restic_failure(self, mock_execute):
        mock_execute.side_effect = command_executor.ResticFailedError(
            'dummy restic failure')

        self.assertIsNone(restic.check())
