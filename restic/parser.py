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


def parse_key_fallback(repo, text):
    lines = text.splitlines()
    header = []
    header_range = []
    line_number = 0
    # skip other data
    while line_number < len(lines):
        if lines[line_number].strip() == 'read password from stdin':
            line_number += 1
            continue
        if lines[line_number].strip().startswith('ID'):
            break
        line_number += 1

    # read header
    while line_number < len(lines):
        if lines[line_number].strip().startswith('ID'):
            header = lines[line_number].split()
            break
        line_number += 1

    # header length
    for i, each_header in enumerate(header):
        start_pos = lines[line_number].find(each_header)
        header_range.append(start_pos)

    line_number += 1

    if len(header_range) >= 2:
        horizontal_line = '-' * (header_range[1] + 1)
    else:
        horizontal_line = '-' * 5
    # -----
    while line_number < len(lines):

        if lines[line_number].startswith(horizontal_line):
            line_number += 1
            break
        line_number += 1

    key_data = []
    while line_number < len(lines):
        single_key = Key(repo)
        line = lines[line_number]
        if line.startswith(horizontal_line):
            break
        for i, each_header in enumerate(header):
            if i == 0:
                single_key.set_attr(each_header,
                                    line[:header_range[i + 1]].strip())
            elif i == len(header_range) - 1:
                single_key.set_attr(each_header, line[header_range[i]:].strip())
            else:
                single_key.set_attr(
                    each_header,
                    line[header_range[i]:header_range[i + 1]].strip())
        key_data.append(single_key)
        line_number += 1

    # -----
    while line_number < len(lines):
        if lines[line_number].startswith(horizontal_line):
            line_number += 1
            break
        line_number += 1

    return key_data
