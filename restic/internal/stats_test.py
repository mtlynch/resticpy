import unittest
from unittest import mock

import restic
from restic.internal import stats

# Ignore suggestions to turn methods into functions.
# pylint: disable=R0201


class SelfUpdateTest(unittest.TestCase):

    @mock.patch.object(stats.command_executor, 'execute')
    def test_stats(self, mock_execute):
        mock_execute.return_value = """{
            "total_size": 20,
            "total_file_count": 3
            }
            """
        restic.stats()
        mock_execute.assert_called_with(['restic', '--json', 'stats'])
