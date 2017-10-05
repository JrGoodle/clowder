"""Git utilities"""
import sys
from git import Repo
from termcolor import colored, cprint
from clowder.utility.clowder_utilities import (
    execute_command,
    remove_directory_exit
)
from clowder.utility.print_utilities import (
    format_path,
    format_ref_string,
    format_remote_string,
    print_command_failed_error,
    print_error
)

# Disable errors shown by pylint for no specified exception types
# pylint: disable=W0702
# Disable errors shown by pylint for catching too general exception Exception
# pylint: disable=W0703

def _checkout_branch(repo_path, branch, remote, depth, fetch=True):
    """Checkout branch, and create if it doesn't exist"""
    repo = _repo(repo_path)
    correct_branch = False
    if branch not in repo.heads:
        _create_local_tracking_branch(repo_path, branch, remote, depth, fetch=fetch)
        return
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

def _checkout_branch_new_repo(repo_path, branch, remote, depth):
    """Checkout remote branch or fail and delete repo if it doesn't exist"""
    repo = _repo(repo_path)
    branch_output = format_ref_string(branch)
    remote_output = format_remote_string(remote)
    try:
        origin = repo.remotes[remote]
    except Exception as err:
        message = colored(' - No existing remote ', 'red')
        print(message + remote_output)
        print_error(err)
        remove_directory_exit(repo_path)
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
            remove_directory_exit(repo_path)
        try:
            remote_branch = origin.refs[branch]
        except:
            message = colored(' - No existing remote branch ', 'red')
            print(message + branch_output)
            remove_directory_exit(repo_path)
        else:
            print(' - Create branch ' + branch_output)
            try:
                default_branch = repo.create_head(branch, remote_branch)
            except Exception as err:
                message = colored(' - Failed to create branch ', 'red')
                print(message + branch_output)
                print_error(err)
                remove_directory_exit(repo_path)
            else:
                if not _set_tracking_branch(default_branch, remote_branch,
                                            branch_output, remote_output):
                    remove_directory_exit(repo_path)
                    return
                try:
                    print(' - Checkout branch ' + branch_output)
                    default_branch.checkout()
                except Exception as err:
                    message = colored(' - Failed to checkout branch ', 'red')
                    print(message + branch_output)
                    print_error(err)
                    remove_directory_exit(repo_path)

def _checkout_commit_new_repo(repo_path, commit, remote, depth):
    """Checkout commit or fail and delete repo if it doesn't exist"""
    repo = _repo(repo_path)
    commit_output = format_ref_string(commit)
    remote_output = format_remote_string(remote)
    try:
        repo.remotes[remote]
    except Exception as err:
        message = colored(' - No existing remote ', 'red')
        print(message + remote_output)
        print_error(err)
        remove_directory_exit(repo_path)
    else:
        if depth == 0:
            print(' - Fetch from ' + remote_output)
            command = ['git', 'fetch', remote, '--prune', '--tags']
        else:
            print(' - Fetch from ' + remote_output + ' ' + commit_output)
            command = ['git', 'fetch', remote, commit, '--depth', str(depth),
                       '--prune', '--tags']
        return_code = execute_command(command, repo_path)
        if return_code != 0:
            message = colored(' - Failed to fetch from ', 'red')
            print(message + remote_output)
            print_command_failed_error(command)
            remove_directory_exit(repo_path)
        print(' - Checkout commit ' + commit_output)
        try:
            repo.git.checkout(commit)
        except Exception as err:
            message = colored(' - Failed to checkout commit ', 'red')
            print(message + commit_output)
            print_error(err)
            remove_directory_exit(repo_path)

