#!/usr/bin/env python3

import tempfile

import restic

PASSWORD = 'mysecretpass'
PASSWORD_FILE = tempfile.NamedTemporaryFile()
PASSWORD_FILE.write(PASSWORD.encode('utf-8'))
PASSWORD_FILE.flush()

restic.binary_path = '/tmp/tmp.RF74RFsHHk/restic_0.12.0_linux_amd64'
restic.repository = tempfile.mkdtemp()
restic.password_file = PASSWORD_FILE.name

restic.init()
