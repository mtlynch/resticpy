from restic.repo import Repo, version
from restic.snapshot import Snapshot


from restic.test import test_all


# check restic version
restic_version = version()
restic_bin = 'restic'