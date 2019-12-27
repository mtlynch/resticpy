
import restic
import unittest
import shutil

class TestInit(unittest.TestCase):
    def test_initlocal(self):
        repo = restic.Repo.init('repos_test/test_repo', '12345678')
        shutil.rmtree('repos_test/test_repo')

if __name__ == '__main__':
    unittest.main()