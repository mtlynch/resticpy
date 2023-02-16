import unittest
from unittest import mock

import restic.errors
from restic.internal import check


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
    def test_check_and_read_data_subset(self, mock_execute):
        restic.check(read_data_subset='10%')

        mock_execute.assert_called_with(
            ['restic', '--json', 'check', '--read-data-subset', '10%'])

    @mock.patch.object(check.command_executor, 'execute')
    def test_check_returns_none_on_restic_failure(self, mock_execute):
        mock_execute.side_effect = restic.errors.ResticFailedError(
            'dummy restic failure')

        self.assertIsNone(restic.check())
