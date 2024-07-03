import json

from restic.internal import command_executor


def run(restic_base_command,
        snapshot_id=None,
        group_by=None,
        tags=None,
        path=None,
        host=None):
    cmd = restic_base_command + ['snapshots']

    if snapshot_id:
        cmd.append(snapshot_id)

    if group_by:
        cmd.extend(['--group-by', group_by])

    if tags:
        cmd.extend(['--tag', ','.join(tags)])

    if path:
        cmd.extend(['--path', path])

    if host:
        cmd.extend(['--host', host])

    return json.loads(command_executor.execute(cmd))
