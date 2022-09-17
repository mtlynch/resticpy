import unittest
from unittest import mock

import restic
from restic.internal import init


class InitTest(unittest.TestCase):

    @mock.patch.object(init.command_executor, 'execute')
    def test_unlock_with_no_parameters(self, mock_execute):
        restic.unlock()
        mock_execute.assert_called_with(['restic', '--json', 'unlock'])
