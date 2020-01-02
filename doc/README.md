# PyRestic Documentation

## Introduction

Restic is a fast and secure backup program. In the following sections, we will present typical workflows, starting with installing, preparing a new repository, and making the first backup.



## Installation

```powershell
pip install pyrestic
```

## Preparing a new repository

The place where your backups will be saved is called a “repository”. This chapter explains how to create (“init”) such a repository. The repository can be stored locally, or on some remote server or service. We’ll first cover using a local repository; the remaining sections of this chapter cover all the other options. You can skip to the next chapter once you’ve read the relevant section here.



## Local

In order to create a repository with password `12345678` at `/srv/restic-repo`, run the following code:

```python
import restic
repo = restic.Repo.init('/srv/restic-repo', '12345678')
```

If you want to load an existing repository with password `12345678` at `/srv/restic-repo`, run the following code:

```python
import restic
repo = restic.Repo('/srv/restic-repo', '12345678')
```





## Backing up

Now we’re ready to backup some data. The contents of a directory at a specific point in time is called a “snapshot” in restic. Run the following code:

```python
import restic
repo = restic.Repo('/srv/restic-repo', '12345678')
repo.backup('setup.py')
```





## Tags for backup

Snapshots can have one or more tags, short strings which add identifying information. Just specify the tags for a snapshot one by one with `--tag`:

```python
repo.backup('setup.py', tags=['github', 'restic']):
```

The tags can later be used to keep (or forget) snapshots with the `forget` command. The command `tag` can be used to modify tags on an existing snapshot.