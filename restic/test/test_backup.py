
import restic
import unittest
import shutil

class TestBackup(unittest.TestCase):
    def test_backup_file(self):
        repo = restic.Repo.init('repos_test/test_repo', '12345678')
        try:
            repo.backup('setup.py')
            snapshots = repo.snapshots()
            self.assertEqual(len(snapshots), 1)
            self.assertTrue(snapshots[0].get_paths()[0].endswith('setup.py'))
        except Exception as e:
            shutil.rmtree('repos_test/test_repo')
            raise e
        shutil.rmtree('repos_test/test_repo')

if __name__ == '__main__':
    unittest.main()