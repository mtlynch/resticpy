import restic.errors
from restic.internal import command_executor


def run(restic_base_command, read_data=False, read_data_subset=None):
    cmd = restic_base_command + ['check']

    if read_data:
        cmd.append('--read-data')

    if read_data_subset:
        cmd.extend(['--read-data-subset', read_data_subset])

    try:
        return command_executor.execute(cmd)
    except restic.errors.ResticFailedError:
        return None
