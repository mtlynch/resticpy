import unittest
from unittest import mock

import restic
from restic.internal import generate


class ResticTest(unittest.TestCase):

    def setUp(self):
        self.original_binary = restic.binary_path
        self.original_repository = restic.repository
        self.original_password_file = restic.password_file
        self.use_cache = restic.use_cache

    def tearDown(self):
        restic.binary_path = self.original_binary
        restic.repository = self.original_repository
        restic.password_file = self.original_password_file
        restic.use_cache = self.use_cache

    @mock.patch.object(generate.command_executor, 'execute')
    def test_can_change_restic_binary_path(self, mock_execute):
        restic.binary_path = '/dummy/path/to/restic-binary'
        restic.generate()
        mock_execute.assert_called_with(
            ['/dummy/path/to/restic-binary', '--json', 'generate'])

    @mock.patch.object(generate.command_executor, 'execute')
    def test_can_set_repository_path(self, mock_execute):
        mock_execute.return_value = (
            'created restic repository 054ed643d8 at /media/backup1')

        restic.repository = '/dummy/repo/path'
        restic.init()

        mock_execute.assert_called_with(
            ['restic', '--json', '--repo', '/dummy/repo/path', 'init'])

    @mock.patch.object(generate.command_executor, 'execute')
    def test_can_set_password_file(self, mock_execute):
        mock_execute.return_value = (
            'created restic repository 054ed643d8 at /media/backup1')

        restic.password_file = 'secret-pw.txt'
        restic.init()

        mock_execute.assert_called_with(
            ['restic', '--json', '--password-file', 'secret-pw.txt', 'init'])

    @mock.patch.object(generate.command_executor, 'execute')
    def test_can_set_cache(self, mock_execute):
        mock_execute.return_value = (
            'created restic repository 054ed643d8 at /media/backup1')

        restic.repository = '/dummy/repo/path'
        restic.use_cache = False
        restic.init()

        mock_execute.assert_called_with([
            'restic', '--json', '--repo', '/dummy/repo/path', '--no-cache',
            'init'
        ])
