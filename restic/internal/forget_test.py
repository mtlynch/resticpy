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

    @mock.patch.object(forget.command_executor, 'execute')
    def test_parses_result_json(self, mock_execute):
        mock_execute.return_value = """
[{"tags":null,"host":"ecb5551395ae","paths":["/tmp/tmp6ew1vzp2/mydata.txt"],"keep":[{"time":"2021-03-16T00:10:37.015657013Z","tree":"4483c2c6c1386abb9f47497cf108bab19e09c42430d32cd640a4f6f97137841f","paths":["/tmp/tmp6ew1vzp2/mydata.txt"],"hostname":"ecb5551395ae","username":"circleci","uid":3434,"gid":3434,"id":"3f6de49c6461ffd42900a204655708a3e136a3814abe298c07f27e412e2b6a43","short_id":"3f6de49c"}],"remove":null,"reasons":[{"snapshot":{"time":"2021-03-16T00:10:37.015657013Z","tree":"4483c2c6c1386abb9f47497cf108bab19e09c42430d32cd640a4f6f97137841f","paths":["/tmp/tmp6ew1vzp2/mydata.txt"],"hostname":"ecb5551395ae","username":"circleci","uid":3434,"gid":3434},"matches":["daily snapshot"],"counters":{"daily":4}}]}]
""".lstrip()
        forget_result = restic.forget()
        self.assertEqual(
            {
                'message_type': 'summary',
                'files_new': 1,
                'files_changed': 0,
                'files_unmodified': 0,
                'dirs_new': 2,
                'dirs_changed': 0,
                'dirs_unmodified': 0,
                'data_blobs': 1,
                'tree_blobs': 3,
                'data_added': 1115,
                'total_files_processed': 1,
                'total_bytes_processed': 20,
                'total_duration': 0.216764185,
                'snapshot_id': '01d88ea7'
            }, forget_result)
