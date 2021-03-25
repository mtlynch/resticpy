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

TODO

### Example

```python
>>> restic.check(read_data=True)
```

---

## forget

### Args

* `prune`: A boolean representing whether to automatically run the 'prune' command if snapshots have been removed
* `keep_daily`: An int representing the last N daily snapshots to keep

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

None

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
