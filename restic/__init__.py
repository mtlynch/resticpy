from restic.internal import generate as internal_generate
from restic.internal import self_update as internal_self_update
from restic.internal import version as internal_version

binary_path = 'restic'


def generate(*args, **kwargs):
    return internal_generate.run(binary_path, *args, **kwargs)


def self_update():
    return internal_self_update.run(binary_path)


def version():
    return internal_version.run(binary_path)
