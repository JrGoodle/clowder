"""Git utilities"""
import os, sys
from git import Repo
from termcolor import colored, cprint

# Disable errors shown by pylint for sh.git
# pylint: disable=E1101

def git_clone_url_at_path(url, repo_path):
    """Clone git repo from url at path"""
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        if not os.path.isdir(repo_path):
            os.makedirs(repo_path)
        repo_path_output = colored(repo_path, 'cyan')
        print(' - Cloning repo at: ' + repo_path_output)
        repo = Repo.init(repo_path)
        origin = repo.create_remote('origin', url)
        origin.fetch()
        master_branch = repo.create_head('master', origin.refs.master)
        master_branch.set_tracking_branch(origin.refs.master)
        master_branch.checkout()

def git_current_branch(repo_path):
    """Return currently checked out branch of project"""
    repo = Repo(repo_path)
    git = repo.git
    return str(git.rev_parse('--abbrev-ref', 'HEAD')).rstrip('\n')

def git_current_ref(repo_path):
    """Return current ref of project"""
    repo = Repo(repo_path)
    if repo.head.is_detached:
        return git_current_sha(repo_path)
    else:
        return git_current_sha(repo_path)

def git_current_sha(repo_path):
    """Return current git sha for checked out commit"""
    repo = Repo(repo_path)
    git = repo.git
    return str(git.rev_parse('HEAD')).rstrip('\n')

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

def git_groom(repo_path):
    """Sync clowder repo with current branch"""
    repo = Repo(repo_path)
    git = repo.git
    git.fetch('--all', '--prune', '--tags')
    if not git_is_detached(repo_path):
        print(' - Pulling latest changes')
        print(git.pull())
    else:
        print(' - HEAD is detached, nothing to pull')

def git_herd(repo_path, ref):
    """Sync git repo with default branch"""
    repo = Repo(repo_path)
    git = repo.git
    git.fetch('--all', '--prune', '--tags')
    project_ref = git_truncate_ref(ref)
    if git_current_branch(repo_path) != project_ref:
        project_output = colored(project_ref, 'magenta')
        print(' - Not on default branch, checking out ' + project_output)
        git.checkout(project_ref)
    print(' - Pulling latest changes')
    print(git.pull())

def git_herd_version(repo_path, version, ref):
    """Sync fixed version of repo at path"""
    repo = Repo(repo_path)
    git = repo.git
    fix_branch = 'clowder-fix/' + version
    branch_output = colored(fix_branch, 'magenta')
    try:
        if repo.heads[fix_branch]:
            if repo.active_branch != repo.heads[fix_branch]:
                print(' - Checking out existing branch: ' + branch_output)
                git.checkout(fix_branch)
    except:
        print(' - No existing branch, checking out: ' + branch_output)
        git.checkout('-b', fix_branch, ref)

def git_is_detached(repo_path):
    """Check if HEAD is detached"""
    repo = Repo(repo_path)
    return repo.head.is_detached

def git_is_dirty(repo_path):
    """Check if repo is dirty"""
    repo = Repo(repo_path)
    return repo.is_dirty()

def git_litter(repo_path):
    """Discard current changes in repository"""
    repo = Repo(repo_path)
    if repo.is_dirty():
        print(' - Discarding current changes')
        repo.head.reset(index=True, working_tree=True)
    else:
        print(' - No changes to discard')

def git_stash(repo_path):
    """Stash current changes in repository"""
    repo = Repo(repo_path)
    if repo.is_dirty():
        print(' - Stashing current changes')
        repo.git.stash()
    else:
        print(' - No changes to stash')

def git_truncate_ref(ref):
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

def git_validate_repo_state(repo_path):
    """Validate repo state"""
    git_path = os.path.join(repo_path, '.git')
    if not os.path.isdir(git_path):
        return
    if git_is_dirty(repo_path):
        repo_output = colored(repo_path, 'cyan')
        print(repo_output + ' is dirty')
        print('Please stash, commit, or discard your changes before running clowder')
        print('')
        cprint('Exiting...', 'red')
        print('')
        sys.exit()
    # if git_untracked_files(repo_path):
    #     print(repo_path + ' has untracked files.')
    #     print('Please remove these files or add to .gitignore')
    #     print('')
    #     cprint('Exiting...', 'red')
    #     print('')
    #     sys.exit()
    # if git_is_detached(repo_path):
    #     repo_output = colored(repo_path, 'cyan')
    #     print(repo_output  + ' HEAD is detached')
    #     print('Please point your HEAD to a branch before running clowder')
    #     print('')
    #     cprint('Exiting...', 'red')
    #     print('')
    #     sys.exit()

def git_untracked_files(repo_path):
    """Check if there are untracked files"""
    repo = Repo(repo_path)
    if repo.untracked_files:
        return True
    else:
        return False

def process_output(line):
    """Utility function for command output callbacks"""
    stripped_line = str(line).rstrip('\n')
    print(stripped_line)
