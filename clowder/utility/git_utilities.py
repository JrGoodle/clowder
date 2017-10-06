"""Git utilities"""
import os
import subprocess
import sys
from git import Repo
from termcolor import colored, cprint
from clowder.utility.clowder_utilities import (
    execute_command,
    ref_type,
    remove_directory_exit,
    truncate_ref
)
from clowder.utility.print_utilities import (
    format_command,
    format_path,
    format_ref_string,
    format_remote_string,
    print_command_failed_error,
    print_error,
    print_remote_already_exists_error
)

# Disable errors shown by pylint for no specified exception types
# pylint: disable=W0702
# Disable errors shown by pylint for catching too general exception Exception
# pylint: disable=W0703
# Disable errors shown by pylint for too many arguments
# pylint: disable=R0913

def git_abort_rebase(repo_path):
    """Abort rebase"""
    if not git_is_rebase_in_progress(repo_path):
        return
    repo = _repo(repo_path)
    try:
        repo.git.rebase('--abort')
    except Exception as err:
        cprint(' - Failed to abort rebase', 'red')
        print_error(err)
        sys.exit(1)

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

def git_clean(repo_path, args=None):
    """Clean git directory"""
    repo = _repo(repo_path)
    clean_args = '-f'
    if args is not None:
        clean_args += args
    try:
        repo.git.clean(clean_args)
    except Exception as err:
        cprint(' - Failed to clean git repo', 'red')
        print_error(err)
        sys.exit(1)

def git_commit(repo_path, message):
    """Commit current changes"""
    repo = _repo(repo_path)
    print(' - Commit current changes')
    print(repo.git.commit(message=message))

def git_configure_remotes(repo_path, upstream_remote_name, upstream_remote_url,
                          fork_remote_name, fork_remote_url):
    """Configure remotes names for fork and upstream"""
    if not git_existing_repository(repo_path):
        return
    repo = _repo(repo_path)
    try:
        remotes = repo.remotes
    except:
        return
    else:
        for remote in remotes:
            if upstream_remote_url == repo.git.remote('get-url', remote.name):
                if remote.name != upstream_remote_name:
                    _rename_remote(repo_path, remote.name, upstream_remote_name)
                    continue
            if fork_remote_url == repo.git.remote('get-url', remote.name):
                if remote.name != fork_remote_name:
                    _rename_remote(repo_path, remote.name, fork_remote_name)
        remote_names = [r.name for r in repo.remotes]
        if upstream_remote_name in remote_names:
            if upstream_remote_url != repo.git.remote('get-url', upstream_remote_name):
                actual_url = repo.git.remote('get-url', upstream_remote_name)
                print_remote_already_exists_error(upstream_remote_name,
                                                  upstream_remote_url, actual_url)
                sys.exit(1)
        if fork_remote_name in remote_names:
            if fork_remote_url != repo.git.remote('get-url', fork_remote_name):
                actual_url = repo.git.remote('get-url', fork_remote_name)
                print_remote_already_exists_error(fork_remote_name,
                                                  fork_remote_url, actual_url)
                sys.exit(1)

def git_create_repo(repo_path, url, remote, ref, depth=0, recursive=False):
    """Clone git repo from url at path"""
    if git_existing_repository(repo_path):
        return
    if not os.path.isdir(repo_path):
        os.makedirs(repo_path)
    repo_path_output = format_path(repo_path)
    try:
        print(' - Clone repo at ' + repo_path_output)
        Repo.init(repo_path)
    except Exception as err:
        cprint(' - Failed to initialize repository', 'red')
        print_error(err)
        remove_directory_exit(repo_path)
    else:
        repo = _repo(repo_path)
        remote_names = [r.name for r in repo.remotes]
        if remote in remote_names:
            _checkout_ref(repo_path, ref, remote, depth)
            return
        return_code = _create_remote(repo_path, remote, url)
        if return_code != 0:
            remove_directory_exit(repo_path)
        if ref_type(ref) is 'branch':
            _checkout_new_repo_branch(repo_path, truncate_ref(ref), remote, depth)
        elif ref_type(ref) is 'tag':
            _checkout_new_repo_tag(repo_path, truncate_ref(ref), remote, depth)
        elif ref_type(ref) is 'sha':
            _checkout_new_repo_commit(repo_path, ref, remote, depth)
        else:
            ref_output = format_ref_string(ref)
            print('Unknown ref ' + ref_output)
        if recursive:
            git_submodule_update_recursive(repo_path, depth)

