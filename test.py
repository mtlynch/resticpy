import restic

if __name__ == "__main__":
    print(restic.version())
    # repo = restic.Repo.init('test_repo', '12345678')
    repo = restic.Repo('test_repo', '12345678')
    repo.backup('setup.py')
    print(repo.check())
    print(repo.snapshots())
    repo.mount('/mnt/restic')
    