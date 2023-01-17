import unittest
from unittest import mock

import restic
from restic.internal import backup


class BackupTest(unittest.TestCase):

    @mock.patch.object(backup.command_executor, 'execute')
    def test_backup_single_path(self, mock_execute):
        mock_execute.return_value = '{}'

        restic.backup(['/tmp/dummy-file.txt'])

        mock_execute.assert_called_with(
            ['restic', '--json', 'backup', '/tmp/dummy-file.txt'])

    @mock.patch.object(backup.command_executor, 'execute')
    def test_backup_multiple_paths(self, mock_execute):
        mock_execute.return_value = '{}'

        restic.backup(['/tmp/dummy-file-1.txt', '/tmp/dummy-file-2.txt'])

        mock_execute.assert_called_with([
            'restic', '--json', 'backup', '/tmp/dummy-file-1.txt',
            '/tmp/dummy-file-2.txt'
        ])

    @mock.patch.object(backup.command_executor, 'execute')
    def test_excludes_single_pattern(self, mock_execute):
        mock_execute.return_value = '{}'

        restic.backup(['/data/music'], exclude_patterns=['Justin Bieber*'])

        mock_execute.assert_called_with([
            'restic', '--json', 'backup', '/data/music', '--exclude',
            'Justin Bieber*'
        ])

    @mock.patch.object(backup.command_executor, 'execute')
    def test_excludes_multiple_patterns(self, mock_execute):
        mock_execute.return_value = '{}'

        restic.backup(['/data/music'],
                      exclude_patterns=['Justin Bieber*', 'Selena Gomez*'])

        mock_execute.assert_called_with([
            'restic', '--json', 'backup', '/data/music', '--exclude',
            'Justin Bieber*', '--exclude', 'Selena Gomez*'
        ])

    @mock.patch.object(backup.command_executor, 'execute')
    def test_tags(self, mock_execute):
        mock_execute.return_value = '{}'

        restic.backup(['/data/music'], tags=['musician1', 'musician2'])

        mock_execute.assert_called_with([
            'restic', '--json', 'backup', '/data/music', '--tag', 'musician1',
            '--tag', 'musician2'
        ])

    @mock.patch.object(backup.command_executor, 'execute')
    def test_dry_run(self, mock_execute):
        mock_execute.return_value = '{}'

        restic.backup(['/data/music'], dry_run=True)

        mock_execute.assert_called_with(
            ['restic', '--json', 'backup', '/data/music', '--dry-run'])

    @mock.patch.object(backup.command_executor, 'execute')
    def test_host(self, mock_execute):
        mock_execute.return_value = '{}'

        restic.backup(['/data/music'], host='myhost')

        mock_execute.assert_called_with(
            ['restic', '--json', 'backup', '/data/music', '--host', 'myhost'])

    @mock.patch.object(backup.command_executor, 'execute')
    def test_scan(self, mock_execute):
        mock_execute.return_value = '{}'

        restic.backup(['/data/music'], scan=False)

        mock_execute.assert_called_with(
            ['restic', '--json', 'backup', '/data/music', '--no-scan'])

    @mock.patch.object(backup.command_executor, 'execute')
    def test_excludes_single_exclude_file(self, mock_execute):
        mock_execute.return_value = '{}'

        restic.backup(['/data/music'], exclude_files=['bad-songs.txt'])

        mock_execute.assert_called_with([
            'restic', '--json', 'backup', '/data/music', '--exclude-file',
            'bad-songs.txt'
        ])

    @mock.patch.object(backup.command_executor, 'execute')
    def test_parses_result_json(self, mock_execute):
        mock_execute.return_value = """
{"message_type":"status","percent_done":0,"total_files":1,"total_bytes":20}
{"message_type":"status","percent_done":0,"total_files":1,"total_bytes":20}
{"message_type":"status","percent_done":0,"total_files":1,"total_bytes":20,"current_files":["/tmp/tmpvg2jkmqw/mydata.txt"]}
{"message_type":"status","percent_done":1,"total_files":1,"total_bytes":20,"bytes_done":20,"current_files":["/tmp/tmpvg2jkmqw/mydata.txt"]}
{"message_type":"status","percent_done":1,"total_files":1,"files_done":1,"total_bytes":20,"bytes_done":20,"current_files":["/tmp/tmpvg2jkmqw/mydata.txt"]}
{"message_type":"status","percent_done":1,"total_files":1,"files_done":1,"total_bytes":20,"bytes_done":20}
{"message_type":"status","percent_done":1,"total_files":1,"files_done":1,"total_bytes":20,"bytes_done":20}
{"message_type":"status","percent_done":1,"total_files":1,"files_done":1,"total_bytes":20,"bytes_done":20}
{"message_type":"status","percent_done":1,"total_files":1,"files_done":1,"total_bytes":20,"bytes_done":20}
{"message_type":"status","percent_done":1,"total_files":1,"files_done":1,"total_bytes":20,"bytes_done":20}
{"message_type":"summary","files_new":1,"files_changed":0,"files_unmodified":0,"dirs_new":2,"dirs_changed":0,"dirs_unmodified":0,"data_blobs":1,"tree_blobs":3,"data_added":1115,"total_files_processed":1,"total_bytes_processed":20,"total_duration":0.216764185,"snapshot_id":"01d88ea7"}
""".lstrip()
        backup_summary = restic.backup(['/tmp/dummy-file.txt'])
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
            }, backup_summary)

    @mock.patch.object(backup.command_executor, 'execute')
    def test_parses_result_json_ignores_terminal_markers(self, mock_execute):
        mock_execute.return_value = """
\x1b[2K{"message_type":"status","percent_done":0,"total_files":1,"total_bytes":20}
\x1b[2K{"message_type":"status","percent_done":0,"total_files":1,"total_bytes":20}
\x1b[2K{"message_type":"status","percent_done":0,"total_files":1,"total_bytes":20,"current_files":["/tmp/tmpvg2jkmqw/mydata.txt"]}
\x1b[2K{"message_type":"status","percent_done":1,"total_files":1,"total_bytes":20,"bytes_done":20,"current_files":["/tmp/tmpvg2jkmqw/mydata.txt"]}
\x1b[2K{"message_type":"status","percent_done":1,"total_files":1,"files_done":1,"total_bytes":20,"bytes_done":20,"current_files":["/tmp/tmpvg2jkmqw/mydata.txt"]}
\x1b[2K{"message_type":"status","percent_done":1,"total_files":1,"files_done":1,"total_bytes":20,"bytes_done":20}
\x1b[2K{"message_type":"status","percent_done":1,"total_files":1,"files_done":1,"total_bytes":20,"bytes_done":20}
\x1b[2K{"message_type":"status","percent_done":1,"total_files":1,"files_done":1,"total_bytes":20,"bytes_done":20}
\x1b[2K{"message_type":"status","percent_done":1,"total_files":1,"files_done":1,"total_bytes":20,"bytes_done":20}
\x1b[2K{"message_type":"status","percent_done":1,"total_files":1,"files_done":1,"total_bytes":20,"bytes_done":20}
\x1b[2K{"message_type":"summary","files_new":1,"files_changed":0,"files_unmodified":0,"dirs_new":2,"dirs_changed":0,"dirs_unmodified":0,"data_blobs":1,"tree_blobs":3,"data_added":1115,"total_files_processed":1,"total_bytes_processed":20,"total_duration":0.216764185,"snapshot_id":"01d88ea7"}
""".lstrip()
        backup_summary = restic.backup(['/tmp/dummy-file.txt'])
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
            }, backup_summary)

    @mock.patch.object(backup.command_executor, 'execute')
    def test_wraps_non_json_response(self, mock_execute):
        mock_execute.return_value = '[[invalid response]]'

        with self.assertRaises(backup.UnexpectedResticResult):
            restic.backup(['/tmp/dummy-file.txt'])