def git_current_branch(repo_path):
    """Return currently checked out branch of project"""
    repo = _repo(repo_path)
    return repo.head.ref.name

def git_existing_remote_branch(repo_path, branch, remote):
    """Check if remote branch exists"""
    repo = _repo(repo_path)
    try:
        origin = repo.remotes[remote]
    except:
        return False
    else:
        return branch in origin.refs

def git_existing_local_branch(repo_path, branch):
    """Check if local branch exists"""
    repo = _repo(repo_path)
    return branch in repo.heads

def git_existing_repository(path):
    """Check if a git repository exists"""
    return os.path.isdir(os.path.join(path, '.git'))

def git_existing_submodule(path):
    """Check if a git submodule exists"""
    return os.path.isfile(os.path.join(path, '.git'))

def git_fetch(repo_path, remote, ref=None, depth=0):
    """Fetch from a specific remote ref"""
    remote_output = format_remote_string(remote)
    if depth == 0:
        print(' - Fetch from ' + remote_output)
        message = colored(' - Failed to fetch from ', 'red')
        error = message + remote_output
        command = ['git', 'fetch', remote, '--prune', '--tags']
    else:
        if ref is None:
            command = ['git', 'fetch', remote, '--depth', str(depth), '--prune', '--tags']
            message = colored(' - Failed to fetch remote ', 'red')
            error = message + remote_output
        else:
            ref_output = format_ref_string(truncate_ref(ref))
            print(' - Fetch from ' + remote_output + ' ' + ref_output)
            message = colored(' - Failed to fetch from ', 'red')
            error = message + remote_output + ' ' + ref_output
            command = ['git', 'fetch', remote, truncate_ref(ref),
                       '--depth', str(depth), '--prune']
    return_code = execute_command(command, repo_path)
    if return_code != 0:
        print(error)
        print_command_failed_error(command)
    return return_code

def git_fetch_silent(repo_path):
    """Perform a git fetch"""
    command = ['git', 'fetch', '--all', '--prune', '--tags']
    return_code = execute_command(command, repo_path)
    if return_code != 0:
        cprint(' - Failed to fetch', 'red')
        print_command_failed_error(command)
        sys.exit(return_code)

def git_has_submodules(repo_path):
    """Repo has submodules"""
    repo = _repo(repo_path)
    if repo.submodules.count > 0:
        return True
    return False

def git_herd(repo_path, url, remote, ref, depth=0, recursive=False, fetch=True):
    """Herd ref"""
    if not git_existing_repository(repo_path):
        git_create_repo(repo_path, url, remote, ref, depth=depth, recursive=recursive)
        return
    if ref_type(ref) is 'branch':
        return_code = _create_remote(repo_path, remote, url)
        if return_code != 0:
            sys.exit(1)
        _checkout_ref(repo_path, ref, remote, depth, fetch=fetch)
        branch = truncate_ref(ref)
        if git_existing_remote_branch(repo_path, branch, remote):
            if _is_tracking_branch(repo_path, branch):
                _pull_remote_branch(repo_path, remote, branch)
            else:
                _set_tracking_branch_same_commit(repo_path, branch, remote, depth)
    elif ref_type(ref) is 'tag' or ref_type(ref) is 'sha':
        return_code = _create_remote(repo_path, remote, url)
        if return_code != 0:
            sys.exit(1)
        _checkout_ref(repo_path, ref, remote, depth)
    else:
        cprint('Unknown ref ' + ref, 'red')
        sys.exit(1)
    if recursive:
        git_submodule_update_recursive(repo_path, depth)

