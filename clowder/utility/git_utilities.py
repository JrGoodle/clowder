"""Git utilities"""
import os
from git import Repo
from termcolor import colored

def git_clone_url_at_path(url, repo_path):
    """Clone git repo from url at path"""
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        if not os.path.isdir(repo_path):
            os.makedirs(repo_path)
        repo_path_output = colored(repo_path, 'cyan')
        print(' - Cloning repo at ' + repo_path_output)
        repo = Repo.init(repo_path)
        origin = repo.create_remote('origin', url)
        try:
            origin.fetch()
        except:
            print(' - Failed to fetch. Removing ' + repo_path_output)
            os.rmdir(repo_path)
            return
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

def git_diff_index_head(repo_path):
    """Print diff of index and HEAD"""
    repo = Repo(repo_path)
    print('repo.index.diff(repo.head.commit)')
    print('A diff between the index and the commit’s tree your HEAD points to')
    print(repo.index.diff(repo.head.commit))

def git_diff_index_working_tree(repo_path):
    """Print diff of index and working tree"""
    repo = Repo(repo_path)
    print('repo.index.diff(None)')
    print('A diff between the index and the working tree')
    print(repo.index.diff(None))

def git_diff_untracked_files(repo_path):
    """Print diff of untracked files"""
    repo = Repo(repo_path)
    print('repo.untracked_files')
    print('A list of untracked files')
    print(repo.untracked_files)

def git_fix_version(repo_path, version):
    """Commit fixed version of clowder.yaml based on current branches"""
    repo = Repo(repo_path)
    git = repo.git
    git.add('versions')
    git.commit('-m', 'Fix versions/' + version + '/clowder.yaml')
    git.pull()
    git.push()

def git_groom(repo_path):
    """Discard current changes in repository"""
    repo = Repo(repo_path)
    if repo.is_dirty():
        print(' - Discarding current changes')
        repo.head.reset(index=True, working_tree=True)
    else:
        print(' - No changes to discard')

def git_herd(repo_path, ref):
    """Sync git repo with default branch"""
    repo = Repo(repo_path)
    git = repo.git
    git.fetch('--all', '--prune', '--tags')
    project_ref = git_truncate_ref(ref)
    branch_output = colored('(' + project_ref + ')', 'magenta')
    if git_current_branch(repo_path) is not project_ref:
        try:
            if repo.heads[project_ref]:
                # print(' - Not on default branch.')
                print(' - Checkout ' + branch_output)
                git.checkout(project_ref)
                print(' - Pulling latest changes')
                print(git.pull())
        except:
            # print(' - No existing default branch.')
            print(' - Create and checkout ' + branch_output)
            origin = repo.remotes.origin
            branch = repo.create_head(project_ref, origin.refs[project_ref])
            branch.set_tracking_branch(origin.refs[project_ref])
            branch.checkout()
    else:
        print(' - Pulling latest changes')
        print(git.pull())

def git_herd_version(repo_path, version, ref):
    """Sync fixed version of repo at path"""
    repo = Repo(repo_path)
    git = repo.git
    branch_output = colored('(' + version + ')', 'magenta')
    try:
        if repo.heads[version]:
            if repo.active_branch is not repo.heads[version]:
                print(' - Checkout ' + branch_output)
                git.checkout(version)
    except:
        # print(' - No existing branch.')
        print(' - Create and checkout ' + branch_output)
        git.checkout('-b', version, ref)

def git_is_detached(repo_path):
    """Check if HEAD is detached"""
    repo = Repo(repo_path)
    return repo.head.is_detached

def git_is_dirty(repo_path):
    """Check if repo is dirty"""
    repo = Repo(repo_path)
    return repo.is_dirty()

def git_stash(repo_path):
    """Stash current changes in repository"""
    repo = Repo(repo_path)
    if repo.is_dirty():
        print(' - Stashing current changes')
        repo.git.stash()
    else:
        print(' - No changes to stash')

def git_status(repo_path):
    """Print git status"""
    repo = Repo(repo_path)
    print(repo.git.status())

def git_sync(repo_path):
    """Sync clowder repo with current branch"""
    repo = Repo(repo_path)
    git = repo.git
    git.fetch('--all', '--prune', '--tags')
    if not git_is_detached(repo_path):
        print(' - Pulling latest changes')
        print(git.pull())

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

def git_validate_detached(repo_path):
    """Validate repo detached HEAD"""
    return not git_is_detached(repo_path)

def git_validate_dirty(repo_path):
    """Validate repo dirty files"""
    return not git_is_dirty(repo_path)

def git_validate_repo_state(repo_path):
    """Validate repo state"""
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        return True
    return git_validate_dirty(repo_path)
    # and git_validate_detached(repo_path)
    # and git_validate_untracked(repo_path)

def git_validate_untracked(repo_path):
    """Validate repo untracked files"""
    return not git_has_untracked_files(repo_path)

def git_has_untracked_files(repo_path):
    """Check if there are untracked files"""
    repo = Repo(repo_path)
    if repo.untracked_files:
        return True
    else:
        return False
