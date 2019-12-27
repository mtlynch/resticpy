
from enum import Enum, unique
import subprocess
import platform
import sys
import re
from restic.snapshot import Snapshot
from restic import restic_bin

@unique
class RepoKind(Enum):
    Local = 0
    SFTP = 1
    REST = 2
    S3 = 3
    Swift = 4
    B2 = 5
    Azure = 6
    GoogleStorage = 7
    Rclone = 8

def run_restic(cmd):
    out = ''
    err = ''
    try:
        with subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            encoding='utf-8',
            text=True) as proc:
            out, err = proc.communicate()
            if err is not None:
                raise RuntimeError('Command runtime failure')
            proc.wait()
            if proc.returncode != 0:
                raise RuntimeError(f'Return code {proc.returncode} is not zero')
    except FileNotFoundError:
        raise RuntimeError('Cannot find restic installed')

    return out

def version():
    cmd = [restic_bin, 'version']
    out = run_restic(cmd)
    if out is None:
        return None
    matchObj = re.match(r'restic ([0-9\.]+) compiled with go([0-9\.]+) on ([a-zA-Z0-9]+)/([a-zA-Z0-9]+)', out)
    return {
        'restic_version': matchObj.group(1),
        'go_version': matchObj.group(2),
        'platform_version': matchObj.group(3),
        'Architecture': matchObj.group(4)
    }

