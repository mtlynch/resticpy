import unittest
from unittest import mock

import restic
from restic.internal import snapshots


class SnapshotsTest(unittest.TestCase):

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

    @mock.patch.object(snapshots.command_executor, 'execute')
    def test_snapshots_parses_result_json(self, mock_execute):
        mock_execute.return_value = """
[
  {
    "group_key": {
      "hostname": "ace809d23440",
      "paths": null,
      "tags": null
    },
    "snapshots": [
      {
        "gid": 3434,
        "hostname": "ace809d23440",
        "id": "bbe7f04941ed969ee940bb41dc04196027fcfb83dbdfea93c16afb2cb9f6dd81",
        "paths": [
          "/tmp/tmp6594jneh/mydata.txt"
        ],
        "short_id": "bbe7f049",
        "time": "2021-03-28T21:31:44.477122573Z",
        "tree": "f589421bafdae95f5be5eea6285074b7ddc54aa0ffd1ad606f74d1e6207d20a3",
        "uid": 3434,
        "username": "circleci"
      }
    ]
  }
]
""".strip()

        # Ignore complaint about too long of a line.
        # pylint: disable=C0301
        self.assertEqual([{
            'group_key': {
                'hostname': 'ace809d23440',
                'paths': None,
                'tags': None
            },
            'snapshots': [{
                'time':
                    '2021-03-28T21:31:44.477122573Z',
                'tree':
                    'f589421bafdae95f5be5eea6285074b7ddc54aa0ffd1ad606f74d1e6207d20a3',
                'paths': ['/tmp/tmp6594jneh/mydata.txt'],
                'hostname':
                    'ace809d23440',
                'username':
                    'circleci',
                'uid':
                    3434,
                'gid':
                    3434,
                'id':
                    'bbe7f04941ed969ee940bb41dc04196027fcfb83dbdfea93c16afb2cb9f6dd81',
                'short_id':
                    'bbe7f049'
            }]
        }], restic.snapshots())
