from restic.config import restic_bin
from restic.internal import command_executor


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

    command_executor.execute(cmd)
