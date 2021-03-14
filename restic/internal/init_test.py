import unittest
from unittest import mock

import restic
from restic.internal import init


class initTest(unittest.TestCase):

    @mock.patch.object(init.command_executor, 'execute')
    def test_init_with_no_parameters(self, mock_execute):
        restic.init()
        mock_execute.assert_called_with(['restic', 'init'])
