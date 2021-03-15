# resticpy API

## `backup`

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

## `forget`

TODO(mtlynch): Write this.

## `generate`

TODO(mtlynch): Write this.

## `init`

TODO(mtlynch): Write this.

## restore

TODO(mtlynch): Write this.

## `self_update`

TODO(mtlynch): Write this.

## `stats`

TODO(mtlynch): Write this.

## `version`

TODO(mtlynch): Write this.
