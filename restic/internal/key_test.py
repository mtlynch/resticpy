import unittest
from unittest import mock

import restic
from restic.internal import key


class KeyListTest(unittest.TestCase):

    @mock.patch.object(key.command_executor, 'execute')
    def test_key_list(self, mock_execute):
        mock_execute.return_value = """
           [{
             "current":true,
             "id":"f1fe5fc6",
             "userName":"user1",
             "hostName":"example",
             "created":"2022-12-02 11:25:13"
            }]"""

        key_result = restic.key.list()

        mock_execute.assert_called_with(['restic', '--json', 'key', 'list'])

        self.assertEqual([{
            'current': True,
            'id': 'f1fe5fc6',
            'userName': 'user1',
            'hostName': 'example',
            'created': '2022-12-02 11:25:13',
        }], key_result)


class KeyAddTest(unittest.TestCase):

    @mock.patch.object(key.command_executor, 'execute')
    def test_key_add(self, mock_execute):
        restic.key.add(new_password_file='/path/to/new-password-file')

        mock_execute.assert_called_with([
            'restic', '--json', 'key', 'add', '--new-password-file',
            '/path/to/new-password-file'
        ])


class KeyPasswdTest(unittest.TestCase):

    @mock.patch.object(key.command_executor, 'execute')
    def test_key_passwd(self, mock_execute):
        restic.key.passwd(new_password_file='/path/to/new-password-file')

        mock_execute.assert_called_with([
            'restic', '--json', 'key', 'passwd', '--new-password-file',
            '/path/to/new-password-file'
        ])


class KeyRemoveTest(unittest.TestCase):

    @mock.patch.object(key.command_executor, 'execute')
    def test_key_remove(self, mock_execute):
        restic.key.remove(key_id='abc123')

        mock_execute.assert_called_with(
            ['restic', '--json', 'key', 'remove', 'abc123'])
