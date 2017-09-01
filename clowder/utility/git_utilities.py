"""Git utilities"""
import os
import shutil
import sys
from git import Repo
from termcolor import colored, cprint

# Disable errors shown by pylint for no specified exception types
# pylint: disable=W0702

def git_add(repo_path, files):
    """Add files to git index"""
    repo = _repo(repo_path)
    try:
        print(' - Add files to git index')
        print(repo.git.add(files))
    except:
        cprint(' - Failed to add files to git index', 'red')
        print('')
        sys.exit(1)

def git_branches(repo_path):
    """Get list of current branches"""
    repo = _repo(repo_path)
    return repo.branches

def git_checkout(repo_path, ref):
    """Checkout git ref"""
    repo = _repo(repo_path)
    ref_output = colored('(' + ref + ')', 'magenta')
    try:
        print(' - Check out ' + ref_output)
        print(repo.git.checkout(ref))
    except:
        message = colored(' - Failed to checkout ref ', 'red')
        print(message + ref_output)
        print('')
        sys.exit(1)

def git_commit(repo_path, message):
    """Commit current changes"""
    repo = _repo(repo_path)
    print(' - Commit current changes')
    print(repo.git.commit(message=message))

def git_create_repo(url, repo_path, remote, ref, depth=0):
    """Clone git repo from url at path"""
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        if not os.path.isdir(repo_path):
            os.makedirs(repo_path)
        repo_path_output = colored(repo_path, 'cyan')
        try:
            print(' - Clone repo at ' + repo_path_output)
            Repo.init(repo_path)
        except:
            cprint(' - Failed to initialize repository', 'red')
            print('')
            shutil.rmtree(repo_path)
            sys.exit(1)
        else:
            repo = _repo(repo_path)
            remote_names = [r.name for r in repo.remotes]
            remote_output = colored(remote, 'yellow')
            if remote not in remote_names:
                try:
                    print(" - Create remote " + remote_output)
                    repo.create_remote(remote, url)
                except:
                    message = colored(" - Failed to create remote ", 'red')
                    print(message + remote_output)
                    print('')
                    shutil.rmtree(repo_path)
                    sys.exit(1)
            _checkout_ref(repo_path, ref, remote, depth)

def git_create_remote(repo_path, remote, url):
    """Create new remote"""
    repo = _repo(repo_path)
    remote_names = [r.name for r in repo.remotes]
    if remote not in remote_names:
        remote_output = colored(remote, 'yellow')
        try:
            print(" - Create remote " + remote_output)
            repo.create_remote(remote, url)
        except:
            message = colored(" - Failed to create remote ", 'red')
            print(message + remote_output)
            print('')
            sys.exit(1)

def git_current_branch(repo_path):
    """Return currently checked out branch of project"""
    repo = _repo(repo_path)
    return repo.head.ref.name

def git_current_sha(repo_path):
    """Return current git sha for checked out commit"""
    repo = _repo(repo_path)
    return repo.head.commit.hexsha

def git_fetch(repo_path):
    """Perform a git fetch"""
    repo = _repo(repo_path)
    try:
        repo.git.fetch()
    except:
        return

def git_fetch_remote(repo_path, remote, ref, depth):
    """Fetch from a specific remote"""
    repo = _repo(repo_path)
    try:
        truncated_ref = _truncate_ref(ref)
        remote_output = colored(remote, 'yellow')
        if depth == 0:
            print(' - Fetch all data from ' + remote_output)
            repo.git.fetch(remote, '--all', '--prune', '--tags')
        else:
            ref_output = colored('(' + truncated_ref + ')', 'magenta')
            print(' - Fetch data from ' + remote_output + ' ' + ref_output)
            repo.git.fetch(remote, truncated_ref, depth=depth)
    except:
        cprint(' - Failed to fetch remote', 'red')
        print('')
        sys.exit(1)

def git_herd(repo_path, url, remote, ref, depth):
    """Check if there are untracked files"""
    ref_type = _ref_type(ref)
    if ref_type is 'branch':
        git_create_remote(repo_path, remote, url)
        _checkout_ref(repo_path, ref, remote, depth)
        branch = _truncate_ref(ref)
        _pull_remote_branch(repo_path, remote, branch)
    elif ref_type is 'tag' or ref_type is 'sha':
        git_create_remote(repo_path, remote, url)
        _checkout_ref(repo_path, ref, remote, depth)
    else:
        cprint('Unknown ref ' + ref, 'red')

def git_is_detached(repo_path):
    """Check if HEAD is detached"""
    if not os.path.isdir(repo_path):
        return False
    else:
        repo = _repo(repo_path)
        return repo.head.is_detached

def git_is_dirty(repo_path):
    """Check if repo is dirty"""
    if not os.path.isdir(repo_path):
        return False
    else:
        repo = _repo(repo_path)
        return repo.is_dirty()

