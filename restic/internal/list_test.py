import unittest
from unittest import mock

import restic
from restic.internal import cat


class ListBlobsTest(unittest.TestCase):

    @mock.patch.object(cat.command_executor, 'execute')
    def test_list_blobs(self, mock_execute):
        mock_execute.return_value = """
data 0e95fab71e38a88ea95bb2faa2e66d9ba3d5651fae6eed43fb252919191fc976
data c65cf635b45712759412f1597125f96605863bdc56fc5b50a8052f2426130866
index 98f8a7a6d05be57dbc834fd764ab701ae46828ab00c4272464b52f831a158a82
""".strip()

        result = restic.list.blobs()

        mock_execute.assert_called_with([
            'restic',
            '--json',
            'list',
            'blobs',
        ])

        # Ignore complaint about too long of a line.
        # pylint: disable=C0301
        self.assertEqual([{
            'type':
                'data',
            'id':
                '0e95fab71e38a88ea95bb2faa2e66d9ba3d5651fae6eed43fb252919191fc976'
        }, {
            'type':
                'data',
            'id':
                'c65cf635b45712759412f1597125f96605863bdc56fc5b50a8052f2426130866'
        }, {
            'type':
                'index',
            'id':
                '98f8a7a6d05be57dbc834fd764ab701ae46828ab00c4272464b52f831a158a82'
        }], result)


class ListPacksTest(unittest.TestCase):

    @mock.patch.object(cat.command_executor, 'execute')
    def test_list_packs(self, mock_execute):
        mock_execute.return_value = """
d9b0b8720480174d1ebf396fbc15e6bed3c6477fa34c4c70885d74788a8bd7fe
a17b22f9585982c46396d300c0e856a487a92b5fc5ad0f080bf6d7016998fd48
""".strip()

        result = restic.list.packs()

        mock_execute.assert_called_with([
            'restic',
            '--json',
            'list',
            'packs',
        ])

        self.assertEqual([
            'd9b0b8720480174d1ebf396fbc15e6bed3c6477fa34c4c70885d74788a8bd7fe',
            'a17b22f9585982c46396d300c0e856a487a92b5fc5ad0f080bf6d7016998fd48'
        ], result)


class ListIndexTest(unittest.TestCase):

    @mock.patch.object(cat.command_executor, 'execute')
    def test_list_index(self, mock_execute):
        mock_execute.return_value = """
0d1c5b5b2019b697b81b82d9b2a0741c9b2f9434d8d1d8f7205821cd5a862440
b2059a9cb836a56aafa44c32fc751aa50966cdedca02b3465daa06487bb23ac8
""".strip()

        result = restic.list.index()

        mock_execute.assert_called_with([
            'restic',
            '--json',
            'list',
            'index',
        ])

        self.assertEqual([
            '0d1c5b5b2019b697b81b82d9b2a0741c9b2f9434d8d1d8f7205821cd5a862440',
            'b2059a9cb836a56aafa44c32fc751aa50966cdedca02b3465daa06487bb23ac8'
        ], result)


class ListSnapshotsTest(unittest.TestCase):

    @mock.patch.object(cat.command_executor, 'execute')
    def test_list_snapshots(self, mock_execute):
        mock_execute.return_value = """
41cb1a6fc558b9b18de18a2cab869cfca046afe412bd2c181f7dd20f599ed31c
f4a3b52cc9fbea3d7762166a5005983850d46d7417dcd25d7aed6e794305c3bb
""".strip()

        result = restic.list.snapshots()

        mock_execute.assert_called_with([
            'restic',
            '--json',
            'list',
            'snapshots',
        ])

        self.assertEqual([
            '41cb1a6fc558b9b18de18a2cab869cfca046afe412bd2c181f7dd20f599ed31c',
            'f4a3b52cc9fbea3d7762166a5005983850d46d7417dcd25d7aed6e794305c3bb'
        ], result)


class ListKeysTest(unittest.TestCase):

    @mock.patch.object(cat.command_executor, 'execute')
    def test_list_keys(self, mock_execute):
        mock_execute.return_value = """
0d9c66857c444c6a42779bb0369f686a33f1df55254be9dd4d706a88a3e0d8b5
""".strip()

        result = restic.list.keys()

        mock_execute.assert_called_with([
            'restic',
            '--json',
            'list',
            'keys',
        ])

        self.assertEqual([
            '0d9c66857c444c6a42779bb0369f686a33f1df55254be9dd4d706a88a3e0d8b5',
        ], result)


class ListLocksTest(unittest.TestCase):

    @mock.patch.object(cat.command_executor, 'execute')
    def test_list_locks(self, mock_execute):
        mock_execute.return_value = """
e3a938731770e741fe34fb43fc26ff3088e77ba3ebb0792181a72e0fdb5fbe0d
2bb62a61dfd1853f845d9baf4330f1af57172516260ccb45989569f459f73753
""".strip()

        result = restic.list.locks()

        mock_execute.assert_called_with([
            'restic',
            '--json',
            'list',
            'locks',
        ])

        self.assertEqual([
            'e3a938731770e741fe34fb43fc26ff3088e77ba3ebb0792181a72e0fdb5fbe0d',
            '2bb62a61dfd1853f845d9baf4330f1af57172516260ccb45989569f459f73753'
        ], result)
