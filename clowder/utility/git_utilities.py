"""Git utilities"""
import os
from git import Repo
from termcolor import colored

# Disable errors shown by pylint for no specified exception types
# pylint: disable=W0702

def git_checkout_branch(repo_path, branch, remote):
    """Checkout branch, and create if it doesn't exist"""
    try:
        repo = Repo(repo_path)
    except:
        repo_path_output = colored(repo_path, 'cyan')
        print("Failed to create Repo instance for " + repo_path_output)
    else:
        branch_output = colored('(' + branch + ')', 'magenta')
        correct_branch = False
        if branch in repo.heads:
            default_branch = repo.heads[branch]
            try:
                not_detached = not repo.head.is_detached
                same_branch = repo.head.ref == default_branch
                # same_commit = repo.head.ref.commit == default_branch.commit
            except:
                pass
            else:
                if not_detached and same_branch:
                    print(' - On correct branch')
                    correct_branch = True
            finally:
                if not correct_branch:
                    try:
                        print(' - Checkout branch ' + branch_output)
                        default_branch.checkout()
                    except:
                        print(' - Failed to checkout branch ' + branch_output)
        else:
            git_create_checkout_branch(repo_path, branch, remote)

def git_create_checkout_branch(repo_path, branch, remote):
    """Create and checkout tracking branch"""
    try:
        repo = Repo(repo_path)
    except:
        repo_path_output = colored(repo_path, 'cyan')
        print("Failed to create Repo instance for " + repo_path_output)
    else:
        branch_output = colored('(' + branch + ')', 'magenta')
        remote_output = colored(remote, attrs=['underline'])
        print(' - Create and checkout branch ' + branch_output)
        try:
            origin = repo.remotes[remote]
            origin.fetch()
        except:
            print(' - Failed to fetch from remote ' + remote_output)
        else:
            try:
                default_branch = repo.create_head(branch, origin.refs[branch])
            except:
                print(' - Failed to create branch ' + branch_output)
            else:
                try:
                    default_branch.set_tracking_branch(origin.refs[branch])
                except:
                    print(' - Failed to set tracking branch ' + branch_output)
                else:
                    try:
                        default_branch.checkout()
                    except:
                        print(' - Failed to checkout branch ' + branch_output)

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
    try:
        repo = Repo(repo_path)
    except:
        repo_path_output = colored(repo_path, 'cyan')
        print("Failed to create Repo instance for " + repo_path_output)
    else:
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
                    print(' - Failed to checkout commit ' + commit_output)

def git_checkout_tag(repo_path, tag):
    """Checkout commit tag is pointing to"""
    try:
        repo = Repo(repo_path)
    except:
        repo_path_output = colored(repo_path, 'cyan')
        print("Failed to create Repo instance for " + repo_path_output)
    else:
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
    try:
        repo = Repo(repo_path)
    except:
        repo_path_output = colored(repo_path, 'cyan')
        print("Failed to create Repo instance for " + repo_path_output)
    else:
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
    try:
        repo = Repo(repo_path)
    except:
        repo_path_output = colored(repo_path, 'cyan')
        print("Failed to create Repo instance for " + repo_path_output)
    else:
        return repo.head.ref.name

def git_current_sha(repo_path):
    """Return current git sha for checked out commit"""
    try:
        repo = Repo(repo_path)
    except:
        repo_path_output = colored(repo_path, 'cyan')
        print("Failed to create Repo instance for " + repo_path_output)
    else:
        return repo.head.commit.hexsha

def git_reset_head(repo_path):
    """Reset head of repo, discarding changes"""
    try:
        repo = Repo(repo_path)
    except:
        repo_path_output = colored(repo_path, 'cyan')
        print("Failed to create Repo instance for " + repo_path_output)
    else:
        repo.head.reset(index=True, working_tree=True)

def git_fetch(repo_path):
    """Fetch all remotes, tags, and prune obsolete branches"""
    try:
        repo = Repo(repo_path)
    except:
        repo_path_output = colored(repo_path, 'cyan')
        print("Failed to create Repo instance for " + repo_path_output)
    else:
        try:
            repo.git.fetch('--all', '--prune', '--tags')
        except:
            print(' - Failed to fetch')

def git_has_untracked_files(repo_path):
    """Check if there are untracked files"""
    try:
        repo = Repo(repo_path)
    except:
        repo_path_output = colored(repo_path, 'cyan')
        print("Failed to create Repo instance for " + repo_path_output)
    else:
        if repo.untracked_files:
            return True
        else:
            return False

def git_is_detached(repo_path):
    """Check if HEAD is detached"""
    if not os.path.isdir(repo_path):
        return False
    else:
        try:
            repo = Repo(repo_path)
        except:
            repo_path_output = colored(repo_path, 'cyan')
            print("Failed to create Repo instance for " + repo_path_output)
        else:
            return repo.head.is_detached

def git_is_dirty(repo_path):
    """Check if repo is dirty"""
    if not os.path.isdir(repo_path):
        return False
    else:
        try:
            repo = Repo(repo_path)
        except:
            repo_path_output = colored(repo_path, 'cyan')
            print("Failed to create Repo instance for " + repo_path_output)
        else:
            return repo.is_dirty()

def git_pull(repo_path):
    """Pull from remote branch"""
    try:
        repo = Repo(repo_path)
    except:
        repo_path_output = colored(repo_path, 'cyan')
        print("Failed to create Repo instance for " + repo_path_output)
    else:
        if not repo.head.is_detached:
            try:
                print(' - Pulling latest changes')
                print(repo.git.pull())
            except:
                print(' - Failed to pull latest changes')

def git_pull_remote_branch(repo_path, remote, branch):
    """Pull from remote branch"""
    try:
        repo = Repo(repo_path)
    except:
        repo_path_output = colored(repo_path, 'cyan')
        print("Failed to create Repo instance for " + repo_path_output)
    else:
        if not repo.head.is_detached:
            try:
                print(' - Pulling latest changes')
                print(repo.git.pull(remote, branch))
            except:
                print(' - Failed to pull latest changes')

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
    try:
        repo = Repo(repo_path)
    except:
        repo_path_output = colored(repo_path, 'cyan')
        print("Failed to create Repo instance for " + repo_path_output)
    else:
        if repo.is_dirty():
            print(' - Stashing current changes')
            repo.git.stash()
        else:
            print(' - No changes to stash')

def git_status(repo_path):
    """Print git status"""
    try:
        repo = Repo(repo_path)
    except:
        repo_path_output = colored(repo_path, 'cyan')
        print("Failed to create Repo instance for " + repo_path_output)
    else:
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
