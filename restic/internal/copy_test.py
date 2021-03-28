import unittest
from unittest import mock

import restic
from restic.internal import copy

# Ignore suggestions to turn methods into functions.
# pylint: disable=R0201


class CopyTest(unittest.TestCase):

    @mock.patch.object(copy.command_executor, 'execute')
    def test_copy_simple(self, mock_execute):
        mock_execute.return_value = '{}'

        restic.copy(repo2='s3:https://dummyrepo.example.com/bucket',
                    password_file2='/dummy/pass.txt')

        mock_execute.assert_called_with([
            'restic', '--json', 'copy', '--repo2',
            's3:https://dummyrepo.example.com/bucket', '--password-file2',
            '/dummy/pass.txt'
        ])
