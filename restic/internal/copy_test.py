import unittest
from unittest import mock

import restic
from restic.internal import copy


class CopyTest(unittest.TestCase):

    @mock.patch.object(copy.command_executor, 'execute')
    def test_copy_simple(self, mock_execute):
        mock_execute.return_value = """
snapshot 670792c6 of [/tmp/tmp9k613t9a/mydata.txt] at 2021-03-29 00:56:31.183738563 +0000 UTC)
  copy started, this may take a while...
snapshot 3671204c saved
""".strip()

        restic.copy(repo2='s3:https://dummyrepo.example.com/bucket',
                    password_file2='/dummy/pass.txt')

        mock_execute.assert_called_with([
            'restic', '--json', 'copy', '--repo2',
            's3:https://dummyrepo.example.com/bucket', '--password-file2',
            '/dummy/pass.txt'
        ])
