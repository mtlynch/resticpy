import unittest
from unittest import mock

import restic
from restic.internal import forget

# Ignore suggestions to turn methods into functions.
# pylint: disable=R0201


class ForgetTest(unittest.TestCase):

    @mock.patch.object(forget.command_executor, 'execute')
    def test_forget(self, mock_execute):
        restic.forget()
        mock_execute.assert_called_with(['restic', '--json', 'forget'])

    @mock.patch.object(forget.command_executor, 'execute')
    def test_forget_and_prune(self, mock_execute):
        restic.forget(prune=True)
        mock_execute.assert_called_with(
            ['restic', '--json', 'forget', '--prune'])

    @mock.patch.object(forget.command_executor, 'execute')
    def test_forget_all_except_last_30_days(self, mock_execute):
        restic.forget(keep_daily=30)
        mock_execute.assert_called_with(
            ['restic', '--json', 'forget', '--keep-daily', '30'])

    @mock.patch.object(forget.command_executor, 'execute')
    def test_forget_all_except_last_30_days_and_prune(self, mock_execute):
        restic.forget(prune=True, keep_daily=30)
        mock_execute.assert_called_with(
            ['restic', '--json', 'forget', '--prune', '--keep-daily', '30'])