class Repo(object):
    kind = None
    path = None
    password = None
    is_open = False
    snapshots_list = []
    def __init__(self, path, password, kind = RepoKind.Local):
        self.path = path
        self.kind = kind
        self.password = password
        self.is_open = False

        try:
            version()
        except Exception:
            print('restic is not in env or it has not been installed')

    def _run_command(self, cmd):
        out = ''
        err = ''
        try:
            with subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                encoding='utf-8',
                text=True) as proc:
                out, err = proc.communicate(self.password)
                if err is not None:
                    raise RuntimeError('Command runtime failure')
                proc.wait()
                if proc.returncode != 0:
                    raise RuntimeError(f'Return code {proc.returncode} is not zero')
        except FileNotFoundError:
            raise RuntimeError('Cannot find restic installed')

        return out

    @staticmethod
    def init(url, password, repo_kind = RepoKind.Local):
        if repo_kind != RepoKind.Local:
            raise NotImplementedError('This kind of repo is not implemented now.')
        
        # check url valid(TODO)
        repo = Repo(url, password, repo_kind)

        # create repo
        repo._run_command([restic_bin, 'init', '--repo', url])

        return repo

    def remove_all_snapshots_list(self):
        for each_snapshots in self.snapshots_list:
            each_snapshots.repo = None

        self.snapshots_list = None

    def update_snapshots_list(self):
        snapshots_list = self.get_snapshots()
        for each_snapshot in self.snapshots_list:
            if each_snapshot.snapshot_id not in [each.snapshot_id for each in snapshots_list]:
                each_snapshot.repo = None
                self.snapshots_list.remove(each_snapshot)

        for each_snapshot in snapshots_list:
            if each_snapshot.snapshot_id not in [each.snapshot_id for each in self.snapshots_list]:
                self.snapshots_list.append(each_snapshot)

    def backup(self, file_path, exclude=None, tags=None):
        # check url valid(TODO)

        # run cmd
        cmd = [restic_bin]
        cmd.append('-r')
        cmd.append(self.path)
        cmd.append('--verbose')
        cmd.append('backup')
        cmd.append(file_path)

        if exclude is not None and type(exclude) == list:
            exclude_cmd = '--exclude="'
            for i, each_file in enumerate(exclude):
                if i != 0:
                    exclude_cmd += ','
                exclude_cmd += each_file
            exclude_cmd += '"'
            cmd.append(exclude_cmd)

        if tags is not None:
            if type(tags) == str:
                cmd.append('--tag')
                cmd.append(tags)
            elif type(tags) == list:
                for each_tag in tags:
                    cmd.append('--tag')
                    cmd.append(each_tag)
            else:
                raise ValueError('tags shall be type of str or list')


        self._run_command(cmd)

    def check(self, read_data=False):
        cmd = [restic_bin]
        cmd.append('-r')
        cmd.append(self.path)
        cmd.append('check')

        if read_data:
            cmd.append('--read-data')

        ret_text = self._run_command(cmd)

        if ret_text is None:
            return

        lines = ret_text.splitlines()
        has_errors = lines[-1].strip() != 'no errors were found'

        if has_errors:
            for each_line in lines:
                if each_line.startswith('error') or each_line.startswith('Fatal'):
                    print(each_line)

        return has_errors

    def mount(self, target, snapshot='latest'):
        if 'Linux' not in platform.system():
            raise RuntimeError('Mounting repositories via FUSE is not possible on OpenBSD, Solaris/illumos and Windows.')
        if type(snapshot) == Snapshot:
            snapshot = snapshot.snapshot_id
        elif type(snapshot) not in [str, Snapshot]:
            raise ValueError('snapshot shall be type of str or Snapshot')

        cmd = [restic_bin]
        cmd.append('-r')
        cmd.append(self.path)
        cmd.append(snapshot)
        cmd.append('mount')
        cmd.append(target)

        self._run_command(cmd)

    def restore(self, target, snapshot='latest'):

        if type(snapshot) == Snapshot:
            snapshot = snapshot.snapshot_id
        elif type(snapshot) not in [str, Snapshot]:
            raise ValueError('snapshot shall be type of str or Snapshot')

        cmd = [restic_bin]
        cmd.append('-r')
        cmd.append(self.path)
        cmd.append('restore')
        cmd.append(snapshot)
        cmd.append('--target')
        cmd.append(target)

        self._run_command(cmd)

    def snapshots(self):
        self.update_snapshots_list()
        return self.snapshots_list

    def get_snapshots(self):
        cmd = [restic_bin]
        cmd.append('-r')
        cmd.append(self.path)
        cmd.append('snapshots')

        ret = self._run_command(cmd)

        if ret is None:
            return

        return self._parse_snapshots(ret)

    def tag(self, add_tags=None, remove_tags=None, set_tags=None, snapshot='latest'):
        if type(snapshot) == Snapshot:
            snapshot = snapshot.snapshot_id
        elif type(snapshot) not in [str, Snapshot]:
            raise ValueError('snapshot shall be type of str or Snapshot')

        cmd = [restic_bin, '-r']
        cmd.append(self.path)
        cmd.append('tag')

        if add_tags is not None:
            if type(add_tags) == str:
                cmd.append('--add')
                cmd.append(add_tags)
            elif type(add_tags) == list:
                for each_tag in add_tags:
                    cmd.append('--add')
                    cmd.append(each_tag)
            else:
                raise ValueError('add_tags shall be type of str or list')

        if remove_tags is not None:
            if type(remove_tags) == str:
                cmd.append('--remove')
                cmd.append(remove_tags)
            elif type(remove_tags) == list:
                for each_tag in remove_tags:
                    cmd.append('--remove')
                    cmd.append(each_tag)
            else:
                raise ValueError('remove_tags shall be type of str or list')

        if set_tags is not None:
            if type(set_tags) == str:
                cmd.append('--set')
                cmd.append(set_tags)
            elif type(set_tags) == list:
                for each_tag in set_tags:
                    cmd.append('--set')
                    cmd.append(each_tag)
            else:
                raise ValueError('set_tags shall be type of str or list')
        cmd.append(snapshot)
        self._run_command(cmd)
       
    def _parse_snapshots(self, text):
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
            snapshot = Snapshot(self)
            line = lines[line_number]
            if line.startswith(horizontal_line):
                break
            for i, each_header in enumerate(header):
                if i == 0:
                    snapshot.set_attr(each_header, line[:header_range[i+1]].strip())
                elif i == len(header_range) - 1:
                    snapshot.set_attr(each_header, line[header_range[i]:].strip())
                else:
                    snapshot.set_attr(each_header, line[header_range[i]:header_range[i+1]].strip())
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


            


