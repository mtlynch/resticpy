# resticpy

Just a test

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

resticpy is tested against [restic 0.12.0](https://github.com/restic/restic/releases/tag/v0.12.0).

## Acknowledgments

This project is forked from [jstzwj/PyRestic](https://github.com/jstzwj/PyRestic).
