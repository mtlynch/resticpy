import unittest
from unittest import mock

import restic
from restic.internal import snapshots


class FindTest(unittest.TestCase):

    @mock.patch.object(snapshots.command_executor, 'execute')
    def test_find_simple(self, mock_execute):
        mock_execute.return_value = '{}'

        restic.find('filename')

        mock_execute.assert_called_with(
            ['restic', '--json', 'find', 'filename'])

    @mock.patch.object(snapshots.command_executor, 'execute')
    def test_find_parses_result_json(self, mock_execute):
        mock_execute.return_value = '''
[{"matches":[{"path":"/filename","permissions":"-rw-r--r--","type":"file","mode":420,"mtime":"2022-01-01T10:00:00.000000000-07:00","atime":"2022-01-01T10:00:00.000000000-07:00","ctime":"2022-01-01T10:00:00.000000000-07:00","uid":10000,"gid":10000,"user":"user","group":"group","device_id":10000,"size":1024,"links":1}],"hits":1,"snapshot":"f589421bafdae95f5be5eea6285074b7ddc54aa0ffd1ad606f74d1e6207d20a3"}]
'''.strip()

        # Ignore complaint about too long of a line.
        # pylint: disable=C0301
        self.assertEqual([{
            'matches': [{
                'path': '/filename',
                'permissions': '-rw-r--r--',
                'type': 'file',
                'mode': 420,
                'mtime': '2022-01-01T10:00:00.000000000-07:00',
                'atime': '2022-01-01T10:00:00.000000000-07:00',
                'ctime': '2022-01-01T10:00:00.000000000-07:00',
                'uid': 10000,
                'gid': 10000,
                'user': 'user',
                'group': 'group',
                'device_id': 10000,
                'size': 1024,
                'links': 1
            }],
            'hits':
                1,
            'snapshot':
                'f589421bafdae95f5be5eea6285074b7ddc54aa0ffd1ad606f74d1e6207d20a3'
        }], restic.find('filename'))
