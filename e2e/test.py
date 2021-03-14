#!/usr/bin/env python3

import os.path
import tempfile

import restic

PASSWORD = 'mysecretpass'
PASSWORD_FILE = tempfile.NamedTemporaryFile()
PASSWORD_FILE.write(PASSWORD.encode('utf-8'))
PASSWORD_FILE.flush()

DUMMY_SOURCE_DIR = tempfile.mkdtemp()
DUMMY_DATA_PATH = os.path.join(DUMMY_SOURCE_DIR, 'mydata.txt')
with open(DUMMY_DATA_PATH, 'w') as dummy_data_file:
    dummy_data_file.write('some data to back up')

restic.binary_path = 'restic'
restic.repository = tempfile.mkdtemp()
restic.password_file = PASSWORD_FILE.name

print('Initializing repository')
restic.init()

print('Backing up %s' % DUMMY_DATA_PATH)
restic.backup(paths=[DUMMY_DATA_PATH])

RESTORE_DIR = tempfile.mkdtemp()
print('Restoring to %s' % RESTORE_DIR)
restic.restore(snapshot_id='latest', target_dir=RESTORE_DIR)

RESTORED_DATA_PATH = os.path.join(RESTORE_DIR, DUMMY_DATA_PATH)
if not os.path.exists(RESTORED_DATA_PATH):
    print('Expected to find %s' % RESTORED_DATA_PATH)
    exit(1)
RESTORED_DATA = open(RESTORED_DATA_PATH).read()
if RESTORED_DATA != 'some data to back up':
    print('Expected to restored file to contain %s (got %s)' %
          ('some data to back up', RESTORED_DATA))
    exit(1)

print('End-to-end test succeeded!')
