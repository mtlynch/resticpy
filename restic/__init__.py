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

PARAM_NAME = 'repocfg'


class RepoCfg:

    # pylint: disable=W0621
    def __init__(self, repository=None, password_file=None, use_cache=True):
        self.password_file = password_file
        self.repository = repository
        self.use_cache = use_cache


def backup(*args, **kwargs):
    cfg = kwargs.get(PARAM_NAME)
    return internal_backup.run(_make_base_command(cfg), *args,
                               **_strip_cfg(**kwargs))


def check(*args, **kwargs):
    cfg = kwargs.get(PARAM_NAME)
    return internal_check.run(_make_base_command(cfg), *args,
                              **_strip_cfg(**kwargs))


def copy(*args, **kwargs):
    cfg = kwargs.get(PARAM_NAME)
    return internal_copy.run(_make_base_command(cfg), *args,
                             **_strip_cfg(**kwargs))


def find(*args, **kwargs):
    cfg = kwargs.get(PARAM_NAME)
    return internal_find.run(_make_base_command(cfg), *args,
                             **_strip_cfg(**kwargs))


def forget(*args, **kwargs):
    cfg = kwargs.get(PARAM_NAME)
    return internal_forget.run(_make_base_command(cfg), *args,
                               **_strip_cfg(**kwargs))


def generate(*args, **kwargs):
    cfg = kwargs.get(PARAM_NAME)
    return internal_generate.run(_make_base_command(cfg), *args,
                                 **_strip_cfg(**kwargs))


def init(*args, **kwargs):
    cfg = kwargs.get(PARAM_NAME)
    return internal_init.run(_make_base_command(cfg), *args,
                             **_strip_cfg(**kwargs))


def restore(*args, **kwargs):
    return internal_restore.run(_make_base_command(kwargs.get(PARAM_NAME)),
                                *args, **_strip_cfg(**kwargs))


def rewrite(*args, **kwargs):
    cfg = kwargs.get(PARAM_NAME)
    return internal_rewrite.run(_make_base_command(cfg), *args,
                                **_strip_cfg(**kwargs))


def self_update():
    return internal_self_update.run(_make_base_command())


def snapshots(*args, **kwargs):
    cfg = kwargs.get(PARAM_NAME)
    return internal_snapshots.run(_make_base_command(cfg), *args,
                                  **_strip_cfg(**kwargs))


def stats(*args, **kwargs):
    cfg = kwargs.get(PARAM_NAME)
    return internal_stats.run(_make_base_command(cfg), *args,
                              **_strip_cfg(**kwargs))


def unlock(**kwargs):
    cfg = kwargs.get(PARAM_NAME)
    return internal_unlock.run(_make_base_command(cfg))


def version():
    return internal_version.run(_make_base_command())


def _strip_cfg(**kwargs):
    if PARAM_NAME in kwargs:
        result = kwargs.copy()
        result.pop(PARAM_NAME)
        return result
    return kwargs


def _make_base_command(repocfg: RepoCfg = None):
    base_command = [binary_path]

    # Always add the JSON flag so we get back results in JSON.
    base_command.extend(['--json'])

    cfg = repocfg or RepoCfg(repository, password_file, use_cache)

    if cfg.repository:
        base_command.extend(['--repo', cfg.repository])

    if cfg.password_file:
        base_command.extend(['--password-file', cfg.password_file])

    if not cfg.use_cache:
        base_command.extend(['--no-cache'])

    return base_command


cat = internal_cat.Cat(_make_base_command)
key = internal_key.Key(_make_base_command)
list = internal_list.List(_make_base_command)  # pylint: disable=W0622
