import unittest
from unittest import mock

import restic
from restic.internal import cat


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
