from restic.internal import generate as internal_generate
from restic.internal import init as internal_init
from restic.internal import self_update as internal_self_update
from restic.internal import version as internal_version

binary_path = 'restic'

# Global flags
repository = None
password_file = None


def generate(*args, **kwargs):
    return internal_generate.run(_make_base_command(), *args, **kwargs)


def init(*args, **kwargs):
    return internal_init.run(_make_base_command(), *args, **kwargs)


def self_update():
    return internal_self_update.run(_make_base_command())


def version():
    return internal_version.run(_make_base_command())


def _make_base_command():
    base_command = [binary_path]

    if repository:
        base_command.extend(['--repo', repository])

    if password_file:
        base_command.extend(['--password-file', password_file])

    return base_command
