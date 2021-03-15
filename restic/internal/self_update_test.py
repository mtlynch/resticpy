import unittest
from unittest import mock

import restic
from restic.internal import self_update

# Ignore suggestions to turn methods into functions.
# pylint: disable=R0201


class SelfUpdateTest(unittest.TestCase):

    @mock.patch.object(self_update.command_executor, 'execute')
    def test_self_update(self, mock_execute):
        restic.self_update()
        mock_execute.assert_called_with(['restic', '--json', 'self-update'])
