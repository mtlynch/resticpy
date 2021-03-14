import unittest
from unittest import mock

import restic
from restic.internal import generate


class GenerateTest(unittest.TestCase):

    @mock.patch.object(generate.command_executor, 'execute')
    def test_generate_with_no_parameters(self, mock_execute):
        restic.generate()
        mock_execute.assert_called_with(['restic', 'generate'])

    @mock.patch.object(generate.command_executor, 'execute')
    def test_generate_bash(self, mock_execute):
        restic.generate(bash_completion_path='/tmp/dummy.path')
        mock_execute.assert_called_with(
            ['restic', 'generate', '--bash-completion', '/tmp/dummy.path'])

    @mock.patch.object(generate.command_executor, 'execute')
    def test_generate_man(self, mock_execute):
        restic.generate(man_directory='/tmp/man-dir')
        mock_execute.assert_called_with(
            ['restic', 'generate', '--man', '/tmp/man-dir'])

    @mock.patch.object(generate.command_executor, 'execute')
    def test_generate_zsh(self, mock_execute):
        restic.generate(zsh_completion_path='/tmp/dummy.path')
        mock_execute.assert_called_with(
            ['restic', 'generate', '--zsh-completion', '/tmp/dummy.path'])

    @mock.patch.object(generate.command_executor, 'execute')
    def test_generate_all(self, mock_execute):
        restic.generate(bash_completion_path='/tmp/dummy.path',
                        man_directory='/tmp/man-dir',
                        zsh_completion_path='/tmp/dummy.path')
        mock_execute.assert_called_with([
            'restic', 'generate', '--bash-completion', '/tmp/dummy.path',
            '--man', '/tmp/man-dir', '--zsh-completion', '/tmp/dummy.path'
        ])
