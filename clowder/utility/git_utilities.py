"""Git utilities"""
import os
import shutil
import sys
from git import Repo
from termcolor import colored, cprint
from clowder.utility.clowder_utilities import execute_command
from clowder.utility.print_utilities import (
    format_command,
    format_path,
    format_ref_string,
    format_remote_string,
    print_command_failed_error,
    print_error
)

# Disable errors shown by pylint for no specified exception types
# pylint: disable=W0702
# Disable errors shown by pylint for too many branches
# pylint: disable=R0912
# Disable errors shown by pylint for catching too general exception Exception
# pylint: disable=W0703
# Disable errors shown by pylint for too many statements
# pylint: disable=R0915

def git_add(repo_path, files):
    """Add files to git index"""
    repo = _repo(repo_path)
    try:
        print(' - Add files to git index')
        print(repo.git.add(files))
    except Exception as err:
        cprint(' - Failed to add files to git index', 'red')
        print_error(err)
        sys.exit(1)

def git_branches(repo_path):
    """Get list of current branches"""
    repo = _repo(repo_path)
    return repo.branches

def git_checkout(repo_path, truncated_ref):
    """Checkout git ref"""
    repo = _repo(repo_path)
    ref_output = format_ref_string(truncated_ref)
    try:
        print(' - Check out ' + ref_output)
        print(repo.git.checkout(truncated_ref))
    except Exception as err:
        message = colored(' - Failed to checkout ref ', 'red')
        print(message + ref_output)
        print_error(err)
        sys.exit(1)

def git_commit(repo_path, message):
    """Commit current changes"""
    repo = _repo(repo_path)
    print(' - Commit current changes')
    print(repo.git.commit(message=message))

def git_create_repo(url, repo_path, remote, ref, depth=0):
    """Clone git repo from url at path"""
    if not git_existing_repository(repo_path):
        if not os.path.isdir(repo_path):
            os.makedirs(repo_path)
        repo_path_output = format_path(repo_path)
        try:
            print(' - Clone repo at ' + repo_path_output)
            Repo.init(repo_path)
        except Exception as err:
            cprint(' - Failed to initialize repository', 'red')
            print_error(err)
            try:
                shutil.rmtree(repo_path)
            except:
                message = colored(" - Failed to remove directory ", 'red')
                print(message + format_path(repo_path))
            finally:
                print()
                sys.exit(1)
        else:
            repo = _repo(repo_path)
            remote_names = [r.name for r in repo.remotes]
            if remote in remote_names:
                _checkout_ref(repo_path, ref, remote, depth)
            else:
                remote_output = format_remote_string(remote)
                print(" - Create remote " + remote_output)
                try:
                    repo.create_remote(remote, url)
                except Exception as err:
                    message = colored(" - Failed to create remote ", 'red')
                    print(message + remote_output)
                    print_error(err)
                    try:
                        shutil.rmtree(repo_path)
                    except:
                        message = colored(" - Failed to remove directory ", 'red')
                        print(message + format_path(repo_path))
                    finally:
                        print()
                        sys.exit(1)
                else:
                    _checkout_ref(repo_path, ref, remote, depth)

def git_create_remote(repo_path, remote, url):
    """Create new remote"""
    repo = _repo(repo_path)
    remote_names = [r.name for r in repo.remotes]
    if remote not in remote_names:
        remote_output = format_remote_string(remote)
        try:
            print(" - Create remote " + remote_output)
            repo.create_remote(remote, url)
        except Exception as err:
            message = colored(" - Failed to create remote ", 'red')
            print(message + remote_output)
            print_error(err)
            sys.exit(1)

def git_current_branch(repo_path):
    """Return currently checked out branch of project"""
    repo = _repo(repo_path)
    return repo.head.ref.name

def git_existing_repository(path):
    """Check if a git repository exists"""
    return os.path.isdir(os.path.join(path, '.git'))

def git_existing_local_branch(repo_path, branch):
    """Check if local branch exists"""
    repo = _repo(repo_path)
    return branch in repo.heads

