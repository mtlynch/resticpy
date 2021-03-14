import unittest
from unittest import mock

import restic
from restic.internal import generate


class ResticTest(unittest.TestCase):

    @mock.patch.object(generate.command_executor, 'execute')
    def test_can_change_restic_binary_path(self, mock_execute):
        restic.binary_path = '/dummy/path/to/restic-binary'
        restic.generate()
        mock_execute.assert_called_with(
            ['/dummy/path/to/restic-binary', 'generate'])