def git_herd_branch(repo_path, url, remote, branch, default_ref, depth=0, recursive=False):
    """Herd branch"""
    if not git_existing_repository(repo_path):
        _create_repo_herd_branch(repo_path, url, remote, branch,
                                 default_ref, depth=depth, recursive=recursive)
        return
    return_code = git_fetch(repo_path, remote, depth=depth, ref=branch)
    if return_code != 0:
        git_herd(repo_path, url, remote, default_ref, depth=depth, recursive=recursive)
        return
    if git_existing_local_branch(repo_path, branch):
        _checkout_ref(repo_path, 'refs/heads/' + branch, remote, depth)
        if git_existing_remote_branch(repo_path, branch, remote):
            if _is_tracking_branch(repo_path, branch):
                _pull_remote_branch(repo_path, remote, branch)
            else:
                _set_tracking_branch_same_commit(repo_path, branch, remote, depth)
    elif git_existing_remote_branch(repo_path, branch, remote):
        git_herd(repo_path, url, remote, 'refs/heads/' + branch, depth=depth,
                 recursive=recursive, fetch=False)
    else:
        git_herd(repo_path, url, remote, default_ref, depth=depth, recursive=recursive)
    if recursive:
        git_submodule_update_recursive(repo_path, depth)

def git_herd_branch_upstream(repo_path, url, remote, branch, default_ref, depth=0):
    """Herd branch for fork's upstream repo"""
    return_code = _create_remote(repo_path, remote, url)
    if return_code != 0:
        sys.exit(1)
    return_code = git_fetch(repo_path, remote, depth=depth, ref=branch)
    if depth != 0 and return_code != 0:
        git_fetch(repo_path, remote, depth=depth, ref=default_ref)

def git_herd_upstream(repo_path, url, remote, ref, depth=0):
    """Herd branch for fork's upstream repo"""
    return_code = _create_remote(repo_path, remote, url)
    if return_code != 0:
        sys.exit(1)
    git_fetch(repo_path, remote, depth=depth, ref=ref)

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

def git_is_rebase_in_progress(repo_path):
    """Detect whether rebase is in progress"""
    rebase_apply = os.path.join(repo_path, '.git', 'rebase-apply')
    rebase_merge = os.path.join(repo_path, '.git', 'rebase-merge')
    is_rebase_apply = os.path.isdir(rebase_apply)
    is_rebase_merge = os.path.isdir(rebase_merge)
    return is_rebase_apply or is_rebase_merge

def git_is_valid_repo(repo_path):
    """Validate repo"""
    if git_is_dirty(repo_path):
        return False
    elif git_is_rebase_in_progress(repo_path):
        return False
    elif git_untracked_files(repo_path):
        return False
    else:
        return True

def git_is_valid_submodule(repo_path):
    """Validate repo"""
    if git_is_dirty(repo_path):
        return False
    # elif git_untracked_files(repo_path):
    #     return False
    else:
        return True

def git_new_commits(repo_path, upstream=False):
    """Returns the number of new commits"""
    repo = _repo(repo_path)
    try:
        local_branch = repo.active_branch
    except:
        return 0
    else:
        if local_branch is None:
            return 0
        tracking_branch = local_branch.tracking_branch()
        if tracking_branch is None:
            return 0
        try:
            commits = local_branch.commit.hexsha + '...' + tracking_branch.commit.hexsha
            rev_list_count = repo.git.rev_list('--count', '--left-right', commits)
            if upstream:
                count = str(rev_list_count).split()[1]
            else:
                count = str(rev_list_count).split()[0]
            return count
        except:
            return 0

def git_print_branches(repo_path, local=False, remote=False):
    """Print branches"""
    if local and remote:
        command = ['git', 'branch', '-a']
    elif local:
        command = ['git', 'branch']
    elif remote:
        command = ['git', 'branch', '-r']
    return_code = execute_command(command, repo_path)
    if return_code != 0:
        cprint(' - Failed to print branches', 'red')
        print_command_failed_error(command)
        sys.exit(return_code)