def git_existing_remote_branch(repo_path, branch, remote):
    """Check if remote branch exists"""
    repo = _repo(repo_path)
    origin = repo.remotes[remote]
    return branch in origin.refs

def git_fetch_all(repo_path):
    """Fetch all upstream changes"""
    print(' - Fetch all upstream changes')
    command = ['git', 'fetch', '--all', '--prune', '--tags']
    return_code = execute_command(command, repo_path)
    if return_code != 0:
        cprint(' - Failed to fetch', 'red')
        print_command_failed_error(command)
        sys.exit(return_code)

def git_fetch_remote(repo_path, remote, depth):
    """Fetch from a specific remote"""
    remote_output = format_remote_string(remote)
    print(' - Fetch from ' + remote_output)
    if depth == 0:
        command = ['git', 'fetch', remote, '--prune', '--tags']
    else:
        command = ['git', 'fetch', remote, '--depth', str(depth), '--prune', '--tags']
    return_code = execute_command(command, repo_path)
    if return_code != 0:
        cprint(' - Failed to fetch remote ', remote_output, 'red')
        print_command_failed_error(command)
        sys.exit(return_code)

def git_fetch_silent(repo_path):
    """Perform a git fetch"""
    command = ['git', 'fetch', '--all', '--prune', '--tags']
    return_code = execute_command(command, repo_path)
    if return_code != 0:
        cprint(' - Failed to fetch', 'red')
        print_command_failed_error(command)
        sys.exit(return_code)

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
                branches = local_branch.name + '...' + tracking_branch.name
                rev_list_count = repo.git.rev_list('--count', '--left-right', branches)
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
                branches = local_branch.name + '...' + tracking_branch.name
                rev_list_count = repo.git.rev_list('--count', '--left-right', branches)
                count = str(rev_list_count).split()[1]
                return count
            except:
                return 0

def git_prune_local(repo_path, branch, default_ref, force):
    """Prune branch in repository"""
    repo = _repo(repo_path)
    branch_output = format_ref_string(branch)
    if branch in repo.heads:
        prune_branch = repo.heads[branch]
        if repo.head.ref == prune_branch:
            truncated_ref = _truncate_ref(default_ref)
            ref_output = format_ref_string(truncated_ref)
            try:
                print(' - Checkout branch ' + ref_output)
                repo.git.checkout(truncated_ref)
            except Exception as err:
                message = colored(' - Failed to checkout ref', 'red')
                print(message + ref_output)
                print_error(err)
                sys.exit(1)
            else:
                try:
                    print(' - Delete local branch ' + branch_output)
                    repo.delete_head(branch, force=force)
                except Exception as err:
                    message = colored(' - Failed to delete local branch ', 'red')
                    print(message + branch_output)
                    print_error(err)
                    sys.exit(1)
        else:
            try:
                print(' - Delete local branch ' + branch_output)
                repo.delete_head(branch, force=force)
            except Exception as err:
                message = colored(' - Failed to delete local branch ', 'red')
                print(message + branch_output)
                print_error(err)
                sys.exit(1)
    else:
        print(' - Local branch ' + branch_output + " doesn't exist")

def git_prune_remote(repo_path, branch, remote):
    """Prune remote branch in repository"""
    repo = _repo(repo_path)
    remote_output = format_remote_string(remote)
    try:
        origin = repo.remotes[remote]
    except Exception as err:
        message = colored(' - No existing remote ', 'red')
        print(message + remote_output)
        print_error(err)
        sys.exit(1)
    else:
        branch_output = format_ref_string(branch)
        if branch in origin.refs:
            try:
                print(' - Delete remote branch ' + branch_output)
                repo.git.push(remote, '--delete', branch)
            except Exception as err:
                message = colored(' - Failed to delete remote branch ', 'red')
                print(message + branch_output)
                print_error(err)
                sys.exit(1)
        else:
            print(' - Remote branch ' + branch_output + " doesn't exist")

def git_pull(repo_path):
    """Pull from remote branch"""
    repo = _repo(repo_path)
    if not repo.head.is_detached:
        try:
            print(' - Pull latest changes')
            print(repo.git.pull())
        except Exception as err:
            cprint(' - Failed to pull latest changes', 'red')
            print_error(err)
            sys.exit(1)
    else:
        print(' - HEAD is detached')

