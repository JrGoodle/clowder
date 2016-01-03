"""Git utilities"""
import os, shutil, sys
from git import Repo
from termcolor import colored, cprint

# Disable errors shown by pylint for no specified exception types
# pylint: disable=W0702

def git_branches(repo_path):
    """Get list of current branches"""
    repo = git_repo(repo_path)
    return repo.branches

def git_checkout_branch(repo_path, branch, remote):
    """Checkout branch, and create if it doesn't exist"""
    repo = git_repo(repo_path)
    branch_output = colored('(' + branch + ')', 'magenta')
    correct_branch = False
    if branch in repo.heads:
        default_branch = repo.heads[branch]
        try:
            not_detached = not repo.head.is_detached
            same_branch = repo.head.ref == default_branch
        except:
            pass
        else:
            if not_detached and same_branch:
                print(' - On default branch')
                correct_branch = True
        finally:
            if not correct_branch:
                try:
                    print(' - Checkout branch ' + branch_output)
                    default_branch.checkout()
                except:
                    message = colored(' - Failed to checkout branch ', 'red')
                    print(message + branch_output)
                    print('')
                    sys.exit(1)
    else:
        git_create_checkout_branch(repo_path, branch, remote)

def git_create_checkout_branch(repo_path, branch, remote):
    """Create and checkout tracking branch"""
    repo = git_repo(repo_path)
    branch_output = colored('(' + branch + ')', 'magenta')
    remote_output = colored(remote, attrs=['bold'])
    print(' - Create and checkout branch ' + branch_output)
    try:
        origin = repo.remotes[remote]
        origin.fetch()
    except:
        message = colored(' - Failed to fetch from remote ', 'red')
        print(message + remote_output)
        shutil.rmtree(repo_path)
        print('')
        sys.exit(1)
    else:
        try:
            default_branch = repo.create_head(branch, origin.refs[branch])
        except:
            message = colored(' - Failed to create branch ', 'red')
            print(message + branch_output)
            print('')
            sys.exit(1)
        else:
            try:
                default_branch.set_tracking_branch(origin.refs[branch])
            except:
                message = colored(' - Failed to set tracking branch ', 'red')
                print(message + branch_output)
                print('')
                sys.exit(1)
            else:
                try:
                    default_branch.checkout()
                except:
                    message = colored(' - Failed to checkout branch ', 'red')
                    print(message + branch_output)
                    print('')
                    sys.exit(1)

def git_checkout_ref(repo_path, ref, remote):
    """Checkout branch, tag, or commit from sha"""
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
    """Checkout commit by sha"""
    repo = git_repo(repo_path)
    commit_output = colored('(' + sha + ')', 'magenta')
    correct_commit = False
    try:
        same_sha = repo.head.commit.hexsha == sha
        is_detached = repo.head.is_detached
    except:
        pass
    else:
        if same_sha and is_detached:
            print(' - On correct commit')
            correct_commit = True
    finally:
        if not correct_commit:
            try:
                print(' - Checkout commit ' + commit_output)
                repo.git.checkout(sha)
            except:
                message = colored(' - Failed to checkout commit ', 'red')
                print(message + commit_output)
                print('')
                sys.exit(1)

def git_checkout_tag(repo_path, tag):
    """Checkout commit tag is pointing to"""
    repo = git_repo(repo_path)
    tag_output = colored('(' + tag + ')', 'magenta')
    correct_commit = False
    if tag in repo.tags:
        try:
            same_commit = repo.head.commit == repo.tags[tag].commit
            is_detached = repo.head.is_detached
        except:
            pass
        else:
            if same_commit and is_detached:
                print(' - On correct commit for tag')
                correct_commit = True
        finally:
            if not correct_commit:
                try:
                    print(' - Checkout tag ' + tag_output)
                    repo.git.checkout(tag)
                except:
                    message = colored(' - Failed to checkout tag ', 'red')
                    print(message + tag_output)
                    print('')
                    sys.exit(1)
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
            cprint(' - Failed to initialize repository', 'red')
            print('')
            sys.exit(1)
        else:
            git_create_remote(repo_path, remote, url)
            git_fetch(repo_path)
            git_checkout_ref(repo_path, ref, remote)

def git_create_remote(repo_path, remote, url):
    """Create new remote"""
    repo = git_repo(repo_path)
    remote_names = [r.name for r in repo.remotes]
    if remote not in remote_names:
        remote_output = colored(remote, attrs=['bold'])
        try:
            print(" - Create remote " + remote_output)
            origin = repo.create_remote(remote, url)
            origin.fetch()
        except:
            message = colored(" - Failed to create remote ", 'red')
            print(message + remote_output)
            print('')
            sys.exit(1)

def git_current_branch(repo_path):
    """Return currently checked out branch of project"""
    repo = git_repo(repo_path)
    return repo.head.ref.name

def git_current_sha(repo_path):
    """Return current git sha for checked out commit"""
    repo = git_repo(repo_path)
    return repo.head.commit.hexsha

def git_reset_head(repo_path):
    """Reset head of repo, discarding changes"""
    repo = git_repo(repo_path)
    repo.head.reset(index=True, working_tree=True)

def git_fetch(repo_path):
    """Fetch all remotes, tags, and prune obsolete branches"""
    repo = git_repo(repo_path)
    try:
        print(' - Fetch remote data')
        repo.git.fetch('--all', '--prune', '--tags')
    except:
        cprint(' - Failed to fetch', 'red')
        print('')
        sys.exit(1)

def git_has_untracked_files(repo_path):
    """Check if there are untracked files"""
    repo = git_repo(repo_path)
    if repo.untracked_files:
        return True
    else:
        return False

def git_is_detached(repo_path):
    """Check if HEAD is detached"""
    if not os.path.isdir(repo_path):
        return False
    else:
        repo = git_repo(repo_path)
        return repo.head.is_detached

def git_is_dirty(repo_path):
    """Check if repo is dirty"""
    if not os.path.isdir(repo_path):
        return False
    else:
        repo = git_repo(repo_path)
        return repo.is_dirty()

def git_pull(repo_path):
    """Pull from remote branch"""
    repo = git_repo(repo_path)
    if not repo.head.is_detached:
        try:
            print(' - Pulling latest changes')
            print(repo.git.pull())
        except:
            cprint(' - Failed to pull latest changes', 'red')
            print('')
            sys.exit(1)

def git_pull_remote_branch(repo_path, remote, branch):
    """Pull from remote branch"""
    repo = git_repo(repo_path)
    if not repo.head.is_detached:
        try:
            print(' - Pulling latest changes')
            print(repo.git.pull(remote, branch))
        except:
            cprint(' - Failed to pull latest changes', 'red')
            print('')
            sys.exit(1)

def git_ref_type(ref):
    """Return branch, tag, sha, or unknown ref type"""
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
    repo = git_repo(repo_path)
    if repo.is_dirty():
        print(' - Stashing current changes')
        repo.git.stash()
    else:
        print(' - No changes to stash')

def git_status(repo_path):
    """Print git status"""
    repo = git_repo(repo_path)
    print(repo.git.status())

def git_repo(repo_path):
    """Create Repo instance for path"""
    try:
        repo = Repo(repo_path)
    except:
        repo_path_output = colored(repo_path, 'cyan')
        message = colored("Failed to create Repo instance for ", 'red')
        print(message + repo_path_output)
        print('')
        sys.exit(1)
    else:
        return repo

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
