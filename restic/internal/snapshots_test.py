import unittest
from unittest import mock

import restic
from restic.internal import snapshots


class SnapshotsTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    @mock.patch.object(snapshots.command_executor, 'execute')
    def test_snapshots_simple(self, mock_execute):
        mock_execute.return_value = '[]'

        self.assertEqual([], restic.snapshots())

        mock_execute.assert_called_with(['restic', '--json', 'snapshots'])

    @mock.patch.object(snapshots.command_executor, 'execute')
    def test_snapshots_group_by_host(self, mock_execute):
        mock_execute.return_value = '[]'

        self.assertEqual([], restic.snapshots(group_by='host'))

        mock_execute.assert_called_with(
            ['restic', '--json', 'snapshots', '--group-by', 'host'])

    @mock.patch.object(snapshots.command_executor, 'execute')
    def test_snapshots_id(self, mock_execute):
        mock_execute.return_value = '[]'

        self.assertEqual([], restic.snapshots(snapshot_id='latest'))

        mock_execute.assert_called_with(
            ['restic', '--json', 'snapshots', 'latest'])

    @mock.patch.object(snapshots.command_executor, 'execute')
    def test_snapshots_tags(self, mock_execute):
        mock_execute.return_value = '[]'

        self.assertEqual([], restic.snapshots(tags=['test', 'test2']))

        mock_execute.assert_called_with(
            ['restic', '--json', 'snapshots', '--tag', 'test,test2'])

    @mock.patch.object(snapshots.command_executor, 'execute')
    def test_snapshots_path(self, mock_execute):
        mock_execute.return_value = '[]'

        self.assertEqual([], restic.snapshots(path='/tmp'))

        mock_execute.assert_called_with(
            ['restic', '--json', 'snapshots', '--path', '/tmp'])

    @mock.patch.object(snapshots.command_executor, 'execute')
    def test_snapshots_host(self, mock_execute):
        mock_execute.return_value = '[]'

        self.assertEqual([], restic.snapshots(host='localhost'))

        mock_execute.assert_called_with(
            ['restic', '--json', 'snapshots', '--host', 'localhost'])

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

    @mock.patch.object(snapshots.command_executor, 'execute')
    def test_snapshots_parses_multiple_snapshots_json(self, mock_execute):
        mock_execute.return_value = """
[
    {
        "group_key": {
            "hostname": "3099758ccbd9",
            "paths": null,
            "tags": null
        },
        "snapshots": [
            {
                "time": "2023-12-31T20:39:22.449822393Z",
                "tree": "d4aed49b16b1fcd2ebcfbc8cfd7c53bcff2397b8673b6764dd6411223775d6b2",
                "paths": [
                    "/tmp/tmpuvf9pfam/mydata.txt"
                ],
                "hostname": "3099758ccbd9",
                "username": "circleci",
                "uid": 1001,
                "gid": 1002,
                "program_version": "restic 0.16.2",
                "id": "7540e94d8117078bb26b0e4a85dd353a41665e084d3771f04e5f72f6b0f24a6f",
                "short_id": "7540e94d"
            },
            {
                "time": "2023-12-31T20:39:25.811155387Z",
                "parent": "7540e94d8117078bb26b0e4a85dd353a41665e084d3771f04e5f72f6b0f24a6f",
                "tree": "a39c45c1b202985f766a177a663a5e4f37acd5bfa9bd324fb4eaf62a3c3e0dea",
                "paths": [
                    "/tmp/tmpuvf9pfam/mydata.txt"
                ],
                "hostname": "3099758ccbd9",
                "username": "circleci",
                "uid": 1001,
                "gid": 1002,
                "program_version": "restic 0.16.2",
                "id": "57d3496886edf2cb0e808838734dc108fb1d929ae80cafdb68597e75702aecbb",
                "short_id": "57d34968"
            }
        ]
    }
]
""".strip()

        # Ignore complaint about too long of a line.
        # pylint: disable=C0301
        self.assertEqual([{
            'group_key': {
                'hostname': '3099758ccbd9',
                'paths': None,
                'tags': None
            },
            'snapshots': [{
                'time':
                    '2023-12-31T20:39:22.449822393Z',
                'tree':
                    'd4aed49b16b1fcd2ebcfbc8cfd7c53bcff2397b8673b6764dd6411223775d6b2',
                'paths': ['/tmp/tmpuvf9pfam/mydata.txt'],
                'hostname':
                    '3099758ccbd9',
                'username':
                    'circleci',
                'uid':
                    1001,
                'gid':
                    1002,
                'program_version':
                    'restic 0.16.2',
                'id':
                    '7540e94d8117078bb26b0e4a85dd353a41665e084d3771f04e5f72f6b0f24a6f',
                'short_id':
                    '7540e94d'
            }, {
                'time':
                    '2023-12-31T20:39:25.811155387Z',
                'tree':
                    'a39c45c1b202985f766a177a663a5e4f37acd5bfa9bd324fb4eaf62a3c3e0dea',
                'paths': ['/tmp/tmpuvf9pfam/mydata.txt'],
                'hostname':
                    '3099758ccbd9',
                'username':
                    'circleci',
                'uid':
                    1001,
                'gid':
                    1002,
                'parent':
                    '7540e94d8117078bb26b0e4a85dd353a41665e084d3771f04e5f72f6b0f24a6f',
                'program_version':
                    'restic 0.16.2',
                'id':
                    '57d3496886edf2cb0e808838734dc108fb1d929ae80cafdb68597e75702aecbb',
                'short_id':
                    '57d34968'
            }]
        }], restic.snapshots())
