from restic.internal import backup as internal_backup
from restic.internal import forget as internal_forget
from restic.internal import generate as internal_generate
from restic.internal import init as internal_init
from restic.internal import restore as internal_restore
from restic.internal import self_update as internal_self_update
from restic.internal import stats as internal_stats
from restic.internal import version as internal_version

# Ignore warnings about naming of globals.
# pylint: disable=C0103
binary_path = 'restic'

# Global flags
# Ignore warnings about naming of globals.
# pylint: disable=C0103
repository = None
password_file = None


def backup(*args, **kwargs):
    return internal_backup.run(_make_base_command(), *args, **kwargs)


def forget(*args, **kwargs):
    return internal_forget.run(_make_base_command(), *args, **kwargs)


def generate(*args, **kwargs):
    return internal_generate.run(_make_base_command(), *args, **kwargs)


def init(*args, **kwargs):
    return internal_init.run(_make_base_command(), *args, **kwargs)


def restore(*args, **kwargs):
    return internal_restore.run(_make_base_command(), *args, **kwargs)


def self_update():
    return internal_self_update.run(_make_base_command())


def stats():
    return internal_stats.run(_make_base_command())


def version():
    return internal_version.run(_make_base_command())


def _make_base_command():
    base_command = [binary_path]

    # Always add the JSON flag so we get back results in JSON.
    base_command.extend(['--json'])

    if repository:
        base_command.extend(['--repo', repository])

    if password_file:
        base_command.extend(['--password-file', password_file])

    return base_command