def git_prune_local(repo_path, branch, default_ref, force):
    """Prune branch in repository"""
    repo = _repo(repo_path)
    branch_output = format_ref_string(branch)
    if branch not in repo.heads:
        print(' - Local branch ' + branch_output + " doesn't exist")
        return
    prune_branch = repo.heads[branch]
    if repo.head.ref == prune_branch:
        ref_output = format_ref_string(truncate_ref(default_ref))
        try:
            print(' - Checkout ref ' + ref_output)
            repo.git.checkout(truncate_ref(default_ref))
        except Exception as err:
            message = colored(' - Failed to checkout ref', 'red')
            print(message + ref_output)
            print_error(err)
            sys.exit(1)
    try:
        print(' - Delete local branch ' + branch_output)
        repo.delete_head(branch, force=force)
        return
    except Exception as err:
        message = colored(' - Failed to delete local branch ', 'red')
        print(message + branch_output)
        print_error(err)
        sys.exit(1)

def git_prune_remote(repo_path, branch, remote):
    """Prune remote branch in repository"""
    repo = _repo(repo_path)
    origin = _remote(repo_path, remote)
    if origin is None:
        sys.exit(1)
    branch_output = format_ref_string(branch)
    if branch not in origin.refs:
        print(' - Remote branch ' + branch_output + " doesn't exist")
        return
    try:
        print(' - Delete remote branch ' + branch_output)
        repo.git.push(remote, '--delete', branch)
    except Exception as err:
        message = colored(' - Failed to delete remote branch ', 'red')
        print(message + branch_output)
        print_error(err)
        sys.exit(1)

def git_pull(repo_path):
    """Pull from remote branch"""
    repo = _repo(repo_path)
    if repo.head.is_detached:
        print(' - HEAD is detached')
        return
    try:
        print(' - Pull latest changes')
        print(repo.git.pull())
    except Exception as err:
        cprint(' - Failed to pull latest changes', 'red')
        print_error(err)
        sys.exit(1)

def git_push(repo_path):
    """Push to remote branch"""
    repo = _repo(repo_path)
    if repo.head.is_detached:
        print(' - HEAD is detached')
        return
    try:
        print(' - Push local changes')
        print(repo.git.push())
    except Exception as err:
        cprint(' - Failed to push local changes', 'red')
        print_error(err)
        sys.exit(1)

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
    if branch not in repo.heads:
        return_code = git_fetch(repo_path, remote, depth=depth, ref=branch)
        if return_code != 0:
            sys.exit(return_code)
        return_code = _create_branch_local(repo_path, branch)
        if return_code != 0:
            sys.exit(return_code)
        return_code = _checkout_branch_local(repo_path, branch)
        if return_code != 0:
            sys.exit(return_code)
        if tracking:
            _create_branch_remote_tracking(repo_path, branch, remote, depth)
        return
    branch_output = format_ref_string(branch)
    print(' - ' + branch_output + ' already exists')
    correct_branch = _is_branch_checked_out(repo_path, branch)
    if correct_branch:
        print(' - On correct branch')
    else:
        return_code = _checkout_branch_local(repo_path, branch)
        if return_code != 0:
            sys.exit(return_code)
    if tracking:
        _create_branch_remote_tracking(repo_path, branch, remote, depth)

def git_start_offline(repo_path, branch):
    """Start new branch in repository when offline"""
    repo = _repo(repo_path)
    correct_branch = False
    branch_output = format_ref_string(branch)
    if branch not in repo.heads:
        return_code = _create_branch_local(repo_path, branch)
        if return_code != 0:
            sys.exit(return_code)
        return_code = _checkout_branch_local(repo_path, branch)
        if return_code != 0:
            sys.exit(return_code)
        return
    print(' - ' + branch_output + ' already exists')
    correct_branch = _is_branch_checked_out(repo, branch)
    if correct_branch:
        print(' - On correct branch')
        return
    return_code = _checkout_branch_local(repo_path, branch)
    if return_code != 0:
        sys.exit(return_code)

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

