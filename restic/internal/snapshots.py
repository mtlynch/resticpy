import json

from restic.internal import command_executor


def run(
    restic_base_command,
    snapshot_id=None,
    group_by=None,
    tags=None,
    path=None,
    host=None,
):
    cmd = restic_base_command + ["snapshots"]

    if snapshot_id:
        cmd.append(snapshot_id)

    # Explicitly check for None, as empty lists and None have different
    # meanings.
    if group_by is not None:
        cmd.extend(["--group-by", ",".join(group_by)])

    if tags:
        cmd.extend(["--tag", ",".join(tags)])

    if path:
        cmd.extend(["--path", path])

    if host:
        cmd.extend(["--host", host])

    return json.loads(command_executor.execute(cmd))
