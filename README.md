# pyrestic

[![CircleCI](https://circleci.com/gh/mtlynch/pyrestic.svg?style=svg)](https://circleci.com/gh/mtlynch/pyrestic) [![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](LICENSE)

## Overview

Minimal Python wrapper around the [restic](https://restic.readthedocs.io/) backup command-line interface.

## Installation

```bash
git clone https://github.com/mtlynch/pyrestic.git
cd pyrestic
pip install .
```

## Quick start

Back up a file:

```python
import restic
repo = restic.Repo(path='/srv/restic-repo', password='12345678')
repo.backup('file-to-backup.txt')
```

## API Documentation

Coming soon.

## Acknowledgments

This project is forked from [jstzwj/PyRestic](https://github.com/jstzwj/PyRestic).
