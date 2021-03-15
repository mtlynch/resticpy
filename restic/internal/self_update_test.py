import unittest
from unittest import mock

import restic
from restic.internal import self_update


class SelfUpdateTest(unittest.TestCase):

    @mock.patch.object(self_update.command_executor, 'execute')
    def test_self_update(self, mock_execute):
        restic.self_update()
        mock_execute.assert_called_with(['restic', '--json', 'self-update'])
