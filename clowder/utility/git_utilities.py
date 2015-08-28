"""Git utilities"""
import os
from git import Repo
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
        repo = Repo.init(repo_path)
        origin = repo.create_remote('origin', url)
        origin.fetch()
        master_branch = repo.create_head('master', origin.refs.master)
        master_branch.set_tracking_branch(origin.refs.master)
        master_branch.checkout()

def git_fix(repo_path):
    """Commit new main clowder.yaml from current changes"""
    repo = Repo(repo_path)
    git = repo.git
    git.add('clowder.yaml')
    git.commit('-m', 'Update clowder.yaml')
    git.pull()
    git.push()

def git_fix_version(repo_path, version):
    """Commit fixed version of clowder.yaml based on current branches"""
    repo = Repo(repo_path)
    git = repo.git
    git.add('versions')
    git.commit('-m', 'Fix versions/' + version + '/clowder.yaml')
    git.pull()
    git.push()

def git_sync(repo_path, ref):
    """Sync git repo with default branch"""
    repo = Repo(repo_path)
    git = repo.git
    git.fetch('--all', '--prune', '--tags')
    project_ref = truncate_git_ref(ref)
    if get_current_branch(repo_path) != project_ref:
        print('Not on default branch')
        print('Stashing current changes')
        git.stash()
        print('Checking out ' + project_ref)
        git.checkout(project_ref)
    print('Pulling latest changes')
    git.pull()

def git_sync_version(repo_path, version, ref):
    """Sync fixed version of repo at path"""
    repo = Repo(repo_path)
    git = repo.git
    fix_branch = 'fix/' + version
    try:
        if repo.heads[fix_branch].exists():
            if repo.active_branch != repo.heads[fix_branch]:
                print('Checking out existing ' + fix_branch + ' branch')
                git.checkout(fix_branch)
    except:
        print('No existing ' + fix_branch + ' branch')
        print('Checking out new branch ' + fix_branch)
        git.checkout('-b', fix_branch, ref)

def git_status(repo_path):
    """Print status of repo at path"""
    repo = Repo(repo_path)
    git = repo.git
    git.status()

def get_current_branch(repo_path):
    """Return currently checked out branch of project"""
    repo = Repo(repo_path)
    git = repo.git
    return str(git.rev_parse('--abbrev-ref', 'HEAD')).rstrip('\n')

def get_current_sha(repo_path):
    """Return current git sha for checked out commit"""
    repo = Repo(repo_path)
    git = repo.git
    return str(git.rev_parse('HEAD')).rstrip('\n')

def process_output(line):
    """Utility function for command output callbacks"""
    stripped_line = str(line).rstrip('\n')
    print(stripped_line)
