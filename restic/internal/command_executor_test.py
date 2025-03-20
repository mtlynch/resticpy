from unittest import TestCase

from restic.internal import command_executor
from restic.internal.command_executor import _strip_terminal_characters
from restic.errors import NoResticBinaryError, ResticFailedError

class Test(TestCase):
    def test__strip_terminal_characters(self):
        stripped = _strip_terminal_characters(b'\x1b[2K Some Content\n')
        self.assertEqual(b' Some Content\n', stripped)

        stripped = _strip_terminal_characters(b'\x1b[2K2K2\n')
        self.assertEqual(b'2K2\n', stripped)

        stripped = _strip_terminal_characters(b'\x1b[2')
        self.assertEqual(b'\x1b[2', stripped)

    def test__raises_error_on_nonexisting_binary(self):
        with self.assertRaises(NoResticBinaryError):
            command_executor.execute(['a_nonexisting_binary'])

    def test__raises_error_on_failing_command(self):
        with self.assertRaises(ResticFailedError):
            command_executor.execute(['restic','a_non_existing_cli_argument'])

    def test__async_io(self):
        output = []

        # test helper outputs numbers from 0 to 9. Even numbers to stdout,
        # odd numbers to stderr. If they are received in order, the functions
        # are called asynchronously
        command_executor.execute(
            cmd=['python3', 'command_executor_test_helper.py'],
            on_stdout=lambda x: output.append(f'stdout: {x}'),
            on_stderr=lambda x: output.append(f'stderr: {x}'))

        expected = []
        for i in range(10):
            pipestr = 'stderr'
            if i % 2 == 0:
                pipestr = 'stdout'
            expected.append(pipestr + f': {i}')

        self.assertEqual(10, len(output))
        for i in range(10):
            self.assertEqual(expected[i], output[i])