def git_submodules_clean(repo_path):
    """Clean all submodules"""
    repo = _repo(repo_path)
    try:
        repo.git.submodule('foreach', '--recursive', 'git', 'clean', '-ffdx')
    except Exception as err:
        cprint(' - Failed to clean submodules', 'red')
        print_error(err)
        sys.exit(1)

def git_submodules_reset(repo_path):
    """Reset all submodules"""
    repo = _repo(repo_path)
    try:
        repo.git.submodule('foreach', '--recursive', 'git', 'reset', '--hard')
    except Exception as err:
        cprint(' - Failed to reset submodules', 'red')
        print_error(err)
        sys.exit(1)

def git_submodules_update(repo_path):
    """Update all submodules"""
    repo = _repo(repo_path)
    try:
        repo.git.submodule('update', '--checkout', '--recursive', '--force')
    except Exception as err:
        cprint(' - Failed to update submodules', 'red')
        print_error(err)
        sys.exit(1)

def git_submodule_update_recursive(repo_path, depth):
    """Update submodules recursively and initialize if not present"""
    print(' - Update submodules recursively and initialize if not present')
    if depth == 0:
        command = ['git', 'submodule', 'update', '--init', '--recursive']
    else:
        command = ['git', 'submodule', 'update', '--init', '--recursive', '--depth', depth]
    return_code = execute_command(command, repo_path)
    if return_code != 0:
        cprint(' - Failed to update submodules', 'red')
        print_command_failed_error(command)
        sys.exit(return_code)

def git_sync(repo_path, upstream_remote, fork_remote, ref, recursive):
    """Sync fork with upstream remote"""
    print(' - Sync fork with upstream remote')
    if ref_type(ref) is not 'branch':
        cprint(' - Can only sync branches', 'red')
        sys.exit(1)
    fork_remote_output = format_remote_string(fork_remote)
    branch_output = format_ref_string(truncate_ref(ref))
    _pull_remote_branch(repo_path, upstream_remote, truncate_ref(ref))
    print(' - Push to ' + fork_remote_output + ' ' + branch_output)
    command = ['git', 'push', fork_remote, truncate_ref(ref)]
    return_code = execute_command(command, repo_path)
    if return_code != 0:
        message = colored(' - Failed to push to ', 'red')
        print(message + fork_remote_output + ' ' + branch_output)
        print_command_failed_error(command)
        sys.exit(return_code)
    if recursive:
        git_submodule_update_recursive(repo_path, recursive)

def git_untracked_files(repo_path):
    """Execute command and display continuous output"""
    command = "git ls-files -o -d --exclude-standard | sed q | wc -l| tr -d '[:space:]'"
    try:
        output = subprocess.check_output(command,
                                         shell=True,
                                         cwd=repo_path)
        return output.decode('utf-8') is '1'
    except Exception as err:
        cprint(' - Failed to check untracked files', 'red')
        print_error(err)
        sys.exit(1)

def git_validate_repo(repo_path):
    """Validate repo state"""
    if not git_existing_repository(repo_path):
        return True
    if not git_is_valid_repo(repo_path):
        return False
    repo = _repo(repo_path)
    for submodule in repo.submodules:
        if not git_is_valid_submodule(submodule.path):
            return False
    return True

def _checkout_branch_local(repo_path, branch):
    """Checkout local branch"""
    repo = _repo(repo_path)
    branch_output = format_ref_string(branch)
    try:
        print(' - Checkout branch ' + branch_output)
        default_branch = repo.heads[branch]
        default_branch.checkout()
        return 0
    except Exception as err:
        message = colored(' - Failed to checkout branch ', 'red')
        print(message + branch_output)
        print_error(err)
        return 1

