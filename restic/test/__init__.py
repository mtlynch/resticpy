
import unittest

from restic.test.test_version import TestVersion
from restic.test.test_init import TestInit
from restic.test.test_backup import TestBackup

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestVersion('test_version'))
    suite.addTest(TestInit('test_initlocal'))
    suite.addTest(TestBackup('test_backup_file'))
    
    return suite


def test_all():
    runner = unittest.TextTestRunner()
    runner.run(suite())

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())