import unittest
from unittest import mock

import restic
from restic.internal import cat


class CatPackTest(unittest.TestCase):

    @mock.patch.object(cat.command_executor, 'execute')
    def test_cat_pack(self, mock_execute):
        mock_execute.return_value = '{}'

        restic.cat.pack(
            'b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b878ae4944c')

        mock_execute.assert_called_with([
            'restic', '--json', 'cat', 'pack',
            'b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b878ae4944c'
        ],
                                        binary_mode=True)


class CatBlobTest(unittest.TestCase):

    @mock.patch.object(cat.command_executor, 'execute')
    def test_cat_blob(self, mock_execute):
        mock_execute.return_value = """{"nodes":[
{"name":"bar", "type":"file", "mode":420, "mtime":"2022-12-09T08:36:42.052086879+01:00",
 "atime":"2022-12-09T08:36:42.052086879+01:00","ctime":"2022-12-09T08:36:42.052086879+01:00",
 "uid":501,"gid":0,"user":"user1","group":"wheel","inode":10367333,"device_id":16777232,
 "links":1,"content":[]}]}"""

        result = restic.cat.blob(
            '7d865e959b2466918c9863afca942d0fb89d7c9ac0c99bafc3749504ded97730')

        mock_execute.assert_called_with([
            'restic', '--json', 'cat', 'blob',
            '7d865e959b2466918c9863afca942d0fb89d7c9ac0c99bafc3749504ded97730'
        ],
                                        binary_mode=False)

        self.assertEqual(
            {
                'nodes': [{
                    'name': 'bar',
                    'type': 'file',
                    'mode': 420,
                    'mtime': '2022-12-09T08:36:42.052086879+01:00',
                    'atime': '2022-12-09T08:36:42.052086879+01:00',
                    'ctime': '2022-12-09T08:36:42.052086879+01:00',
                    'uid': 501,
                    'gid': 0,
                    'user': 'user1',
                    'group': 'wheel',
                    'inode': 10367333,
                    'device_id': 16777232,
                    'links': 1,
                    'content': []
                }]
            }, result)


class CatSnapshotTest(unittest.TestCase):

    @mock.patch.object(cat.command_executor, 'execute')
    def test_cat_snapshot(self, mock_execute):
        mock_execute.return_value = """{
        "time": "2022-12-09T08:36:50.814165+01:00",
"tree": "f374bd541231781ab084c5a6a49df21810e2dbebfaa79eb5137172842a01a177",
"paths": [  "/tmp/foo" ], "hostname": "server1", "username": "user1",
"uid": 501, "gid": 20}"""

        result = restic.cat.snapshot('latest')

        mock_execute.assert_called_with(
            ['restic', '--json', 'cat', 'snapshot', 'latest'],
            binary_mode=False)

        self.assertEqual(
            {
                'time':
                    '2022-12-09T08:36:50.814165+01:00',
                'tree':
                    'f374bd541231781ab084c5a6a49df21810e2dbebfaa79eb5137172842a01a177',  # pylint: disable=C0301
                'paths': ['/tmp/foo'],
                'hostname':
                    'server1',
                'username':
                    'user1',
                'uid':
                    501,
                'gid':
                    20
            },
            result)


class CatIndexTest(unittest.TestCase):

    @mock.patch.object(cat.command_executor, 'execute')
    def test_cat_index(self, mock_execute):
        mock_execute.return_value = """{"packs":[
{"id":"54e5a60ae4463fd43b7564bc085bc4664ec0f3cb3aa870c93713fbb39ee05b04","blobs":[
{"id":"f374bd541231781ab084c5a6a49df21810e2dbebfaa79eb5137172842a01a177","type":"tree",
        "offset":217,"length":264,"uncompressed_length":375},
{"id":"9138506698e27def6164ecdd55c3c58d1e7d44b61986ef903514059578e77a8b","type":"tree",
        "offset":0,"length":217,"uncompressed_length":300}]}]}"""

        result = restic.cat.index(
            'bf07a7fbb825fc0aae7bf4a1177b2b31fcf8a3feeaf7092761e18c859ee52a9c')

        mock_execute.assert_called_with([
            'restic', '--json', 'cat', 'index',
            'bf07a7fbb825fc0aae7bf4a1177b2b31fcf8a3feeaf7092761e18c859ee52a9c'
        ],
                                        binary_mode=False)

        self.assertEqual(
            {
                'packs': [{
                    'id':
                        '54e5a60ae4463fd43b7564bc085bc4664ec0f3cb3aa870c93713fbb39ee05b04',  # pylint: disable=C0301
                    'blobs': [
                        {
                            'id':
                                'f374bd541231781ab084c5a6a49df21810e2dbebfaa79eb5137172842a01a177',  # pylint: disable=C0301
                            'type':
                                'tree',
                            'offset':
                                217,
                            'length':
                                264,
                            'uncompressed_length':
                                375
                        },
                        {
                            'id':
                                '9138506698e27def6164ecdd55c3c58d1e7d44b61986ef903514059578e77a8b',  # pylint: disable=C0301
                            'type':
                                'tree',
                            'offset':
                                0,
                            'length':
                                217,
                            'uncompressed_length':
                                300
                        }
                    ]
                }]
            },
            result)


class CatKeyTest(unittest.TestCase):

    @mock.patch.object(cat.command_executor, 'execute')
    def test_cat_key(self, mock_execute):
        mock_execute.return_value = """
{ "created": "2020-08-25T08:32:14.566238264+08:00",
"username": "user1", "hostname": "server1", "kdf": "scrypt",
"N": 32768, "r": 8, "p": 3, "salt": "SALT", "data": "DATA"}"""

        result = restic.cat.key('53ee3b37')

        mock_execute.assert_called_with(
            ['restic', '--json', 'cat', 'key', '53ee3b37'], binary_mode=False)

        self.assertEqual(
            {
                'created': '2020-08-25T08:32:14.566238264+08:00',
                'username': 'user1',
                'hostname': 'server1',
                'kdf': 'scrypt',
                'N': 32768,
                'r': 8,
                'p': 3,
                'salt': 'SALT',
                'data': 'DATA'
            }, result)


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
        ],
                                        binary_mode=False)

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
        ],
                                        binary_mode=False)

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
        mock_execute.return_value = """
{ "time": "2022-12-09T07:52:04.257867084Z", "exclusive": false,
"hostname": "server1", "username": "user1", "pid": 30281,
"uid": 501, "gid": 20}"""

        result = restic.cat.lock(
            '5d70f436aa013f4f1d5af4a5e8149b479c813ab4ceea0bcf8b01f78eac84fd25')

        mock_execute.assert_called_with([
            'restic', '--json', 'cat', 'lock',
            '5d70f436aa013f4f1d5af4a5e8149b479c813ab4ceea0bcf8b01f78eac84fd25'
        ],
                                        binary_mode=False)

        self.assertEqual(
            {
                'time': '2022-12-09T07:52:04.257867084Z',
                'exclusive': False,
                'hostname': 'server1',
                'username': 'user1',
                'pid': 30281,
                'uid': 501,
                'gid': 20
            }, result)