def _checkout_new_repo_branch(repo_path, branch, remote, depth):
    """Checkout remote branch or fail and delete repo if it doesn't exist"""
    branch_output = format_ref_string(branch)
    origin = _remote(repo_path, remote)
    if origin is None:
        remove_directory_exit(repo_path)
    return_code = git_fetch(repo_path, remote, depth=depth, ref=branch)
    if return_code != 0:
        remove_directory_exit(repo_path)
    if not git_existing_remote_branch(repo_path, branch, remote):
        message = colored(' - No existing remote branch ', 'red')
        print(message + branch_output)
        remove_directory_exit(repo_path)
    return_code = _create_branch_local_tracking(repo_path, branch, remote,
                                                depth=depth, fetch=False)
    if return_code != 0:
        remove_directory_exit(repo_path)
    else:
        return_code = _set_tracking_branch(repo_path, remote, branch)
        if return_code != 0:
            remove_directory_exit(repo_path)
            return
        return_code = _checkout_branch_local(repo_path, branch)
        if return_code != 0:
            remove_directory_exit(repo_path)

def _checkout_new_repo_commit(repo_path, commit, remote, depth):
    """Checkout commit or fail and delete repo if it doesn't exist"""
    repo = _repo(repo_path)
    commit_output = format_ref_string(commit)
    origin = _remote(repo_path, remote)
    if origin is None:
        remove_directory_exit(repo_path)
    return_code = git_fetch(repo_path, remote, depth=depth, ref=commit)
    if return_code != 0:
        remove_directory_exit(repo_path)
    print(' - Checkout commit ' + commit_output)
    try:
        repo.git.checkout(commit)
    except Exception as err:
        message = colored(' - Failed to checkout commit ', 'red')
        print(message + commit_output)
        print_error(err)
        remove_directory_exit(repo_path)

def _checkout_new_repo_tag(repo_path, tag, remote, depth):
    """Checkout tag or fail and delete repo if it doesn't exist"""
    repo = _repo(repo_path)
    tag_output = format_ref_string(tag)
    origin = _remote(repo_path, remote)
    if origin is None:
        remove_directory_exit(repo_path)
    return_code = git_fetch(repo_path, remote, depth=depth, ref=tag)
    if return_code != 0:
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

def _checkout_ref(repo_path, ref, remote, depth, fetch=True):
    """Checkout branch, tag, or commit from sha"""
    if ref_type(ref) is 'branch':
        branch = truncate_ref(ref)
        if not git_existing_local_branch(repo_path, branch):
            return_code = _create_branch_local_tracking(repo_path, branch, remote,
                                                        depth=depth, fetch=fetch)
            if return_code != 0:
                sys.exit(return_code)
        if _is_branch_checked_out(repo_path, branch):
            branch_output = format_ref_string(branch)
            message_1 = ' - Branch '
            message_2 = ' already checked out'
            print(message_1 + branch_output + message_2)
            return
        _checkout_branch_local(repo_path, branch)
    elif ref_type(ref) is 'tag':
        git_fetch(repo_path, remote, depth=depth, ref=ref)
        _checkout_tag(repo_path, truncate_ref(ref))
    elif ref_type(ref) is 'sha':
        git_fetch(repo_path, remote, depth=depth, ref=ref)
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
    except:
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
            except Exception as err:
                message = colored(' - Failed to checkout tag ', 'red')
                print(message + tag_output)
                print_error(err)
                sys.exit(1)

def _create_branch_local(repo_path, branch):
    """Create local branch"""
    repo = _repo(repo_path)
    branch_output = format_ref_string(branch)
    try:
        print(' - Create branch ' + branch_output)
        repo.create_head(branch)
        return 0
    except Exception as err:
        message = colored(' - Failed to create branch ', 'red')
        print(message + branch_output)
        print_error(err)
        return 1

