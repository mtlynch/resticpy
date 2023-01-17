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
