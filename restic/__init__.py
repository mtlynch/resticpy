from restic.internal import generate as internal_generate
from restic.internal import self_update as internal_self_update
from restic.internal import version as internal_version


def generate(*args, **kwargs):
    return internal_generate.run(*args, **kwargs)


def self_update():
    return internal_self_update.run()


def version():
    return internal_version.run()