def git_push(repo_path):
    """Push to remote branch"""
    repo = _repo(repo_path)
    if not repo.head.is_detached:
        try:
            print(' - Push local changes')
            print(repo.git.push())
        except Exception as err:
            cprint(' - Failed to push local changes', 'red')
            print_error(err)
            sys.exit(1)
    else:
        print(' - HEAD is detached')

def git_reset_head(repo_path):
    """Reset head of repo, discarding changes"""
    repo = _repo(repo_path)
    repo.head.reset(index=True, working_tree=True)

def git_sha_long(repo_path):
    """Return long sha for currently checked out commit"""
    repo = _repo(repo_path)
    return repo.head.commit.hexsha

def git_sha_short(repo_path):
    """Return short sha of currently checked out commit"""
    repo = _repo(repo_path)
    sha = repo.head.commit.hexsha
    return repo.git.rev_parse(sha, short=True)

def git_start(repo_path, remote, branch, depth, tracking):
    """Start new branch in repository"""
    repo = _repo(repo_path)
    correct_branch = False
    if branch in repo.heads:
        branch_output = format_ref_string(branch)
        print(' - ' + branch_output + ' already exists')
        default_branch = repo.heads[branch]
        try:
            not_detached = not repo.head.is_detached
            same_branch = repo.head.ref == default_branch
        except Exception as err:
            pass
        else:
            if not_detached and same_branch:
                print(' - On correct branch')
                correct_branch = True
                if tracking:
                    _create_remote_tracking_branch(repo_path, branch, remote, depth)
        finally:
            if not correct_branch:
                try:
                    print(' - Checkout branch ' + branch_output)
                    default_branch.checkout()
                except Exception as err:
                    message = colored(' - Failed to checkout branch ', 'red')
                    print(message + branch_output)
                    print_error(err)
                    sys.exit(1)
                else:
                    if tracking:
                        _create_remote_tracking_branch(repo_path, branch, remote, depth)
    else:
        _create_checkout_branch(repo_path, branch, remote, depth)
        if tracking:
            _create_remote_tracking_branch(repo_path, branch, remote, depth)

def git_stash(repo_path):
    """Stash current changes in repository"""
    repo = _repo(repo_path)
    if repo.is_dirty():
        print(' - Stash current changes')
        repo.git.stash()
    else:
        print(' - No changes to stash')

def git_status(repo_path):
    """Print git status"""
    command = ['git', 'status', '-vv']
    print(format_command(command))
    return_code = execute_command(command, repo_path)
    if return_code != 0:
        cprint(' - Failed to print status', 'red')
        print_command_failed_error(command)
        sys.exit(return_code)

def _checkout_branch(repo_path, branch, remote, depth):
    """Checkout branch, and create if it doesn't exist"""
    repo = _repo(repo_path)
    correct_branch = False
    if branch in repo.heads:
        default_branch = repo.heads[branch]
        try:
            not_detached = not repo.head.is_detached
            same_branch = repo.head.ref == default_branch
        except Exception as err:
            pass
        else:
            if not_detached and same_branch:
                print(' - On default branch')
                correct_branch = True
        finally:
            if not correct_branch:
                branch_output = format_ref_string(branch)
                try:
                    print(' - Checkout branch ' + branch_output)
                    default_branch.checkout()
                except Exception as err:
                    message = colored(' - Failed to checkout branch ', 'red')
                    print(message + branch_output)
                    print_error(err)
                    sys.exit(1)
    else:
        _create_local_tracking_branch(repo_path, branch, remote, depth)

def _checkout_ref(repo_path, ref, remote, depth):
    """Checkout branch, tag, or commit from sha"""
    ref_type = _ref_type(ref)
    if ref_type is 'branch':
        branch = _truncate_ref(ref)
        _checkout_branch(repo_path, branch, remote, depth)
    elif ref_type is 'tag':
        git_fetch_remote_ref(repo_path, remote, ref, depth)
        tag = _truncate_ref(ref)
        _checkout_tag(repo_path, tag)
    elif ref_type is 'sha':
        git_fetch_remote_ref(repo_path, remote, ref, depth)
        _checkout_sha(repo_path, ref)
    else:
        ref_output = format_ref_string(ref)
        print('Unknown ref ' + ref_output)

