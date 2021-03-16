import unittest
from unittest import mock

import restic
from restic.internal import init

# Ignore suggestions to turn methods into functions.
# pylint: disable=R0201


class InitTest(unittest.TestCase):

    @mock.patch.object(init.command_executor, 'execute')
    def test_init_with_no_parameters(self, mock_execute):
        mock_execute.return_value = (
            'created restic repository 054ed643d8 at /media/backup1')

        repository_id = restic.init()

        self.assertEqual('054ed643d8', repository_id)
        mock_execute.assert_called_with(['restic', '--json', 'init'])
