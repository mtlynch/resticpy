import unittest
from unittest import mock

import restic
from restic.internal import cat


class CatMasterkeyTest(unittest.TestCase):

    @mock.patch.object(cat.command_executor, 'execute')
    def test_cat_masterkey(self, mock_execute):
        mock_execute.return_value = """{ "mac":
{ "k": "Pz4lpSpJ3/qbgNkv9g5m9g==", "r": "eSzdCoRqKgUMWSwJGPylCg==" },
"encrypt": "BPlHYRVMNhu12MlJH5Zq91Lm1KH09UqVk0QRr2Jcblo="}"""

        result = restic.cat.masterkey()

        mock_execute.assert_called_with([
            'restic',
            '--json',
            'cat',
            'masterkey',
        ])

        self.assertEqual(
            {
                'mac': {
                    'k': 'Pz4lpSpJ3/qbgNkv9g5m9g==',
                    'r': 'eSzdCoRqKgUMWSwJGPylCg=='
                },
                'encrypt': 'BPlHYRVMNhu12MlJH5Zq91Lm1KH09UqVk0QRr2Jcblo='
            }, result)


class CatConfigTest(unittest.TestCase):

    @mock.patch.object(cat.command_executor, 'execute')
    def test_cat_config(self, mock_execute):
        mock_execute.return_value = """{ "version": 2,
"id": "dc0268fe690023237565f1ca58c257350ea5b86ffabc3a067933c271a3c0998a",
"chunker_polynomial": "2f7ca3c3c5dbad"}"""

        result = restic.cat.config()

        mock_execute.assert_called_with([
            'restic',
            '--json',
            'cat',
            'config',
        ])

        self.assertEqual(
            {
                'version':
                    2,
                'id':
                    'dc0268fe690023237565f1ca58c257350ea5b86ffabc3a067933c271a3c0998a',  # pylint: disable=C0301
                'chunker_polynomial':
                    '2f7ca3c3c5dbad'
            },
            result)


class CatLockTest(unittest.TestCase):

    @mock.patch.object(cat.command_executor, 'execute')
    def test_cat_lock(self, mock_execute):
        # pylint: disable-next=line-too-long
        mock_execute.return_value = """{ "time": "2025-11-19T12:10:09.853558935Z", "exclusive": true, "hostname": "some-random-hostname", "username": "some-random-username", "pid": 1337 }"""

        result = restic.cat.lock(
            lock_id=
            '444974b52718c2255fc908275e6549b307465f31c3147c75490887ae06a6b0a1')

        mock_execute.assert_called_with([
            'restic',
            '--json',
            'cat',
            'lock',
            '444974b52718c2255fc908275e6549b307465f31c3147c75490887ae06a6b0a1',
        ])

        self.assertEqual(
            {
                'time': '2025-11-19T12:10:09.853558935Z',
                'exclusive': True,
                'hostname': 'some-random-hostname',
                'username': 'some-random-username',
                'pid': 1337,
            }, result)


class CatLockNoLockTest(unittest.TestCase):

    @mock.patch.object(cat.command_executor, 'execute')
    def test_cat_lock(self, mock_execute):
        # pylint: disable-next=line-too-long
        mock_execute.return_value = """{ "time": "2025-11-19T12:10:09.853558935Z", "exclusive": true, "hostname": "some-random-hostname", "username": "some-random-username", "pid": 1337 }"""

        result = restic.cat.lock(
            lock_id=
            '444974b52718c2255fc908275e6549b307465f31c3147c75490887ae06a6b0a1',
            no_lock=True)

        mock_execute.assert_called_with([
            'restic', '--json', 'cat', 'lock',
            '444974b52718c2255fc908275e6549b307465f31c3147c75490887ae06a6b0a1',
            '--no-lock'
        ])

        self.assertEqual(
            {
                'time': '2025-11-19T12:10:09.853558935Z',
                'exclusive': True,
                'hostname': 'some-random-hostname',
                'username': 'some-random-username',
                'pid': 1337,
            }, result)
