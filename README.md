# resticpy

[![CircleCI](https://circleci.com/gh/mtlynch/resticpy.svg?style=svg)](https://circleci.com/gh/mtlynch/resticpy) [![Coverage Status](https://coveralls.io/repos/github/mtlynch/resticpy/badge.svg?branch=master)](https://coveralls.io/github/mtlynch/resticpy?branch=master) [![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](LICENSE)

## Overview

Minimal Python wrapper around the [restic](https://restic.readthedocs.io/) backup command-line interface.

## Installation

### From pip

```bash
pip install resticpy
```

### From source

```bash
git clone https://github.com/mtlynch/resticpy.git
cd resticpy
pip install .
```

## Quick start

Initialize a repository and back up a file:

```python
import restic

PASSWORD = 'mysecretpass'
PASSWORD_FILE_PATH = 'secret.txt'

with open(PASSWORD_FILE_PATH, 'w') as password_file:
  password_file.write(PASSWORD)

restic.repository = '/tmp/backup1'
restic.password_file = PASSWORD_FILE_PATH

restic.init()
restic.backup('some-file.txt')
```

## API Documentation

Coming soon.

## Acknowledgments

This project is forked from [jstzwj/PyRestic](https://github.com/jstzwj/PyRestic).
