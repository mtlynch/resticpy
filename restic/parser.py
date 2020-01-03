import json

from restic.snapshot import Snapshot
from restic.key import Key


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

    line_number+=1

    if len(header_range) >= 2:
        horizontal_line = '-'*(header_range[1] + 1)
    else:
        horizontal_line = '-'*5
    # -----
    while line_number < len(lines):
        
        if lines[line_number].startswith(horizontal_line):
            line_number+=1
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
                single_key.set_attr(each_header, line[:header_range[i+1]].strip())
            elif i == len(header_range) - 1:
                single_key.set_attr(each_header, line[header_range[i]:].strip())
            else:
                single_key.set_attr(each_header, line[header_range[i]:header_range[i+1]].strip())
        key_data.append(single_key)
        line_number += 1

    # -----
    while line_number < len(lines):
        if lines[line_number].startswith(horizontal_line):
            line_number+=1
            break
        line_number += 1

    return key_data

'''
Do not use it, it does not support mutlit paths in a snapshot
'''
def parse_snapshots_fallback(repo, text):
    # to header
    lines = text.splitlines()
    header = []
    header_range = []
    line_number = 0
    # skip other data
    while line_number < len(lines):
        if lines[line_number].strip() == 'read password from stdin':
            line_number += 1
            continue
        if lines[line_number].startswith('ID'):
            break
        line_number += 1
    # read header
    while line_number < len(lines):
        if lines[line_number].startswith('ID'):
            header = lines[line_number].split()
            break
        line_number += 1

    # header length
    for i, each_header in enumerate(header):
        start_pos = lines[line_number].find(each_header)
        header_range.append(start_pos)

    line_number+=1

    if len(header_range) >= 2:
        horizontal_line = '-'*(header_range[1] + 1)
    else:
        horizontal_line = '-'*5
    # -----
    while line_number < len(lines):
        
        if lines[line_number].startswith(horizontal_line):
            line_number+=1
            break
        line_number += 1

    snapshot_data = []
    while line_number < len(lines):
        snapshot = Snapshot(repo)
        line = lines[line_number]
        if line.startswith(horizontal_line):
            break
        for i, each_header in enumerate(header):
            value = None
            
            if i == 0:
                value = line[:header_range[i+1]].strip()
            elif i == len(header_range) - 1:
                value = line[header_range[i]:].strip()
            else:
                value = line[header_range[i]:header_range[i+1]].strip()
            # TODO: multiline paths
            snapshot.set_attr(each_header, value)
        snapshot_data.append(snapshot)
        line_number += 1

    # -----
    while line_number < len(lines):
        if lines[line_number].startswith(horizontal_line):
            line_number+=1
            break
        line_number += 1

    # snapshots number
    snapshots_number = 0
    if line_number < len(lines) and lines[line_number].endswith('snapshots'):
        splits_line = lines[line_number].split()
        snapshots_number = int(splits_line[0])

    # check if snapshots number is correct
    if len(snapshot_data) != snapshots_number:
        raise RuntimeError('Snapshots read failure')

    return snapshot_data

def parse_stats_fallback(repo, text):
    lines = text.splitlines()
    line_number = 0

    # scanning
    while line_number < len(lines):
        if lines[line_number].strip() == 'scanning...':
            line_number += 1
            break
        line_number += 1

    # Stats
    while line_number < len(lines):
        if lines[line_number].strip() == 'Stats for all snapshots in restore-size mode:':
            line_number += 1
            break
        line_number += 1

    # file count and total size
    file_count = '0'
    total_size = '0 B'
    while line_number < len(lines):
        if lines[line_number].strip().startswith('Total File Count:'):
            line = lines[line_number].split(':', 1)
            file_count = line[1].strip()
        elif lines[line_number].strip().startswith('Total Size:'):
            line = lines[line_number].split(':', 1)
            total_size = line[1].strip()
        line_number += 1

    return {
        'total_file_count': file_count,
        'total_size': total_size
    }
