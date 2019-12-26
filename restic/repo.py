
from enum import Enum, unique
import subprocess
import platform
from restic.snapshot import Snapshot

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

class Repo(object):
    kind = None
    path = None
    password = None
    is_open = False
    def __init__(self, path, password, kind = RepoKind.Local):
        self.path = path
        self.kind = kind
        self.password = password
        self.is_open = False

    def _run_command(self, cmd):
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
        return out

    @staticmethod
    def init(url, password, repo_kind = RepoKind.Local):
        if repo_kind != RepoKind.Local:
            raise NotImplementedError('This kind of repo is not implemented now.')
        
        # check url valid(TODO)
        repo = Repo(url, password, repo_kind)

        # create repo
        repo._run_command(['restic', 'init', '--repo', url])

        return repo

    def backup(self, file_path, exclude=None):
        # check url valid(TODO)

        # run cmd
        cmd = ['restic']
        cmd.append('-r')
        cmd.append(self.path)
        cmd.append('--verbose')
        cmd.append('backup')
        cmd.append(file_path)

        if exclude is not None and type(exclude) == list:
            exclude_cmd = '--exclude="'
            for i, each_file in enumerate(exclude):
                if i != 0:
                    exclude_cmd.append(',')
                exclude_cmd.append(each_file)
            exclude_cmd.append('"')
            cmd.append(exclude_cmd)

        self._run_command(cmd)

    def check(self, read_data=False):
        cmd = ['restic']
        cmd.append('-r')
        cmd.append(self.path)
        cmd.append('check')

        if read_data:
            cmd.append('--read-data')

        ret_text = self._run_command(cmd)

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

        cmd = ['restic']
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

        cmd = ['restic']
        cmd.append('-r')
        cmd.append(self.path)
        cmd.append(snapshot)
        cmd.append('--target')
        cmd.append(target)

        self._run_command(cmd)

    def snapshots(self):
        cmd = ['restic']
        cmd.append('-r')
        cmd.append(self.path)
        cmd.append('snapshots')

        ret = self._run_command(cmd)

        return self._parse_snapshots(ret)

       
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
            snapshot = Snapshot()
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


            


