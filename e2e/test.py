#!/usr/bin/env python3

import tempfile

import restic

PASSWORD = 'mysecretpass'
PASSWORD_FILE = tempfile.NamedTemporaryFile()
PASSWORD_FILE.write(PASSWORD.encode('utf-8'))
PASSWORD_FILE.flush()

restic.binary_path = 'restic'
restic.repository = tempfile.mkdtemp()
restic.password_file = PASSWORD_FILE.name

restic.init()