def _create_branch_local_tracking(repo_path, branch, remote, depth, fetch=True):
    """Create and checkout tracking branch"""
    repo = _repo(repo_path)
    branch_output = format_ref_string(branch)
    origin = _remote(repo_path, remote)
    if origin is None:
        return 1
    if fetch:
        return_code = git_fetch(repo_path, remote, depth=depth, ref=branch)
        if return_code != 0:
            return return_code
    try:
        print(' - Create branch ' + branch_output)
        repo.create_head(branch, origin.refs[branch])
    except Exception as err:
        message = colored(' - Failed to create branch ', 'red')
        print(message + branch_output)
        print_error(err)
        return 1
    else:
        return_code = _set_tracking_branch(repo_path, remote, branch)
        if return_code != 0:
            return return_code
        return _checkout_branch_local(repo_path, branch)

def _create_branch_remote_tracking(repo_path, branch, remote, depth):
    """Create remote tracking branch"""
    repo = _repo(repo_path)
    branch_output = format_ref_string(branch)
    origin = _remote(repo_path, remote)
    if origin is None:
        sys.exit(1)
    return_code = git_fetch(repo_path, remote, depth=depth, ref=branch)
    if return_code != 0:
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
        return_code = _set_tracking_branch(repo_path, remote, branch)
        if return_code != 0:
            sys.exit(return_code)

def _create_remote(repo_path, remote, url):
    """Create new remote"""
    repo = _repo(repo_path)
    remote_names = [r.name for r in repo.remotes]
    if remote in remote_names:
        return 0
    remote_output = format_remote_string(remote)
    try:
        print(" - Create remote " + remote_output)
        repo.create_remote(remote, url)
        return 0
    except Exception as err:
        message = colored(" - Failed to create remote ", 'red')
        print(message + remote_output)
        print_error(err)
        return 1

def _create_repo_herd_branch(repo_path, url, remote, branch, default_ref,
                                depth=0, recursive=False):
    """Clone git repo from url at path for herd branch"""
    if git_existing_repository(repo_path):
        return
    if not os.path.isdir(repo_path):
        os.makedirs(repo_path)
    repo_path_output = format_path(repo_path)
    try:
        print(' - Clone repo at ' + repo_path_output)
        Repo.init(repo_path)
    except Exception as err:
        cprint(' - Failed to initialize repository', 'red')
        print_error(err)
        remove_directory_exit(repo_path)
    else:
        repo = _repo(repo_path)
        remote_names = [r.name for r in repo.remotes]
        if remote in remote_names:
            _checkout_ref(repo_path, 'refs/heads/' + branch, remote, depth)
            return
        return_code = _create_remote(repo_path, remote, url)
        if return_code != 0:
            remove_directory_exit(repo_path)
        branch_output = format_ref_string(branch)
        origin = _remote(repo_path, remote)
        if origin is None:
            remove_directory_exit(repo_path)
        return_code = git_fetch(repo_path, remote, depth=depth, ref=branch)
        if return_code != 0:
            remove_directory_exit(repo_path)
        if not git_existing_remote_branch(repo_path, branch, remote):
            print(' - No existing remote branch ' + branch_output)
            _checkout_new_repo_branch(repo_path, truncate_ref(default_ref), remote, depth)
            return
        return_code = _create_branch_local_tracking(repo_path, branch, remote,
                                                    depth=depth, fetch=False)
        if return_code != 0:
            remove_directory_exit(repo_path)
        else:
            return_code = _set_tracking_branch(repo_path, remote, branch)
            if return_code != 0:
                remove_directory_exit(repo_path)
                return
            return_code = _checkout_branch_local(repo_path, branch)
            if return_code != 0:
                remove_directory_exit(repo_path)
        if recursive:
            git_submodule_update_recursive(repo_path, depth)

def _is_branch_checked_out(repo_path, branch):
    """Check if branch is checked out"""
    repo = _repo(repo_path)
    try:
        default_branch = repo.heads[branch]
        not_detached = not repo.head.is_detached
        same_branch = repo.head.ref == default_branch
    except:
        return False
    else:
        return not_detached and same_branch

