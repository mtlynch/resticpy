# resticpy

[![PyPI](https://img.shields.io/pypi/v/resticpy)](https://pypi.org/project/resticpy/)
[![CircleCI](https://circleci.com/gh/mtlynch/resticpy.svg?style=svg)](https://circleci.com/gh/mtlynch/resticpy)
[![Coverage Status](https://coveralls.io/repos/github/mtlynch/resticpy/badge.svg?branch=master)](https://coveralls.io/github/mtlynch/resticpy?branch=master)
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](LICENSE)

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

### Create a password file

```bash
printf "mysecretpass" > password.txt
```

### Initialize a repository and back up a file

```python
import restic

restic.repository = '/tmp/backup1'
restic.password_file = 'password.txt'

restic.init()
restic.backup(paths=['some-file.txt'])
```

### Restore a snapshot

```python
import restic

restic.repository = '/tmp/backup1'
restic.password_file = 'password.txt'

restic.restore(snapshot_id='latest', target_dir='~/restored')
```

## API Documentation

<https://mtlynch.github.io/resticpy/>

## Example

I personally use this library for my backups. I've published my backup script at [mtlynch/mtlynch-backup](https://github.com/mtlynch/mtlynch-backup).

## Compatibility

resticpy is tested against [restic 0.16.2](https://github.com/restic/restic/releases/tag/v0.16.2).

## resticpy's scope and future

resticpy is maintained by [Michael Lynch](https://mtlynch.io) as a hobby project.

resticpy is **not** meant to achieve feature parity with restic. It is meant to cover a small subset of the most useful features of restic.

Due to time limitations, I keep resticpy's scope limited to only the features that fit into my workflows.

### Feature requests

I don't fulfill feature requests for resticpy. You are welcome to file a feature request for a third-party contributor to take on.

### Pull requests

I accept pull requests when they are:

- Documented
- Tested
- Small

I don't accept pull requests for features that look like they'll be a large maintenance burden.

## Acknowledgments

This project is forked from [jstzwj/PyRestic](https://github.com/jstzwj/PyRestic).
