"""Utilities for clowder"""
import os
import sh
# Disable errors shown by pylint for sh.git
# pylint: disable=E1101

def truncate_git_ref(ref):
    """Return bare branch, tag, or sha"""
    git_branch = "refs/heads/"
    git_tag = "refs/tags/"
    if ref.startswith(git_branch):
        length = len(git_branch)
    elif ref.startswith(git_tag):
        length = len(git_tag)
    else:
        length = 0
    return ref[length:]

def clone_git_url_at_path(url, repo_path):
    """Clone git repo from url at path"""
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        if not os.path.isdir(repo_path):
            os.makedirs(repo_path)
        print('Cloning git repo at ' + repo_path)
        git = sh.git.bake(_cwd=repo_path)
        git.init()
        git.remote('add', 'origin', url)
        git.fetch('--all', '--prune', '--tags', _out=process_output)
        git.checkout('-t', 'origin/master')

def process_output(line):
    """Utility function for command output callbacks"""
    print(line)

def symlink_clowder_yaml(root_directory, clowder_yaml):
    """Create clowder.yaml symlink in directory pointing to file"""
    os.chdir(root_directory)
    if os.path.isfile(clowder_yaml):
        if os.path.isfile('clowder.yaml'):
            os.remove('clowder.yaml')
        os.symlink(clowder_yaml, 'clowder.yaml')
    else:
        print(clowder_yaml + " doesn't seem to exist")
