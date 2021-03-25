import restic.errors
from restic.internal import command_executor


def run(restic_base_command, read_data=False):
    cmd = restic_base_command + ['check']

    if read_data:
        cmd.append('--read-data')

    try:
        return command_executor.execute(cmd)
    except command_executor.ResticFailedError as e:
        raise restic.errors.RepoIntegrityError(
            'Repo failed integrity check: %s' % str(e)) from e