def _checkout_sha(repo_path, sha):
    """Checkout commit by sha"""
    repo = _repo(repo_path)
    correct_commit = False
    try:
        same_sha = repo.head.commit.hexsha == sha
        is_detached = repo.head.is_detached
    except Exception as err:
        pass
    else:
        if same_sha and is_detached:
            print(' - On correct commit')
            correct_commit = True
    finally:
        if not correct_commit:
            commit_output = format_ref_string(sha)
            try:
                print(' - Checkout commit ' + commit_output)
                repo.git.checkout(sha)
            except Exception as err:
                message = colored(' - Failed to checkout commit ', 'red')
                print(message + commit_output)
                print_error(err)
                sys.exit(1)

def _checkout_tag(repo_path, tag):
    """Checkout commit tag is pointing to"""
    repo = _repo(repo_path)
    tag_output = format_ref_string(tag)
    correct_commit = False
    if tag in repo.tags:
        try:
            same_commit = repo.head.commit == repo.tags[tag].commit
            is_detached = repo.head.is_detached
        except Exception as err:
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
                except Exception as err:
                    message = colored(' - Failed to checkout tag ', 'red')
                    print(message + tag_output)
                    print_error(err)
                    sys.exit(1)
    else:
        print(' - No existing tag ' + tag_output)

def _create_checkout_branch(repo_path, branch, remote, depth):
    """Create and checkout local branch"""
    repo = _repo(repo_path)
    remote_output = format_remote_string(remote)
    print(' - Fetch from ' + remote_output)
    if depth == 0:
        command = ['git', 'fetch', remote, '--prune', '--tags']
    else:
        command = ['git', 'fetch', remote, '--depth', str(depth), '--prune', '--tags']
    return_code = execute_command(command, repo_path)
    if return_code != 0:
        message = colored(' - Failed to fetch from ', 'red')
        print(message + remote_output)
        print_command_failed_error(command)
        sys.exit(return_code)
    branch_output = format_ref_string(branch)
    try:
        print(' - Create branch ' + branch_output)
        default_branch = repo.create_head(branch)
    except Exception as err:
        message = colored(' - Failed to create branch ', 'red')
        print(message + branch_output)
        print_error(err)
        sys.exit(1)
    else:
        try:
            print(' - Checkout branch ' + branch_output)
            default_branch.checkout()
        except Exception as err:
            message = colored(' - Failed to checkout branch ', 'red')
            print(message + branch_output)
            print_error(err)
            sys.exit(1)

def _create_local_tracking_branch(repo_path, branch, remote, depth):
    """Create and checkout tracking branch"""
    repo = _repo(repo_path)
    branch_output = format_ref_string(branch)
    remote_output = format_remote_string(remote)
    try:
        origin = repo.remotes[remote]
    except Exception as err:
        message = colored(' - No existing remote ', 'red')
        print(message + remote_output)
        print_error(err)
        sys.exit(1)
    else:
        if depth == 0:
            print(' - Fetch from ' + remote_output)
            command = ['git', 'fetch', remote, '--prune', '--tags']
        else:
            print(' - Fetch from ' + remote_output + ' ' + branch_output)
            command = ['git', 'fetch', remote, branch, '--depth', str(depth),
                       '--prune', '--tags']
        return_code = execute_command(command, repo_path)
        if return_code != 0:
            message = colored(' - Failed to fetch from ', 'red')
            print(message + remote_output)
            print_command_failed_error(command)
            sys.exit(return_code)
        try:
            print(' - Create branch ' + branch_output)
            default_branch = repo.create_head(branch, origin.refs[branch])
        except Exception as err:
            message = colored(' - Failed to create branch ', 'red')
            print(message + branch_output)
            print_error(err)
            sys.exit(1)
        else:
            try:
                print(' - Set tracking branch ' + branch_output +
                      ' -> ' + remote_output + ' ' + branch_output)
                default_branch.set_tracking_branch(origin.refs[branch])
            except Exception as err:
                message = colored(' - Failed to set tracking branch ', 'red')
                print(message + branch_output)
                print_error(err)
                sys.exit(1)
            else:
                try:
                    print(' - Checkout branch ' + branch_output)
                    default_branch.checkout()
                except Exception as err:
                    message = colored(' - Failed to checkout branch ', 'red')
                    print(message + branch_output)
                    print_error(err)
                    sys.exit(1)

