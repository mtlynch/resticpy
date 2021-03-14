import json

from restic.key import Key
from restic.snapshot import Snapshot


def parse_key(repo, text):
    ret_object = json.loads(text)
    keys = []
    for each_key in ret_object:
        single_key = Key(repo)
        single_key.set_current(each_key['current'])
        single_key.set_id(each_key['id'])
        single_key.set_user(each_key['userName'])
        single_key.set_host(each_key['hostName'])
        single_key.set_created(each_key['created'])
        keys.append(single_key)
    return keys


def parse_stats(repo, text):
    ret_object = json.loads(text)
    return ret_object


def parse_snapshots(repo, text):
    ret_object = json.loads(text)
    snapshots = []
    for each_snapshot in ret_object:
        single_snapshot = Snapshot(repo)
        single_snapshot.set_id(each_snapshot['id'])
        single_snapshot.set_host(each_snapshot['username'])
        single_snapshot.set_paths(each_snapshot['paths'])
        single_snapshot.set_time(each_snapshot['time'])
        if 'parent' in each_snapshot.keys():
            single_snapshot.set_parent(each_snapshot['parent'])
        if 'origin' in each_snapshot.keys():
            single_snapshot.set_origin(each_snapshot['origin'])
        snapshots.append(single_snapshot)
    return snapshots
