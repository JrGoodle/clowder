"""Git utilities"""
import os
from git import Repo
from termcolor import colored

# Disable errors shown by pylint for no specified exception types
# pylint: disable=W0702

def git_checkout_default_ref(repo_path, ref, remote):
    """Checkout default branch. Create if doesn't exist"""
    repo = Repo(repo_path)
    ref_type = git_ref_type(ref)
    if ref_type is 'branch':
        branch = git_truncate_ref(ref)
        branch_output = colored('(' + branch + ')', 'magenta')
        if branch in repo.heads:
            default_branch = repo.heads[branch]
            if repo.head.is_detached:
                print(' - Checkout ' + branch_output)
                default_branch.checkout()
            elif repo.head.ref != default_branch:
                print(' - Checkout ' + branch_output)
                default_branch.checkout()
        else:
            try:
                print(' - Create and checkout ' + branch_output)
                origin = repo.remotes[remote]
                origin.fetch()
                default_branch = repo.create_head(branch, origin.refs[branch])
                default_branch.set_tracking_branch(origin.refs[branch])
                default_branch.checkout()
            except:
                print(' - Failed to create and checkout ' + branch_output)
    elif ref_type is 'tag':
        tag = git_truncate_ref(ref)
        tag_output = colored('(' + tag + ')', 'magenta')
        print(' - Checkout tag ' + tag_output)
        try:
            repo.git.checkout(ref)
        except:
            print(' - Failed to checkout tag ' + tag_output)
    elif ref_type is 'sha':
        ref_output = colored('(' + ref + ')', 'magenta')
        print(' - Checkout ref ' + ref_output)
        try:
            repo.git.checkout(ref)
        except:
            print(' - Failed to checkout ref ' + ref_output)
    else:
        print('Unknown ref type')

def git_clone_url_at_path(url, repo_path, branch, remote):
    """Clone git repo from url at path"""
    repo_path_output = colored(repo_path, 'cyan')
    ref = git_truncate_ref(branch)
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        if not os.path.isdir(repo_path):
            os.makedirs(repo_path)

        print(' - Cloning repo at ' + repo_path_output)
        repo = Repo.init(repo_path)
        git_create_remote(repo_path, remote, url)
        git_fetch(repo_path)

        ref_type = git_ref_type(branch)
        if ref_type is not 'branch':
            try:
                repo.git.checkout(ref)
            except:
                if ref_type is 'tag':
                    tag = git_truncate_ref(ref)
                    tag_output = colored('(' + tag + ')', 'magenta')
                    print('Failed to checkout tag ' + tag_output)
                elif ref_type is 'sha':
                    ref_output = colored('(' + ref + ')', 'magenta')
                    print('Failed to checkout ref ' + ref_output)
                else:
                    ref_output = colored('(' + ref + ')', 'magenta')
                    print('Failed to checkout unknown ref ' + ref_output)
        else:
            try:
                origin = repo.remotes[remote]
                default_branch = repo.create_head(ref, origin.refs[ref])
                default_branch.set_tracking_branch(origin.refs[ref])
                default_branch.checkout()
            except:
                print('Failed to create and checkout branch ' + ref)

def git_create_remote(repo_path, remote, url):
    """Create new remote"""
    repo = Repo(repo_path)
    try:
        repo.remotes[remote]
    except:
        print(" - Creating remote " + remote)
        origin = repo.create_remote(remote, url)
        origin.fetch()

def git_current_branch(repo_path):
    """Return currently checked out branch of project"""
    repo = Repo(repo_path)
    return str(repo.git.rev_parse('--abbrev-ref', 'HEAD')).rstrip('\n')

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
    return str(repo.git.rev_parse('HEAD')).rstrip('\n')

def git_fetch(repo_path):
    """Fetch all remotes, tags, and prune"""
    repo = Repo(repo_path)
    try:
        repo.git.fetch('--all', '--prune', '--tags')
    except:
        print(' - Failed to fetch.')

def git_groom(repo_path):
    """Discard current changes in repository"""
    repo = Repo(repo_path)
    if repo.is_dirty():
        print(' - Discarding current changes')
        repo.head.reset(index=True, working_tree=True)
    else:
        print(' - No changes to discard')

def git_herd(repo_path, ref, remote, url):
    """Sync git repo with default branch"""
    if git_ref_type(ref) is not 'branch':
        if not os.path.isdir(os.path.join(repo_path, '.git')):
            git_clone_url_at_path(url, repo_path, ref, remote)
        else:
            git_create_remote(repo_path, remote, url)
            git_fetch(repo_path)
            git_checkout_default_ref(repo_path, ref, remote)
    else:
        if not os.path.isdir(os.path.join(repo_path, '.git')):
            git_clone_url_at_path(url, repo_path, ref, remote)
        else:
            git_create_remote(repo_path, remote, url)
            git_fetch(repo_path)
            git_checkout_default_ref(repo_path, ref, remote)
            branch = git_truncate_ref(ref)
            git_pull(repo_path, remote, branch)

def git_herd_version(repo_path, version, ref):
    """Sync fixed version of repo at path"""
    repo = Repo(repo_path)
    branch_output = colored('(' + version + ')', 'magenta')
    try:
        if repo.heads[version]:
            if repo.active_branch is not repo.heads[version]:
                print(' - Checkout ' + branch_output)
                repo.git.checkout(version)
    except:
        # print(' - No existing branch.')
        print(' - Create and checkout ' + branch_output)
        repo.git.checkout('-b', version, ref)

def git_has_untracked_files(repo_path):
    """Check if there are untracked files"""
    repo = Repo(repo_path)
    if repo.untracked_files:
        return True
    else:
        return False

def git_is_detached(repo_path):
    """Check if HEAD is detached"""
    repo = Repo(repo_path)
    return repo.head.is_detached

def git_is_dirty(repo_path):
    """Check if repo is dirty"""
    repo = Repo(repo_path)
    return repo.is_dirty()

def git_pull(repo_path, remote, branch):
    """Pull from remote branch"""
    repo = Repo(repo_path)
    print(' - Pulling latest changes')
    if not repo.head.is_detached:
        try:
            print(repo.git.pull(remote, branch))
        except:
            print(' - Failed to pull latest changes')

def git_ref_type(ref):
    """Return branch, tag, or sha"""
    git_branch = "refs/heads/"
    git_tag = "refs/tags/"
    if ref.startswith(git_branch):
        return 'branch'
    elif ref.startswith(git_tag):
        return 'tag'
    elif len(ref) is 40:
        return 'sha'
    else:
        return 'unknown'

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
    git_fetch(repo_path)
    repo = Repo(repo_path)
    if not git_is_detached(repo_path):
        print(' - Pulling latest changes')
        print(repo.git.pull())

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

def git_validate_untracked(repo_path):
    """Validate repo untracked files"""
    return not git_has_untracked_files(repo_path)
