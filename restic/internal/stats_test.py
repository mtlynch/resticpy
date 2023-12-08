import unittest
from unittest import mock

import restic
from restic.internal import stats


class SelfUpdateTest(unittest.TestCase):

    @mock.patch.object(stats.command_executor, 'execute')
    def test_stats(self, mock_execute):
        mock_execute.return_value = """{
            "total_size": 20,
            "total_file_count": 3
            }
            """

        self.assertEqual({
            'total_size': 20,
            'total_file_count': 3
        }, restic.stats())

        mock_execute.assert_called_with(['restic', '--json', 'stats'])

    @mock.patch.object(stats.command_executor, 'execute')
    def test_stats_with_mode(self, mock_execute):
        mock_execute.return_value = """{
            "total_size": 20,
            "total_file_count": 1,
            "total_blob_count": 1
            }
            """

        self.assertEqual(
            {
                'total_size': 20,
                'total_file_count': 1,
                'total_blob_count': 1
            }, restic.stats(mode='blobs-per-file'))

        mock_execute.assert_called_with(
            ['restic', '--json', 'stats', '--mode', 'blobs-per-file'])

    @mock.patch.object(stats.command_executor, 'execute')
    def test_stats_with_tag(self, mock_execute):
        mock_execute.return_value = """{
            "total_size": 10,
            "total_file_count": 2
            }
            """

        self.assertEqual({
            'total_size': 10,
            'total_file_count': 2
        }, restic.stats(tags=['musician1']))

        mock_execute.assert_called_with(
            ['restic', '--json', 'stats', '--tag', 'musician1'])

    @mock.patch.object(stats.command_executor, 'execute')
    def test_stats_with_host(self, mock_execute):
        mock_execute.return_value = """{
            "total_size": 10,
            "total_file_count": 2
            }
            """

        self.assertEqual({
            'total_size': 10,
            'total_file_count': 2
        }, restic.stats(host='myhost'))

        mock_execute.assert_called_with(
            ['restic', '--json', 'stats', '--host', 'myhost'])
