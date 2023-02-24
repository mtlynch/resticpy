from restic.internal import backup as internal_backup
from restic.internal import cat as internal_cat
from restic.internal import check as internal_check
from restic.internal import copy as internal_copy
from restic.internal import find as internal_find
from restic.internal import forget as internal_forget
from restic.internal import generate as internal_generate
from restic.internal import init as internal_init
from restic.internal import key as internal_key
from restic.internal import list as internal_list
from restic.internal import restore as internal_restore
from restic.internal import rewrite as internal_rewrite
from restic.internal import self_update as internal_self_update
from restic.internal import snapshots as internal_snapshots
from restic.internal import stats as internal_stats
from restic.internal import unlock as internal_unlock
from restic.internal import version as internal_version

# Ignore warnings about naming of globals.
# pylint: disable=C0103
binary_path = 'restic'

# Global flags
# Ignore warnings about naming of globals.
# pylint: disable=C0103
repository = None
password_file = None
use_cache = True


def backup(*args, **kwargs):
    return internal_backup.run(_make_base_command(), *args, **kwargs)


def check(*args, **kwargs):
    return internal_check.run(_make_base_command(), *args, **kwargs)


def copy(*args, **kwargs):
    return internal_copy.run(_make_base_command(), *args, **kwargs)


def find(*args, **kwargs):
    return internal_find.run(_make_base_command(), *args, **kwargs)


def forget(*args, **kwargs):
    return internal_forget.run(_make_base_command(), *args, **kwargs)


def generate(*args, **kwargs):
    return internal_generate.run(_make_base_command(), *args, **kwargs)


def init(*args, **kwargs):
    return internal_init.run(_make_base_command(), *args, **kwargs)


def restore(*args, **kwargs):
    return internal_restore.run(_make_base_command(), *args, **kwargs)


def rewrite(*args, **kwargs):
    return internal_rewrite.run(_make_base_command(), *args, **kwargs)


def self_update():
    return internal_self_update.run(_make_base_command())


def snapshots(*args, **kwargs):
    return internal_snapshots.run(_make_base_command(), *args, **kwargs)


def stats(*args, **kwargs):
    return internal_stats.run(_make_base_command(), *args, **kwargs)


def unlock():
    return internal_unlock.run(_make_base_command())


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

    if not use_cache:
        base_command.extend(['--no-cache'])

    return base_command


cat = internal_cat.Cat(_make_base_command)
key = internal_key.Key(_make_base_command)
list = internal_list.List(_make_base_command)  # pylint: disable=W0622