def _is_tracking_branch(repo_path, branch):
    """Check if branch is a tracking branch"""
    repo = _repo(repo_path)
    branch_output = format_ref_string(branch)
    try:
        local_branch = repo.heads[branch]
    except Exception as err:
        message = colored(' - No existing branch ', 'red')
        print(message + branch_output)
        print_error(err)
        sys.exit(1)
    else:
        tracking_branch = local_branch.tracking_branch()
        return True if tracking_branch else False

def _pull_remote_branch(repo_path, remote, branch):
    """Pull from remote branch"""
    repo = _repo(repo_path)
    if repo.head.is_detached:
        print(' - HEAD is detached')
        return
    branch_output = format_ref_string(branch)
    remote_output = format_remote_string(remote)
    print(' - Pull from ' + remote_output + ' ' + branch_output)
    command = ['git', 'pull', remote, branch]
    return_code = execute_command(command, repo_path)
    if return_code != 0:
        message = colored(' - Failed to pull from ', 'red')
        print(message + remote_output + ' ' + branch_output)
        print_command_failed_error(command)
        sys.exit(return_code)

def _remote(repo_path, remote):
    """Get remote"""
    repo = _repo(repo_path)
    remote_output = format_remote_string(remote)
    try:
        return repo.remotes[remote]
    except Exception as err:
        message = colored(' - No existing remote ', 'red')
        print(message + remote_output)
        print_error(err)
        return None

def _rename_remote(repo_path, remote_from, remote_to):
    """Rename remote"""
    repo = _repo(repo_path)
    remote_output_from = format_remote_string(remote_from)
    remote_output_to = format_remote_string(remote_to)
    print(' - Rename remote ' + remote_output_from + ' to ' + remote_output_to)
    try:
        repo.git.remote('rename', remote_from, remote_to)
    except Exception as err:
        cprint(' - Failed to rename remote', 'red')
        print_error(err)
        sys.exit(1)

def _repo(repo_path):
    """Create Repo instance for path"""
    try:
        repo = Repo(repo_path)
        return repo
    except Exception as err:
        repo_path_output = format_path(repo_path)
        message = colored("Failed to create Repo instance for ", 'red')
        print(message + repo_path_output)
        print_error(err)
        sys.exit(1)

def _set_tracking_branch(repo_path, remote, branch):
    """Set tracking branch"""
    repo = _repo(repo_path)
    branch_output = format_ref_string(branch)
    remote_output = format_remote_string(remote)
    origin = _remote(repo_path, remote)
    try:
        local_branch = repo.heads[branch]
        remote_branch = origin.refs[branch]
        print(' - Set tracking branch ' + branch_output +
              ' -> ' + remote_output + ' ' + branch_output)
        local_branch.set_tracking_branch(remote_branch)
        return 0
    except Exception as err:
        message = colored(' - Failed to set tracking branch ', 'red')
        print(message + branch_output)
        print_error(err)
        return 1

def _set_tracking_branch_same_commit(repo_path, branch, remote, depth):
    """Set tracking relationship between local and remote branch if on same commit"""
    repo = _repo(repo_path)
    branch_output = format_ref_string(branch)
    origin = _remote(repo_path, remote)
    if origin is None:
        sys.exit(1)
    return_code = git_fetch(repo_path, remote, depth=depth, ref=branch)
    if return_code != 0:
        sys.exit(return_code)
    if not git_existing_local_branch(repo_path, branch):
        message_1 = colored(' - No local branch ', 'red')
        print(message_1 + branch_output + '\n')
        sys.exit(1)
    if not git_existing_remote_branch(repo_path, branch, remote):
        message_1 = colored(' - No remote branch ', 'red')
        print(message_1 + branch_output + '\n')
        sys.exit(1)
    local_branch = repo.heads[branch]
    remote_branch = origin.refs[branch]
    if local_branch.commit != remote_branch.commit:
        message_1 = colored(' - Existing remote branch ', 'red')
        message_2 = colored(' on different commit', 'red')
        print(message_1 + branch_output + message_2 + '\n')
        sys.exit(1)
    return_code = _set_tracking_branch(repo_path, remote, branch)
    if return_code != 0:
        sys.exit(return_code)
