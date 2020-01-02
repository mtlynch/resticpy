
from enum import Enum, unique
import subprocess
import platform
import sys
from restic.snapshot import Snapshot
from restic.core import version
from restic.config import restic_bin

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

    # global flags
    cacert = None
    cache_dir = None
    no_lock = False
    limit_download = None
    limit_upload = None
    options = {}
    quiet = False
    verbose = False

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

    def _build_command_internal(self):
        cmd = [restic_bin, '-r', self.path]
        return cmd

    def _build_command(self):
        cmd = [restic_bin, '-r', self.path]

        if self.cacert is not None:
            if type(self.cacert) == str:
                cmd.extend(['--cacert', self.cacert])
            else:
                raise ValueError('cacert shall be type of str or None')

        if self.cache_dir is not None:
            if type(self.cache_dir) == str:
                cmd.extend(['--cache-dir', self.cache_dir])
            else:
                raise ValueError('cache_dir shall be type of str or None')

        if self.no_lock:
            cmd.append('--no-lock')

        if self.limit_download is not None:
            if type(self.limit_download) == int:
                cmd.extend(['--limit-download', str(self.limit_download)])
            else:
                raise ValueError('limit_download shall be type of str or None')

        if self.limit_upload is not None:
            if type(self.limit_upload) == int:
                cmd.extend(['--limit-upload', str(self.limit_upload)])
            else:
                raise ValueError('limit_upload shall be type of str or None')

        if self.quiet:
            cmd.append('--quiet')

        if self.verbose:
            cmd.append('--verbose')
        return cmd


    @staticmethod
    def init(url, password, repo_kind = RepoKind.Local):
        if repo_kind not in [RepoKind.Local, RepoKind.SFTP, RepoKind.REST, RepoKind.S3]:
            raise NotImplementedError('This kind of repo is not implemented now.')
        
        # check url valid(TODO)
        repo = Repo(url, password, repo_kind)

        # create repo
        repo_url = None
        if repo_kind == RepoKind.Local:
            repo_url = url
        elif repo_kind == RepoKind.SFTP:
            repo_url = 'sftp:' + url
        elif repo_kind == RepoKind.REST:
            repo_url = 'rest:' + url
        elif repo_kind == RepoKind.S3:
            repo_url = 's3:' + url
        else:
            raise NotImplementedError('This kind of repo is not implemented now.')
        repo._run_command([restic_bin, 'init', '--repo', url])

        return repo

    def remove_all_snapshots_list(self):
        for each_snapshots in self.snapshots_list:
            each_snapshots.repo = None

        self.snapshots_list = None

    def update_snapshots_list(self):
        snapshots_list = self._run_snapshots_command()
        for each_snapshot in self.snapshots_list:
            if each_snapshot.snapshot_id not in [each.snapshot_id for each in snapshots_list]:
                each_snapshot.repo = None
                self.snapshots_list.remove(each_snapshot)

        for each_snapshot in snapshots_list:
            if each_snapshot.snapshot_id not in [each.snapshot_id for each in self.snapshots_list]:
                self.snapshots_list.append(each_snapshot)

    '''
    Internal command implement
    '''
    def _run_snapshots_command(self):
        cmd = self._build_command()
        cmd.append('snapshots')

        ret = self._run_command(cmd)

        if ret is None:
            return

        return self._parse_snapshots(ret)

    def _run_stats_command(self):
        cmd = self._build_command()
        cmd.append('stats')

        ret = self._run_command(cmd)

        if ret is None:
            return

        return self._parse_stats(ret)

    
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

    def _parse_stats(self, text):
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
            'file_count': file_count,
            'total_size': total_size
        }

    '''
    Public repository API
    '''
    def backup(self, file_path, exclude=None, tags=None):
        # check url valid(TODO)

        # run cmd
        cmd = self._build_command()
        cmd.extend(['backup', file_path])

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
                cmd.extend(['--tag', tags])
            elif type(tags) == list:
                for each_tag in tags:
                    cmd.extend(['--tag', each_tag])
            else:
                raise ValueError('tags shall be type of str or list')

        self._run_command(cmd)

    def check(self, read_data=False):
        cmd = self._build_command()
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

        cmd = self._build_command()
        cmd.extend([snapshot, 'mount', target])

        self._run_command(cmd)

    def restore(self, target, snapshot='latest'):

        if type(snapshot) == Snapshot:
            snapshot = snapshot.snapshot_id
        elif type(snapshot) not in [str, Snapshot]:
            raise ValueError('snapshot shall be type of str or Snapshot')

        cmd = self._build_command()
        cmd.extend(['restore', snapshot, '--target', target])

        self._run_command(cmd)

    def snapshots(self):
        self.update_snapshots_list()
        return self.snapshots_list

    def stats(self):
        return self._run_stats_command()

    def tag(self, add_tags=None, remove_tags=None, set_tags=None, snapshot='latest'):
        if type(snapshot) == Snapshot:
            snapshot = snapshot.snapshot_id
        elif type(snapshot) not in [str, Snapshot]:
            raise ValueError('snapshot shall be type of str or Snapshot')

        cmd = self._build_command()
        cmd.append('tag')

        if add_tags is not None:
            if type(add_tags) == str:
                cmd.extend(['--add', add_tags])
            elif type(add_tags) == list:
                for each_tag in add_tags:
                    if ',' not in each_tag:
                        cmd.extend(['--add', each_tag])
                    else:
                        raise ValueError('the `,` charactor in tag may make PyRestic wrong')
            else:
                raise ValueError('add_tags shall be type of str or list')

        if remove_tags is not None:
            if type(remove_tags) == str:
                cmd.extend(['--remove', remove_tags])
            elif type(remove_tags) == list:
                for each_tag in remove_tags:
                    if ',' not in each_tag:
                        cmd.extend(['--remove', each_tag])
                    else:
                        raise ValueError('the `,` charactor in tag may make PyRestic wrong')
            else:
                raise ValueError('remove_tags shall be type of str or list')

        if set_tags is not None:
            if type(set_tags) == str:
                cmd.extend(['--set', set_tags])
            elif type(set_tags) == list:
                for each_tag in set_tags:
                    if ',' not in each_tag:
                        cmd.extend(['--set', each_tag])
                    else:
                        raise ValueError('the `,` charactor in tag may make PyRestic wrong')
            else:
                raise ValueError('set_tags shall be type of str or list')
        cmd.append(snapshot)
        self._run_command(cmd)



            


