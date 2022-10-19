* Table of Contents
{:toc}

## Global options

| Option                   | Default Value | Notes |
|--------------------------|---------------|-------|
| `restic.binary_path`     | `'restic'`    | Specifies the location of your restic binary if it's not in the user's default path. (e.g., `/path/to/restic.exe`) |
| `restic.repository`      | `None`      | Specifies the path or URL of your restic backup repository. |
| `restic.password_file`   | `None`      | Specifies the path to the file containing your restic repository password. |

---

## backup

### Args

* `paths`: A list of paths to files or directories to back up
* `exclude_patterns`: A list of patterns of path exclusions
* `exclude_files`: A list of files containing exclude lists
* `tags`: A list of tags for the new snapshot
* `dry_run`: Set to `True` to perform just a dry run of the backup
* `host`: Set the hostname for the snapshot manually

### Returns

A dictionary with a summary of the backup result.

### Example

```python
>>> restic.backup(paths=['/data/music'],
                  exclude_patterns=['Justin Bieber*', 'Selena Gomez*'],
                  exclude_files=['bad-songs.txt'])
{
  "message_type": "summary",
  "files_new": 1,
  "files_changed": 0,
  "files_unmodified": 0,
  "dirs_new": 2,
  "dirs_changed": 0,
  "dirs_unmodified": 0,
  "data_blobs": 1,
  "tree_blobs": 3,
  "data_added": 1133,
  "total_files_processed": 1,
  "total_bytes_processed": 20,
  "total_duration": 0.211291367,
  "snapshot_id": "e17049ab"
}
```

---

## check

### Args

* `read_data`: Boolean indicating whether to read all data blobs in the repo.

### Returns

On success, returns log messages relating to checking the repo integrity.

On failure, returns None.

### Example

```python
>>> restic.check(read_data=True)
using temporary cache in /tmp/restic-check-cache-842210662
create exclusive lock for repository
load indexes
check all packs
check snapshots, trees and blobs
read all data
[0:00] 100.00%  1 / 1 snapshots

[0:00] 100.00%  2 / 2 packs

no errors were found
```

---

## copy

### Args

* `repo2`: Destination repository to copy to.
* `password_file2`: Path to file containing password for destination reposity.

### Returns

Log messages related to the copy.

### Example

```python
>>> restic.copy(repo2='/mediabackup2/', password_file2='~/pwd2.txt')
snapshot 670792c6 of [/tmp/tmp9k613t9a/mydata.txt] at 2021-03-29 00:56:31.183738563 +0000 UTC)
  copy started, this may take a while...
snapshot 3671204c saved
```

---

## forget

### Args

* `dry_run`: Set to `True` to perform just a dry run of the backup
* `group_by`: A string for grouping snapshots
* `keep_last`: An int representing the last N snapshots to keep
* `keep_hourly`: An int representing the last N hourly snapshots to keep
* `keep_daily`: An int representing the last N daily snapshots to keep
* `keep_weekly`: An int representing the last N weekly snapshots to keep
* `keep_monthly`: An int representing the last N monthly snapshots to keep
* `keep_yearly`: An int representing the last N yearly snapshots to keep
* `keep_within` A string representing a duration before which to prune relative to the latest snapshot
* `prune`: A boolean representing whether to automatically run the 'prune' command if snapshots have been removed

### Returns

A dictionary with a summary of the forget result.

### Example

```python
>>> restic.forget(prune=True, keep_daily=4)
[{
  'tags': None,
  'host': 'ecb5551395ae',
  'paths': ['/tmp/tmp6ew1vzp2/mydata.txt'],
  'keep': [{
      'time': '2021-03-16T00:10:37.015657013Z',
      'tree': '4483c2c6c1386abb9f47497cf108bab19e09c42430d32cd640a4f6f97137841f',
      'paths': ['/tmp/tmp6ew1vzp2/mydata.txt'],
      'hostname': 'ecb5551395ae',
      'username': 'demouser',
      'uid': 3434,
      'gid': 3434,
      'id': '3f6de49c6461ffd42900a204655708a3e136a3814abe298c07f27e412e2b6a43',
      'short_id': '3f6de49c'
  }],
  'remove': None,
  'reasons': [{
      'snapshot': {
          'time': '2021-03-16T00:10:37.015657013Z',
          'tree': '4483c2c6c1386abb9f47497cf108bab19e09c42430d32cd640a4f6f97137841f',
          'paths': ['/tmp/tmp6ew1vzp2/mydata.txt'],
          'hostname': 'ecb5551395ae',
          'username': 'demouser',
          'uid': 3434,
          'gid': 3434
      },
      'matches': ['daily snapshot'],
      'counters': {
          'daily': 4
      }
  }]
}]
```

---

## generate

### Args

* `bash_completion_path`: Path to bash completion file to write
* `man_directory`: Path to man directory to write to
* `zsh_completion_path`: Path to zsh completion file to write

### Returns

None

### Example

```python
>>> restic.generate(bash_completion_path='/etc/bash_completion.d/restic',
                    man_directory='/usr/local/man',
                    zsh_completion_path='/etc/zsh_completion.d/restic')
```

---

## init

Initializes a new restic repository at the current repository location.

### Args

* `copy-chunker-params`: Copy chunker parameters from the secondary repository.
* `repo2`: Secondary repository to copy chunker parameters from.

### Returns

The repository ID of the new reposityory.

### Example

```python
>>> restic.init()
'054ed643d8'
```

---

## restore

Restores a snapshot from the repository to the specified path.

### Args

* `snapshot_id`: ID of snapshot to restore (default: `latest`)
* `include`: String specifying a pattern to include, exclude everything else
* `target_dir`: String specifying output directory to place restored data

### Returns

None

### Example

```python
>>> restic.restore(target_dir='/tmp/restored1')
```

---

## self_update

Updates the restic binary in place.

### Args

None

### Returns

None

### Example

```python
>>> restic.self_update()
```

---

## snapshots

Retrieve a list of snapshots in the repo

### Args

* `group_by`: String for grouping snapshots by host, paths, tags.

### Returns

A list of dictionary objects representing each snapshot.

### Example

```python
>>> restic.snapshots(group_by='host')
[
  {
    "group_key": {
      "hostname": "ace809d23440",
      "paths": null,
      "tags": null
    },
    "snapshots": [
      {
        "gid": 3434,
        "hostname": "ace809d23440",
        "id": "bbe7f04941ed969ee940bb41dc04196027fcfb83dbdfea93c16afb2cb9f6dd81",
        "paths": [
          "/tmp/tmp6594jneh/mydata.txt"
        ],
        "short_id": "bbe7f049",
        "time": "2021-03-28T21:31:44.477122573Z",
        "tree": "f589421bafdae95f5be5eea6285074b7ddc54aa0ffd1ad606f74d1e6207d20a3",
        "uid": 3434,
        "username": "circleci"
      }
    ]
  }
]
```

---

## stats

Retrieve stats about the current restic repository.

### Args

* `mode`: Type of stats to retrieve. Can be one of `restore-size`, `files-by-contents`, `blobs-per-file` or `raw-data`.

### Returns

A dictionary of stats about the restic repository.

### Example

```python
>>> restic.stats(mode='restore-size')
{
  'total_size': 20,
  'total_file_count': 3
}
```

---

## version

Retrieves the version information about the restic binary.

### Args

None

### Returns

None

### Example

```python
>>> restic.binary_path = 'c:/restic/restic_0.12.0_windows_amd64.exe'
>>> restic.version()
{
    'architecture': 'amd64',
    'go_version': '1.15.8',
    'platform_version': 'windows',
    'restic_version': '0.12.0'
}
```