def git_new_local_commits(repo_path):
    """Returns the number of new commits upstream"""
    repo = _repo(repo_path)
    try:
        local_branch = repo.active_branch
    except:
        return 0
    if local_branch is None:
        return 0
    else:
        tracking_branch = local_branch.tracking_branch()
        if tracking_branch is None:
            return 0
        else:
            try:
                rev_list_count = repo.git.rev_list('--count', '--left-right', local_branch.name + '...' + tracking_branch.name)
                count = str(rev_list_count).split()[0]
                return count
            except:
                return 0

def git_new_upstream_commits(repo_path):
    """Returns the number of new commits upstream"""
    repo = _repo(repo_path)
    try:
        local_branch = repo.active_branch
    except:
        return 0
    if local_branch is None:
        return 0
    else:
        tracking_branch = local_branch.tracking_branch()
        if tracking_branch is None:
            return 0
        else:
            try:
                rev_list_count = repo.git.rev_list('--count', '--left-right', local_branch.name + '...' + tracking_branch.name)
                count = str(rev_list_count).split()[1]
                return count
            except:
                return 0

def git_prune(repo_path, branch, default_ref, force):
    """Prune branch in repository"""
    repo = _repo(repo_path)
    branch_output = colored('(' + branch + ')', 'magenta')
    if branch in repo.heads:
        prune_branch = repo.heads[branch]
        if repo.head.ref == prune_branch:
            truncated_ref = _truncate_ref(default_ref)
            ref_output = colored('(' + truncated_ref + ')', 'magenta')
            try:
                print(' - Checkout branch ' + ref_output)
                repo.git.checkout(truncated_ref)
            except:
                message = colored(' - Failed to checkout ref', 'red')
                print(message + ref_output)
                print('')
                sys.exit(1)
        try:
            print(' - Delete branch ' + branch_output)
            repo.delete_head(branch, force=force)
        except:
            message = colored(' - Failed to delete branch ', 'red')
            print(message + branch_output)
            print('')
            sys.exit(1)
    else:
        print(' - Branch ' + branch_output + " doesn't exist")

def git_prune_remote(repo_path, branch, remote):
    """Prune remote branch in repository"""
    repo = _repo(repo_path)
    remote_output = colored(remote, 'yellow')
    try:
        print(' - Fetch data from ' + remote_output)
        origin = repo.remotes[remote]
        origin.fetch()
        branch_output = colored('(' + branch + ')', 'magenta')
        if branch in origin.refs:
            try:
                print(' - Delete branch ' + branch_output)
                repo.git.push(remote, '--delete', branch)
            except:
                message = colored(' - Failed to delete branch ', 'red')
                print(message + branch_output)
                print('')
                sys.exit(1)
        else:
            print(' - Branch ' + branch_output + " doesn't exist")
    except:
        message = colored(' - Failed to fetch from remote ', 'red')
        print(message + remote_output)
        print('')
        sys.exit(1)

def git_pull(repo_path):
    """Pull from remote branch"""
    repo = _repo(repo_path)
    if not repo.head.is_detached:
        try:
            print(' - Pull latest changes')
            print(repo.git.pull())
        except:
            cprint(' - Failed to pull latest changes', 'red')
            print('')
            sys.exit(1)
    else:
        print(' - HEAD is detached')

def git_push(repo_path):
    """Push to remote branch"""
    repo = _repo(repo_path)
    if not repo.head.is_detached:
        try:
            print(' - Pushing local changes')
            print(repo.git.push())
        except:
            cprint(' - Failed to push local changes', 'red')
            print('')
            sys.exit(1)
    else:
        print(' - HEAD is detached')

def git_reset_head(repo_path):
    """Reset head of repo, discarding changes"""
    repo = _repo(repo_path)
    repo.head.reset(index=True, working_tree=True)

def git_start(repo_path, remote, branch, depth):
    """Start new branch in repository"""
    repo = _repo(repo_path)
    correct_branch = False
    if branch in repo.heads:
        branch_output = colored('(' + branch + ')', 'magenta')
        print(' - ' + branch_output + ' already exists')
        default_branch = repo.heads[branch]
        try:
            not_detached = not repo.head.is_detached
            same_branch = repo.head.ref == default_branch
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
                    message = colored(' - Failed to checkout branch ', 'red')
                    print(message + branch_output)
                    print('')
                    sys.exit(1)
    else:
        _create_checkout_branch(repo_path, branch, remote, depth)

def git_stash(repo_path):
    """Stash current changes in repository"""
    repo = _repo(repo_path)
    if repo.is_dirty():
        print(' - Stashing current changes')
        repo.git.stash()
    else:
        print(' - No changes to stash')

def git_status(repo_path):
    """Print git status"""
    repo = _repo(repo_path)
    print(repo.git.status())

def _checkout_branch(repo_path, branch, remote, depth):
    """Checkout branch, and create if it doesn't exist"""
    repo = _repo(repo_path)
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
                branch_output = colored('(' + branch + ')', 'magenta')
                try:
                    print(' - Checkout branch ' + branch_output)
                    default_branch.checkout()
                except:
                    message = colored(' - Failed to checkout branch ', 'red')
                    print(message + branch_output)
                    print('')
                    sys.exit(1)
    else:
        _create_tracking_branch(repo_path, branch, remote, depth)

