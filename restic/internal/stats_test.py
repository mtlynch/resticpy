import unittest
from unittest import mock

import restic
from restic.internal import stats


class SelfUpdateTest(unittest.TestCase):

    @mock.patch.object(stats.command_executor, 'execute')
    def test_stats(self, mock_execute):
        restic.stats()
        mock_execute.assert_called_with(['restic', '--json', 'stats'])
