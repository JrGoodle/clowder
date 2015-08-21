"""Git utilities"""
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

def git_fix(repo_path):
    """Commit new main clowder.yaml from current changes"""
    git = sh.git.bake(_cwd=repo_path)
    git.add('clowder.yaml')
    git.commit('-m', 'Update clowder.yaml')
    git.pull()
    git.push()

def git_fix_version(repo_path, version):
    """Commit fixed version of clowder.yaml based on current branches"""
    git = sh.git.bake(_cwd=repo_path)
    git.add('versions')
    git.commit('-m', 'Fix versions/' + version + '/clowder.yaml')
    git.pull()
    git.push()

def git_sync(repo_path, ref):
    """Sync git repo with default branch"""
    git = sh.git.bake(_cwd=repo_path)
    git.fetch('--all', '--prune', '--tags', _out=process_output)
    project_ref = truncate_git_ref(ref)
    # print('currentBranch: ' + self.get_current_branch())
    # print('project_ref: ' + project_ref)
    if get_current_branch(repo_path) != project_ref:
        print('Not on default branch')
        print('Stashing current changes')
        git.stash()
        print('Checking out ' + project_ref)
        git.checkout(project_ref)
    print('Pulling latest changes')
    git.pull(_out=process_output)

def git_sync_version(repo_path, version, ref):
    """Sync fixed version of repo at path"""
    git = sh.git.bake(_cwd=repo_path)
    git.checkout('-b', 'fix/' + version, ref, _out=process_output)

def git_status(repo_path):
    """Print status of repo at path"""
    git = sh.git.bake(_cwd=repo_path)
    print(git.status())

def get_current_branch(repo_path):
    """Return currently checked out branch of project"""
    git = sh.git.bake(_cwd=repo_path)
    return str(git('rev-parse', '--abbrev-ref', 'HEAD')).rstrip('\n')

def get_current_sha(repo_path):
    """Return current git sha for checked out commit"""
    git = sh.git.bake(_cwd=repo_path)
    return str(git('rev-parse', 'HEAD')).rstrip('\n')

def process_output(line):
    """Utility function for command output callbacks"""
    stripped_line = str(line).rstrip('\n')
    print(stripped_line)
