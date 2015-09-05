"""Git utilities"""
import os
from git import Repo
from termcolor import colored

# Disable errors shown by pylint for no specified exception types
# pylint: disable=W0702

def git_checkout_branch(repo_path, branch, remote):
    """Checkout branch"""
    repo = Repo(repo_path)
    branch_output = colored('(' + branch + ')', 'magenta')
    if branch in repo.heads:
        default_branch = repo.heads[branch]
        try:
            if not repo.head.is_detached and repo.head.ref.commit == default_branch.commit:
                print(' - Already on correct branch')
            else:
                try:
                    print(' - Checkout branch ' + branch_output)
                    default_branch.checkout()
                except:
                    print(' - Failed to checkout branch ' + branch_output)
        except:
            try:
                print(' - Checkout branch ' + branch_output)
                default_branch.checkout()
            except:
                print(' - Failed to checkout branch ' + branch_output)
    else:
        git_create_checkout_branch(repo_path, branch, remote)

def git_create_checkout_branch(repo_path, branch, remote):
    """Create and checkout tracking branch"""
    repo = Repo(repo_path)
    branch_output = colored('(' + branch + ')', 'magenta')
    try:
        print(' - Create and checkout branch ' + branch_output)
        origin = repo.remotes[remote]
        origin.fetch()
        default_branch = repo.create_head(branch, origin.refs[branch])
        default_branch.set_tracking_branch(origin.refs[branch])
        default_branch.checkout()
    except:
        print(' - Failed to create and checkout branch ' + branch_output)

def git_checkout_ref(repo_path, ref, remote):
    """Checkout default branch. Create if doesn't exist"""
    ref_type = git_ref_type(ref)
    if ref_type is 'branch':
        branch = git_truncate_ref(ref)
        git_checkout_branch(repo_path, branch, remote)
    elif ref_type is 'tag':
        tag = git_truncate_ref(ref)
        git_checkout_tag(repo_path, tag)
    elif ref_type is 'sha':
        git_checkout_sha(repo_path, ref)
    else:
        ref_output = colored('(' + ref + ')', 'magenta')
        print('Unknown ref ' + ref_output)

def git_checkout_sha(repo_path, sha):
    """Checkout commit sha"""
    repo = Repo(repo_path)
    ref_output = colored('(' + sha + ')', 'magenta')
    try:
        if repo.head.commit.hexsha == sha and repo.head.is_detached:
            print(' - Already on correct commit')
        else:
            try:
                print(' - Checkout ref ' + ref_output)
                repo.git.checkout(sha)
            except:
                print(' - Failed to checkout ref ' + ref_output)
    except:
        try:
            print(' - Checkout ref ' + ref_output)
            repo.git.checkout(sha)
        except:
            print(' - Failed to checkout ref ' + ref_output)

def git_checkout_tag(repo_path, tag):
    """Checkout tag"""
    repo = Repo(repo_path)
    tag_output = colored('(' + tag + ')', 'magenta')
    if tag in repo.tags:
        try:
            if repo.head.commit == repo.tags[tag].commit and repo.head.is_detached:
                print(' - Already on correct commit')
            else:
                try:
                    print(' - Checkout tag ' + tag_output)
                    repo.git.checkout(tag)
                except:
                    print(' - Failed to checkout tag ' + tag_output)
        except:
            try:
                print(' - Checkout tag ' + tag_output)
                repo.git.checkout(tag)
            except:
                print(' - Failed to checkout tag ' + tag_output)
    else:
        print(' - No existing tag ' + tag_output)

def git_clone_url_at_path(url, repo_path, ref, remote):
    """Clone git repo from url at path"""
    repo_path_output = colored(repo_path, 'cyan')
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        if not os.path.isdir(repo_path):
            os.makedirs(repo_path)
        try:
            print(' - Cloning repo at ' + repo_path_output)
            Repo.init(repo_path)
        except:
            print(' - Failed to initialize repository')
        else:
            git_create_remote(repo_path, remote, url)
            git_fetch(repo_path)
            git_checkout_ref(repo_path, ref, remote)

def git_create_remote(repo_path, remote, url):
    """Create new remote"""
    repo = Repo(repo_path)
    remote_names = [r.name for r in repo.remotes]
    if remote not in remote_names:
        remote_output = colored(remote, attrs=['bold'])
        try:
            print(" - Create remote " + remote_output)
            origin = repo.create_remote(remote, url)
            origin.fetch()
        except:
            print(" - Failed to create remote " + remote_output)

def git_current_branch(repo_path):
    """Return currently checked out branch of project"""
    repo = Repo(repo_path)
    return repo.head.ref.name

def git_current_sha(repo_path):
    """Return current git sha for checked out commit"""
    repo = Repo(repo_path)
    return repo.head.commit.hexsha

def git_fetch(repo_path):
    """Fetch all remotes, tags, and prune"""
    try:
        repo = Repo(repo_path)
        repo.git.fetch('--all', '--prune', '--tags')
    except:
        print(' - Failed to fetch')

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
    if not repo.head.is_detached:
        try:
            print(' - Pulling latest changes')
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
