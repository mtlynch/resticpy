import restic

if __name__ == "__main__":
    # repo = restic.Repo.init('test_repo', '12345678')
    repo = restic.Repo('test_repo', '12345678')
    # repo.backup('setup.py')
    print(repo.snapshots())
    