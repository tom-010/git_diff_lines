import subprocess
import shlex
from git_diff_lines.parser import parse


def list_currently_changed_lines(path_to_repo='.'):
    return git_diff_lines(compared_to='HEAD', path_to_repo=path_to_repo)


def list_changed_lines_in_last_commit(path_to_repo='.'):
    return git_diff_lines(compared_to='HEAD~1', path_to_repo=path_to_repo)


def git_diff_lines(compared_to='HEAD', path_to_repo='.'):
    """"
    Returns a list of tuples of changed lines in a diff in the 
    form (filename, line_number) with the type tuple(str, int).

    compared_to is the argument passed to git diff, so for example
                if compared_to is HEAD~1 it is the same as 
                git diff HEAD~1
    path_to_repo is the (relative or absolute) path, to the directory, 
                 that contains the .git folder
    """
    stdout, stderr, has_error = _run(f'git diff {compared_to}', cwd=path_to_repo)
    if has_error:
        print(stderr)
        return set()
    return parse(stdout)



####



def _run(command, cwd='.'):
    if isinstance(command, str):
        command = shlex.split(command)
    res = subprocess.run(
        command, 
        cwd=cwd,
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        check=False)
    has_error = res.returncode != 0
    return res.stdout.decode(), res.stderr.decode(), has_error