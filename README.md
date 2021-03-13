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

Once you have installed restic and PyRestic, you can create a repository:

```python
import restic
repo = restic.Repo('/srv/restic-repo', '12345678')
```

The new repository is located in `/srv/restic-repo` with password `12345678`

Then try to backup some files:

```python
import restic
repo = restic.Repo('/srv/restic-repo', '12345678')
repo.backup('setup.py')
```

## Acknowledgments

This project is forked from [jstzwj/PyRestic](https://github.com/jstzwj/PyRestic).
