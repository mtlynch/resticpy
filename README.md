# PyRestic

[![CircleCI](https://circleci.com/gh/mtlynch/pyrestic.svg?style=svg)](https://circleci.com/gh/mtlynch/pyrestic)

## Introduction

[restic](https://github.com/restic/restic) is a backup program that is fast, efficient and secure. It supports the three major operating systems (Linux, macOS, Windows) and a few smaller ones (FreeBSD, OpenBSD).

PyRestic is a python wrapper for restic. It makes programmatic data backup in Python possible. It provides a set of object-oriented and easy-used API.

## Installation

Before using PyRestic, you need to install newest restic and add it to your ENV variable. Make sure command `restic version` works.

Next you can install PyRestic by pip:

```powershell
pip install pyrestic
```

or you can install it from source:

```powershell
git clone https://github.com/jstzwj/PyRestic.git
cd PyRestic
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
