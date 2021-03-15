import unittest
from unittest import mock

import restic
from restic.internal import version


class VersionTest(unittest.TestCase):

    @mock.patch.object(version.command_executor, 'execute')
    def test_version(self, mock_execute):
        mock_execute.return_value = (
            'restic 0.12.0 compiled with go1.15.8 on windows/amd64')

        self.assertEqual(
            {
                'architecture': 'amd64',
                'go_version': '1.15.8',
                'platform_version': 'windows',
                'restic_version': '0.12.0'
            }, restic.version())

        mock_execute.assert_called_with(['restic', '--json', 'version'])
