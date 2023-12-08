import unittest
from unittest import mock

import restic.errors
from restic.internal import forget


class ForgetTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    @mock.patch.object(forget.command_executor, 'execute')
    def test_forget(self, mock_execute):
        mock_execute.return_value = '{}'
        restic.forget()
        mock_execute.assert_called_with(['restic', '--json', 'forget'])

    @mock.patch.object(forget.command_executor, 'execute')
    def test_forget_empty_return(self, mock_execute):
        mock_execute.return_value = ''
        restic.forget()
        mock_execute.assert_called_with(['restic', '--json', 'forget'])

    @mock.patch.object(forget.command_executor, 'execute')
    def test_dry_run(self, mock_execute):
        mock_execute.return_value = '{}'

        restic.forget(dry_run=True)

        mock_execute.assert_called_with(
            ['restic', '--json', 'forget', '--dry-run'])

    @mock.patch.object(forget.command_executor, 'execute')
    def test_forget_with_group_by(self, mock_execute):
        mock_execute.return_value = '{}'
        restic.forget(prune=True, group_by='host')
        mock_execute.assert_called_with(
            ['restic', '--json', 'forget', '--group-by', 'host', '--prune'])

    @mock.patch.object(forget.command_executor, 'execute')
    def test_forget_with_single_tag(self, mock_execute):
        mock_execute.return_value = '{}'
        restic.forget(prune=True, tags=['musician1'])
        mock_execute.assert_called_with(
            ['restic', '--json', 'forget', '--tag', 'musician1', '--prune'])

    # See restic documentation:
    # https://restic.readthedocs.io/en/latest/060_forget.html#removing-snapshots-according-to-a-policy
    #
    # Remove all but the last snapshot of all snapshots that have either
    # the foo or bar tag set:
    # 'restic forget --tag foo --tag bar --keep-last 1'
    @mock.patch.object(forget.command_executor, 'execute')
    def test_forget_with_multiple_tags_with_or_relation(self, mock_execute):
        mock_execute.return_value = '{}'
        restic.forget(prune=True, tags=['musician1', 'musician2'])
        mock_execute.assert_called_with([
            'restic', '--json', 'forget', '--tag', 'musician1', '--tag',
            'musician2', '--prune'
        ])

    # See restic documentation:
    # https://restic.readthedocs.io/en/latest/060_forget.html#removing-snapshots-according-to-a-policy
    #
    # Remove all but the last snapshot of all snapshots that have both
    # the tag foo and bar set:
    # 'restic forget --tag foo,bar --keep-last 1'
    @mock.patch.object(forget.command_executor, 'execute')
    def test_forget_with_multiple_tags_with_and_relation(self, mock_execute):
        mock_execute.return_value = '{}'
        restic.forget(prune=True, tags=['musician1,musician2'])
        mock_execute.assert_called_with([
            'restic', '--json', 'forget', '--tag', 'musician1,musician2',
            '--prune'
        ])

    @mock.patch.object(forget.command_executor, 'execute')
    def test_forget_with_host(self, mock_execute):
        mock_execute.return_value = '{}'
        restic.forget(prune=True, host='myhost')
        mock_execute.assert_called_with(
            ['restic', '--json', 'forget', '--host', 'myhost', '--prune'])

    @mock.patch.object(forget.command_executor, 'execute')
    def test_forget_keep_last_10(self, mock_execute):
        mock_execute.return_value = '{}'
        restic.forget(keep_last=10)
        mock_execute.assert_called_with(
            ['restic', '--json', 'forget', '--keep-last', '10'])

    @mock.patch.object(forget.command_executor, 'execute')
    def test_forget_keep_hourly_10(self, mock_execute):
        mock_execute.return_value = '{}'
        restic.forget(keep_hourly=10)
        mock_execute.assert_called_with(
            ['restic', '--json', 'forget', '--keep-hourly', '10'])

    @mock.patch.object(forget.command_executor, 'execute')
    def test_forget_all_except_last_30_days(self, mock_execute):
        mock_execute.return_value = '{}'
        restic.forget(keep_daily=30)
        mock_execute.assert_called_with(
            ['restic', '--json', 'forget', '--keep-daily', '30'])

    @mock.patch.object(forget.command_executor, 'execute')
    def test_forget_keep_weekly_10(self, mock_execute):
        mock_execute.return_value = '{}'
        restic.forget(keep_weekly=10)
        mock_execute.assert_called_with(
            ['restic', '--json', 'forget', '--keep-weekly', '10'])

    @mock.patch.object(forget.command_executor, 'execute')
    def test_forget_keep_monthly_10(self, mock_execute):
        mock_execute.return_value = '{}'
        restic.forget(keep_monthly=10)
        mock_execute.assert_called_with(
            ['restic', '--json', 'forget', '--keep-monthly', '10'])

    @mock.patch.object(forget.command_executor, 'execute')
    def test_forget_keep_yearly_10(self, mock_execute):
        mock_execute.return_value = '{}'
        restic.forget(keep_yearly=10)
        mock_execute.assert_called_with(
            ['restic', '--json', 'forget', '--keep-yearly', '10'])

    @mock.patch.object(forget.command_executor, 'execute')
    def test_forget_all_except_last_30_days_and_prune(self, mock_execute):
        mock_execute.return_value = '{}'
        restic.forget(prune=True, keep_daily=30)
        mock_execute.assert_called_with(
            ['restic', '--json', 'forget', '--keep-daily', '30', '--prune'])

    @mock.patch.object(forget.command_executor, 'execute')
    def test_forget_and_prune(self, mock_execute):
        mock_execute.return_value = '{}'
        restic.forget(prune=True)
        mock_execute.assert_called_with(
            ['restic', '--json', 'forget', '--prune'])

    @mock.patch.object(forget.command_executor, 'execute')
    def test_forget_and_keep_within(self, mock_execute):
        mock_execute.return_value = '{}'
        restic.forget(prune=True, keep_within='60d')
        mock_execute.assert_called_with(
            ['restic', '--json', 'forget', '--keep-within', '60d', '--prune'])

    @mock.patch.object(forget.command_executor, 'execute')
    def test_parses_result_json(self, mock_execute):
        # Ignore complaint about too long of a line.
        # pylint: disable=C0301
        mock_execute.return_value = """
[{"tags": null, "host": "ecb5551395ae", "paths": ["/tmp/tmp6ew1vzp2/mydata.txt"], "keep": [{"time": "2021-03-16T00:10:37.015657013Z", "tree": "4483c2c6c1386abb9f47497cf108bab19e09c42430d32cd640a4f6f97137841f", "paths": ["/tmp/tmp6ew1vzp2/mydata.txt"], "hostname": "ecb5551395ae", "username": "circleci", "uid": 3434, "gid": 3434, "id": "3f6de49c6461ffd42900a204655708a3e136a3814abe298c07f27e412e2b6a43", "short_id": "3f6de49c"}], "remove": null, "reasons": [{"snapshot": {"time": "2021-03-16T00:10:37.015657013Z", "tree": "4483c2c6c1386abb9f47497cf108bab19e09c42430d32cd640a4f6f97137841f", "paths": ["/tmp/tmp6ew1vzp2/mydata.txt"], "hostname": "ecb5551395ae", "username": "circleci", "uid": 3434, "gid": 3434}, "matches": ["daily snapshot"], "counters": {"daily": 4}}]}]
""".strip()
        forget_result = restic.forget()
        self.assertEqual([{
            'tags':
                None,
            'host':
                'ecb5551395ae',
            'paths': ['/tmp/tmp6ew1vzp2/mydata.txt'],
            'keep': [{
                'time':
                    '2021-03-16T00:10:37.015657013Z',
                'tree':
                    '4483c2c6c1386abb9f47497cf108bab19e09c42430d32cd640a4f6f97137841f',
                'paths': ['/tmp/tmp6ew1vzp2/mydata.txt'],
                'hostname':
                    'ecb5551395ae',
                'username':
                    'circleci',
                'uid':
                    3434,
                'gid':
                    3434,
                'id':
                    '3f6de49c6461ffd42900a204655708a3e136a3814abe298c07f27e412e2b6a43',
                'short_id':
                    '3f6de49c'
            }],
            'remove':
                None,
            'reasons': [{
                'snapshot': {
                    'time':
                        '2021-03-16T00:10:37.015657013Z',
                    'tree':
                        '4483c2c6c1386abb9f47497cf108bab19e09c42430d32cd640a4f6f97137841f',
                    'paths': ['/tmp/tmp6ew1vzp2/mydata.txt'],
                    'hostname':
                        'ecb5551395ae',
                    'username':
                        'circleci',
                    'uid':
                        3434,
                    'gid':
                        3434
                },
                'matches': ['daily snapshot'],
                'counters': {
                    'daily': 4
                }
            }]
        }], forget_result)

    @mock.patch.object(forget.command_executor, 'execute')
    def test_parses_result_json_and_ignores_text_afterwards(self, mock_execute):
        # Ignore complaint about too long of a line.
        # pylint: disable=C0301
        mock_execute.return_value = """
[{"tags": null, "host": "ecb5551395ae", "paths": ["/tmp/tmp6ew1vzp2/mydata.txt"], "keep": [{"time": "2021-03-16T00:10:37.015657013Z", "tree": "4483c2c6c1386abb9f47497cf108bab19e09c42430d32cd640a4f6f97137841f", "paths": ["/tmp/tmp6ew1vzp2/mydata.txt"], "hostname": "ecb5551395ae", "username": "circleci", "uid": 3434, "gid": 3434, "id": "3f6de49c6461ffd42900a204655708a3e136a3814abe298c07f27e412e2b6a43", "short_id": "3f6de49c"}], "remove": null, "reasons": [{"snapshot": {"time": "2021-03-16T00:10:37.015657013Z", "tree": "4483c2c6c1386abb9f47497cf108bab19e09c42430d32cd640a4f6f97137841f", "paths": ["/tmp/tmp6ew1vzp2/mydata.txt"], "hostname": "ecb5551395ae", "username": "circleci", "uid": 3434, "gid": 3434}, "matches": ["daily snapshot"], "counters": {"daily": 4}}]}]
loading indexes...
loading all snapshots...
finding data that is still in use for 2 snapshots
[0:00] 100.00%  2 / 2 snapshots

searching used packs...
collecting packs for deletion and repacking
[0:00] 100.00%  6 / 6 packs processed


to repack:            0 blobs / 0 B
this removes          0 blobs / 0 B
to delete:            0 blobs / 0 B
total prune:          0 blobs / 0 B
remaining:           49 blobs / 4.890 MiB
unused size after prune: 0 B (0.00% of remaining size)

done
""".lstrip()
        forget_result = restic.forget()
        self.assertEqual([{
            'tags':
                None,
            'host':
                'ecb5551395ae',
            'paths': ['/tmp/tmp6ew1vzp2/mydata.txt'],
            'keep': [{
                'time':
                    '2021-03-16T00:10:37.015657013Z',
                'tree':
                    '4483c2c6c1386abb9f47497cf108bab19e09c42430d32cd640a4f6f97137841f',
                'paths': ['/tmp/tmp6ew1vzp2/mydata.txt'],
                'hostname':
                    'ecb5551395ae',
                'username':
                    'circleci',
                'uid':
                    3434,
                'gid':
                    3434,
                'id':
                    '3f6de49c6461ffd42900a204655708a3e136a3814abe298c07f27e412e2b6a43',
                'short_id':
                    '3f6de49c'
            }],
            'remove':
                None,
            'reasons': [{
                'snapshot': {
                    'time':
                        '2021-03-16T00:10:37.015657013Z',
                    'tree':
                        '4483c2c6c1386abb9f47497cf108bab19e09c42430d32cd640a4f6f97137841f',
                    'paths': ['/tmp/tmp6ew1vzp2/mydata.txt'],
                    'hostname':
                        'ecb5551395ae',
                    'username':
                        'circleci',
                    'uid':
                        3434,
                    'gid':
                        3434
                },
                'matches': ['daily snapshot'],
                'counters': {
                    'daily': 4
                }
            }]
        }], forget_result)

    @mock.patch.object(forget.command_executor, 'execute')
    def test_forget_raises_exception_when_response_is_invalid_json(
            self, mock_execute):
        mock_execute.return_value = '{{{{{{{[[[[[['
        with self.assertRaises(restic.errors.UnexpectedResticResponse):
            restic.forget()