def _checkout_tag_new_repo(repo_path, tag, remote, depth):
    """Checkout tag or fail and delete repo if it doesn't exist"""
    repo = _repo(repo_path)
    tag_output = format_ref_string(tag)
    remote_output = format_remote_string(remote)
    try:
        origin = repo.remotes[remote]
    except Exception as err:
        message = colored(' - No existing remote ', 'red')
        print(message + remote_output)
        print_error(err)
        remove_directory_exit(repo_path)
    else:
        if depth == 0:
            print(' - Fetch from ' + remote_output)
            command = ['git', 'fetch', remote, '--prune', '--tags']
        else:
            print(' - Fetch from ' + remote_output + ' ' + tag_output)
            command = ['git', 'fetch', remote, tag, '--depth', str(depth),
                       '--prune', '--tags']
        return_code = execute_command(command, repo_path)
        if return_code != 0:
            message = colored(' - Failed to fetch from ', 'red')
            print(message + remote_output)
            print_command_failed_error(command)
            remove_directory_exit(repo_path)
        try:
            remote_tag = origin.tags[tag]
        except:
            message = colored(' - No existing remote tag ', 'red')
            print(message + tag_output)
            remove_directory_exit(repo_path)
        else:
            print(' - Checkout tag ' + tag_output)
            try:
                repo.git.checkout(remote_tag)
            except Exception as err:
                message = colored(' - Failed to checkout tag ', 'red')
                print(message + tag_output)
                print_error(err)
                remove_directory_exit(repo_path)

def _checkout_branch_herd_branch(repo_path, branch, default_ref, remote, depth):
    """Checkout remote branch or fall back to normal checkout branch if fails"""
    repo = _repo(repo_path)
    branch_output = format_ref_string(branch)
    remote_output = format_remote_string(remote)
    try:
        origin = repo.remotes[remote]
    except Exception as err:
        message = colored(' - No existing remote ', 'red')
        print(message + remote_output)
        print_error(err)
        remove_directory_exit(repo_path)
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
            remove_directory_exit(repo_path)
        try:
            remote_branch = origin.refs[branch]
        except:
            print(' - No existing remote branch ' + branch_output)
            _checkout_branch_new_repo(repo_path, _truncate_ref(default_ref), remote, depth)
        else:
            print(' - Create branch ' + branch_output)
            try:
                default_branch = repo.create_head(branch, remote_branch)
            except Exception as err:
                message = colored(' - Failed to create branch ', 'red')
                print(message + branch_output)
                print_error(err)
                remove_directory_exit(repo_path)
            else:
                if not _set_tracking_branch(default_branch, remote_branch,
                                            branch_output, remote_output):
                    remove_directory_exit(repo_path)
                    return
                try:
                    print(' - Checkout branch ' + branch_output)
                    default_branch.checkout()
                except Exception as err:
                    message = colored(' - Failed to checkout branch ', 'red')
                    print(message + branch_output)
                    print_error(err)
                    remove_directory_exit(repo_path)

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
    if tag not in repo.tags:
        print(' - No existing tag ' + tag_output)
        return
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

def _create_local_tracking_branch(repo_path, branch, remote, depth, fetch=True):
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
        if fetch:
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
            success = _set_tracking_branch(default_branch, origin.refs[branch],
                                           branch_output, remote_output)
            if not success:
                sys.exit(1)
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
                print(message_1 + branch_output + message_2 + '\n')
                sys.exit(1)
            else:
                print(' - Tracking branch ' + branch_output + ' already exists')
                return
        try:
            print(' - Push remote branch ' + branch_output)
            repo.git.push(remote, branch)
        except Exception as err:
            message = colored(' - Failed to push remote branch ', 'red')
            print(message + branch_output)
            print_error(err)
            sys.exit(1)
        else:
            success = _set_tracking_branch(repo.active_branch, origin.refs[branch],
                                           branch_output, remote_output)
            if not success:
                sys.exit(1)

def _pull_remote_branch(repo_path, remote, branch):
    """Pull from remote branch"""
    repo = _repo(repo_path)
    if repo.head.is_detached:
        print(' - HEAD is detached')
        return
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

def _set_tracking_branch(local_branch, remote_branch, branch_output, remote_output):
    """Set tracking branch"""
    try:
        print(' - Set tracking branch ' + branch_output +
              ' -> ' + remote_output + ' ' + branch_output)
        local_branch.set_tracking_branch(remote_branch)
        return True
    except Exception as err:
        message = colored(' - Failed to set tracking branch ', 'red')
        print(message + branch_output)
        print_error(err)
        return False