def _create_remote_tracking_branch(repo_path, branch, remote, depth):
    """Create remote tracking branch"""
    repo = _repo(repo_path)
    branch_output = format_ref_string(branch)
    remote_output = format_remote_string(remote)
    try:
        origin = repo.remotes[remote]
    except Exception as err:
        message = colored(' - No existing remote ', 'red')
        print(message + remote_output)
        print_error(err)
        sys.exit(1)
    else:
        print(' - Fetch from ' + remote_output)
        if depth == 0:
            command = ['git', 'fetch', remote, '--prune', '--tags']
        else:
            command = ['git', 'fetch', remote, '--depth', str(depth),
                       '--prune', '--tags']
        return_code = execute_command(command, repo_path)
        if return_code != 0:
            message = colored(' - Failed to fetch from ', 'red')
            print(message + remote_output)
            print_command_failed_error(command)
            sys.exit(return_code)
        if branch in origin.refs:
            try:
                repo.git.config('--get', 'branch.' + branch + '.merge')
            except:
                message_1 = colored(' - Remote branch ', 'red')
                message_2 = colored(' already exists', 'red')
                print(message_1 + branch_output + message_2)
                print()
                sys.exit(1)
            else:
                print(' - Tracking branch ' + branch_output + ' already exists')
        else:
            try:
                print(' - Push remote branch ' + branch_output)
                repo.git.push(remote, branch)
            except Exception as err:
                message = colored(' - Failed to push remote branch ', 'red')
                print(message + branch_output)
                print_error(err)
                sys.exit(1)
            else:
                try:
                    print(' - Set tracking branch ' + branch_output +
                          ' -> ' + remote_output + ' ' + branch_output)
                    repo.active_branch.set_tracking_branch(origin.refs[branch])
                except Exception as err:
                    message = colored(' - Failed to set tracking branch ', 'red')
                    print(message + branch_output)
                    print_error(err)
                    sys.exit(1)

def git_fetch_remote_ref(repo_path, remote, ref, depth):
    """Fetch from a specific remote ref"""
    remote_output = format_remote_string(remote)
    if depth == 0:
        print(' - Fetch from ' + remote_output)
        message = colored(' - Failed to fetch from ', 'red')
        error = message + remote_output
        command = ['git', 'fetch', remote, '--prune', '--tags']
    else:
        ref_output = format_ref_string(ref)
        print(' - Fetch from ' + remote_output + ' ' + ref_output)
        message = colored(' - Failed to fetch from ', 'red')
        error = message + remote_output + ' ' + ref_output
        command = ['git', 'fetch', remote, _truncate_ref(ref),
                   '--depth', str(depth), '--prune']
    return_code = execute_command(command, repo_path)
    if return_code != 0:
        print(error)
        print_command_failed_error(command)
        sys.exit(return_code)

def git_validate_repo_state(repo_path):
    """Validate repo state"""
    if not git_existing_repository(repo_path):
        return True
    return not git_is_dirty(repo_path)

def _pull_remote_branch(repo_path, remote, branch):
    """Pull from remote branch"""
    repo = _repo(repo_path)
    if not repo.head.is_detached:
        try:
            branch_output = format_ref_string(branch)
            remote_output = format_remote_string(remote)
            print(' - Pull latest changes from ' + remote_output + ' ' + branch_output)
            print(repo.git.pull(remote, branch))
        except Exception as err:
            cprint(' - Failed to pull latest changes', 'red')
            print_error(err)
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
    except Exception as err:
        repo_path_output = format_path(repo_path)
        message = colored("Failed to create Repo instance for ", 'red')
        print(message + repo_path_output)
        print_error(err)
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
