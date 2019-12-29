
import re
import subprocess
from restic.config import restic_bin

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

def self_update():
    cmd = [restic_bin, 'self-update']
    run_restic(cmd)


def generate(bash_completion=None, man=None, zsh_completion=None):
    cmd = [restic_bin, 'generate']
    if bash_completion is not None:
        if type(bash_completion) == str:
            cmd.extend(['--bash-completion', bash_completion])
        else:
            raise ValueError('bash-completion shall be type of str or None')

    if man is not None:
        if type(man) == str:
            cmd.extend(['--man', man])
        else:
            raise ValueError('man shall be type of str or None')


    if zsh_completion is not None:
        if type(zsh_completion) == str:
            cmd.extend(['--zsh-completion', zsh_completion])
        else:
            raise ValueError('zsh-completion shall be type of str or None')

    run_restic(cmd)