def _checkout_ref(repo_path, ref, remote, depth):
    """Checkout branch, tag, or commit from sha"""
    ref_type = _ref_type(ref)
    if ref_type is 'branch':
        branch = _truncate_ref(ref)
        _checkout_branch(repo_path, branch, remote, depth)
    elif ref_type is 'tag':
        tag = _truncate_ref(ref)
        _fetch_remote_ref(repo_path, remote, ref, depth)
        _checkout_tag(repo_path, tag)
    elif ref_type is 'sha':
        _fetch_remote_ref(repo_path, remote, ref, depth)
        _checkout_sha(repo_path, ref)
    else:
        ref_output = colored('(' + ref + ')', 'magenta')
        print('Unknown ref ' + ref_output)

def _checkout_sha(repo_path, sha):
    """Checkout commit by sha"""
    repo = _repo(repo_path)
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
            commit_output = colored('(' + sha + ')', 'magenta')
            try:
                print(' - Checkout commit ' + commit_output)
                repo.git.checkout(sha)
            except:
                message = colored(' - Failed to checkout commit ', 'red')
                print(message + commit_output)
                print('')
                sys.exit(1)

def _checkout_tag(repo_path, tag):
    """Checkout commit tag is pointing to"""
    repo = _repo(repo_path)
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

def _create_checkout_branch(repo_path, branch, remote, depth):
    """Create and checkout local branch"""
    repo = _repo(repo_path)
    remote_output = colored(remote, 'yellow')
    try:
        print(' - Fetch data from ' + remote_output)
        origin = repo.remotes[remote]
        if depth == 0:
            origin.fetch()
        else:
            origin.fetch(depth=depth)
    except:
        message = colored(' - Failed to fetch from remote ', 'red')
        print(message + remote_output)
        print('')
        sys.exit(1)
    else:
        branch_output = colored('(' + branch + ')', 'magenta')
        try:
            print(' - Create branch ' + branch_output)
            default_branch = repo.create_head(branch)
        except:
            message = colored(' - Failed to create branch ', 'red')
            print(message + branch_output)
            print('')
            sys.exit(1)
        else:
            try:
                print(' - Checkout branch ' + branch_output)
                default_branch.checkout()
            except:
                message = colored(' - Failed to checkout branch ', 'red')
                print(message + branch_output)
                print('')
                sys.exit(1)

def _create_tracking_branch(repo_path, branch, remote, depth):
    """Create and checkout tracking branch"""
    repo = _repo(repo_path)
    branch_output = colored('(' + branch + ')', 'magenta')
    remote_output = colored(remote, 'yellow')
    try:
        origin = repo.remotes[remote]
        if depth == 0:
            print(' - Fetch data from ' + remote_output)
            origin.fetch()
        else:
            print(' - Fetch data from ' + remote_output + ' ' + branch_output)
            origin.fetch(branch, depth=depth)
    except:
        message = colored(' - Failed to fetch from remote ', 'red')
        print(message + remote_output)
        print('')
        sys.exit(1)
    else:
        try:
            print(' - Create branch ' + branch_output)
            default_branch = repo.create_head(branch, origin.refs[branch])
        except:
            message = colored(' - Failed to create branch ', 'red')
            print(message + branch_output)
            print('')
            sys.exit(1)
        else:
            try:
                print(' - Set tracking branch')
                default_branch.set_tracking_branch(origin.refs[branch])
            except:
                message = colored(' - Failed to set tracking branch ', 'red')
                print(message + branch_output)
                print('')
                sys.exit(1)
            else:
                try:
                    print(' - Checkout branch ' + branch_output)
                    default_branch.checkout()
                except:
                    message = colored(' - Failed to checkout branch ', 'red')
                    print(message + branch_output)
                    print('')
                    sys.exit(1)

def _fetch_remote_ref(repo_path, remote, ref, depth):
    """Fetch from a specific remote ref"""
    repo = _repo(repo_path)
    try:
        remote_output = colored(remote, 'yellow')
        if depth == 0:
            print(' - Fetch all data from ' + remote_output)
            repo.git.fetch('--all', '--prune', '--tags')
        else:
            ref_output = colored('(' + ref + ')', 'magenta')
            print(' - Fetch data from ' + remote_output + ' ' + ref_output)
            origin = repo.remotes[remote]
            origin.fetch(_truncate_ref(ref), depth=depth)
    except:
        cprint(' - Failed to fetch remote ref', 'red')
        print('')
        sys.exit(1)

def _pull_remote_branch(repo_path, remote, branch):
    """Pull from remote branch"""
    repo = _repo(repo_path)
    if not repo.head.is_detached:
        try:
            branch_output = colored('(' + branch + ')', 'magenta')
            remote_output = colored(remote, 'yellow')
            print(' - Pull latest changes from ' + remote_output + ' ' + branch_output)
            print(repo.git.pull(remote, branch))
        except:
            cprint(' - Failed to pull latest changes', 'red')
            print('')
            sys.exit(1)

def _ref_type(ref):
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

def _repo(repo_path):
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

def _truncate_ref(ref):
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
