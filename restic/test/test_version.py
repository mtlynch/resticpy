
import restic
import unittest

class TestVersion(unittest.TestCase):
    def test_version(self):
        restic_version = restic.version()
        self.assertEqual(restic_version['restic_version'], '0.9.6')
        self.assertEqual(restic_version['go_version'], '1.13.4')

if __name__ == '__main__':
    unittest.main()