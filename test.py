import restic

if __name__ == "__main__":
    print(restic.version())
    # repo = restic.Repo.init('repos_test/test_repo', '12345678')
    repo = restic.Repo('repos_test/test_repo', '12345678')
    repo.backup('setup.py')
    print(repo.check())
    snapshots = repo.snapshots()
    print('snapshots begin')
    for each_snapshot in snapshots:
        print(each_snapshot)
    print('snapshots end')
    # snapshots[0].restore('repos_test/restore_repo')

    print('add tag')
    snapshots[0].add_tag('ok')
    print(snapshots[0])
    snapshots[0].remove_tag('ok')
    print(snapshots[0])

    # repo.mount('/mnt/restic')
    