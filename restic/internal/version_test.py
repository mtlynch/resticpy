import unittest
from unittest import mock

import restic
from restic.internal import version


class VersionTest(unittest.TestCase):

    @mock.patch.object(version.command_executor, 'execute')
    def test_version(self, mock_execute):
        mock_execute.return_value = (
            'restic 0.16.2 compiled with go1.20.6 on windows/amd64')

        self.assertEqual(
            {
                'architecture': 'amd64',
                'go_version': '1.20.6',
                'platform_version': 'windows',
                'restic_version': '0.16.2'
            }, restic.version())

        mock_execute.assert_called_with(['restic', '--json', 'version'])
