from restic.internal import self_update as internal_self_update
from restic.internal import version as internal_version


def self_update():
    return internal_self_update.run()


def version():
    return internal_version.run()
