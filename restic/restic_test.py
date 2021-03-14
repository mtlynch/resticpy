import unittest
from unittest import mock

import restic
from restic.internal import generate


class ResticTest(unittest.TestCase):

    def setUp(self):
        self.original_binary = restic.binary_path
        self.original_repository = restic.repository

    def tearDown(self):
        restic.binary_path = self.original_binary
        restic.repository = self.original_repository

    @mock.patch.object(generate.command_executor, 'execute')
    def test_can_change_restic_binary_path(self, mock_execute):
        restic.binary_path = '/dummy/path/to/restic-binary'
        restic.generate()
        mock_execute.assert_called_with(
            ['/dummy/path/to/restic-binary', 'generate'])

    @mock.patch.object(generate.command_executor, 'execute')
    def test_can_set_repository_path(self, mock_execute):
        restic.repository = '/dummy/repo/path'
        restic.generate()
        mock_execute.assert_called_with(
            ['restic', '--repo', '/dummy/repo/path', 'generate'])
