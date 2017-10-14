"""Git utilities"""

from __future__ import print_function
import os
import subprocess
import sys
from git import Repo, GitError
from termcolor import colored, cprint
from clowder.utility.clowder_utilities import (
    execute_command,
    existing_git_repository,
    is_offline,
    ref_type,
    remove_directory_exit,
    truncate_ref
)
from clowder.utility.print_utilities import (
    format_path,
    format_ref_string,
    format_remote_string,
    print_command_failed_error,
    print_error,
    print_remote_already_exists_error
)


class Git(object):
    """Class encapsulating git utilities"""

    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.repo = self._repo() if existing_git_repository(repo_path) else None

    def checkout(self, truncated_ref):
        """Checkout git ref"""
        ref_output = format_ref_string(truncated_ref)
        try:
            print(' - Check out ' + ref_output)
            print(self.repo.git.checkout(truncated_ref))
        except GitError as err:
            message = colored(' - Failed to checkout ref ', 'red')
            print(message + ref_output)
            print_error(err)
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def clean(self, args=''):
        """Discard changes for repo"""
        print(' - Clean project')
        clean_args = '-f' if args == '' else '-f' + args
        self._clean(args=clean_args)
        print(' - Reset project')
        self._reset_head()
        if self._is_rebase_in_progress():
            print(' - Abort rebase in progress')
            self._abort_rebase()

    def create_clowder_repo(self, url, remote, branch, depth=0):
        """Clone clowder git repo from url at path"""
        if existing_git_repository(self.repo_path):
            return
        self._init_repo()
        return_code = self._create_remote(remote, url)
        if return_code != 0:
            remove_directory_exit(self.repo_path)
        self._checkout_new_repo_branch(branch, remote, depth)

    def configure_remotes(self, upstream_remote_name, upstream_remote_url,
                          fork_remote_name, fork_remote_url):
        """Configure remotes names for fork and upstream"""
        if not existing_git_repository(self.repo_path):
            return
        try:
            remotes = self.repo.remotes
        except GitError:
            return
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)
        for remote in remotes:
            if upstream_remote_url == self.repo.git.remote('get-url', remote.name):
                if remote.name != upstream_remote_name:
                    self._rename_remote(remote.name, upstream_remote_name)
                    continue
            if fork_remote_url == self.repo.git.remote('get-url', remote.name):
                if remote.name != fork_remote_name:
                    self._rename_remote(remote.name, fork_remote_name)
        remote_names = [r.name for r in self.repo.remotes]
        if upstream_remote_name in remote_names:
            if upstream_remote_url != self.repo.git.remote('get-url', upstream_remote_name):
                actual_url = self.repo.git.remote('get-url', upstream_remote_name)
                print_remote_already_exists_error(upstream_remote_name,
                                                  upstream_remote_url, actual_url)
                sys.exit(1)
        if fork_remote_name in remote_names:
            if fork_remote_url != self.repo.git.remote('get-url', fork_remote_name):
                actual_url = self.repo.git.remote('get-url', fork_remote_name)
                print_remote_already_exists_error(fork_remote_name,
                                                  fork_remote_url, actual_url)
                sys.exit(1)

    def current_branch(self):
        """Return currently checked out branch of project"""
        return self.repo.head.ref.name

    def existing_remote_branch(self, branch, remote):
        """Check if remote branch exists"""
        try:
            origin = self.repo.remotes[remote]
            return branch in origin.refs
        except (GitError, IndexError):
            return False
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def existing_local_branch(self, branch):
        """Check if local branch exists"""
        return branch in self.repo.heads

    def fetch(self, remote, ref=None, depth=0, remove_dir=False):
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
        return_code = execute_command(command, self.repo_path)
        if return_code != 0:
            print(error)
            if remove_dir:
                remove_directory_exit(self.repo_path)
        return return_code

    def herd(self, url, remote, ref, depth=0, fetch=True, rebase=False):
        """Herd ref"""
        if not existing_git_repository(self.repo_path):
            self._herd_initial(url, remote, ref, depth=depth)
            return
        return_code = self._create_remote(remote, url)
        if return_code != 0:
            sys.exit(1)
        if ref_type(ref) == 'branch':
            branch = truncate_ref(ref)
            if not self.existing_local_branch(branch):
                return_code = self._create_branch_local_tracking(branch, remote, depth=depth, fetch=fetch)
                if return_code != 0:
                    sys.exit(return_code)
            if self._is_branch_checked_out(branch):
                branch_output = format_ref_string(branch)
                print(' - Branch ' + branch_output + ' already checked out')
            else:
                self._checkout_branch_local(branch)
            if not self.existing_remote_branch(branch, remote):
                return
            if not self._is_tracking_branch(branch):
                self._set_tracking_branch_commit(branch, remote, depth)
                return
            if rebase:
                self._rebase_remote_branch(remote, branch)
                return
            self._pull_remote_branch(remote, branch)
        elif ref_type(ref) == 'tag':
            self.fetch(remote, depth=depth, ref=ref)
            self._checkout_tag(truncate_ref(ref))
        elif ref_type(ref) == 'sha':
            self.fetch(remote, depth=depth, ref=ref)
            self._checkout_sha(ref)

    def herd_branch(self, url, remote, branch, default_ref, depth=0, rebase=False):
        """Herd branch"""
        if not existing_git_repository(self.repo_path):
            self._herd_branch_initial(url, remote, branch, default_ref, depth=depth)
            return
        if self.existing_local_branch(branch):
            if self._is_branch_checked_out(branch):
                branch_output = format_ref_string(branch)
                print(' - Branch ' + branch_output + ' already checked out')
            else:
                self._checkout_branch_local(branch)
            if not self.existing_remote_branch(branch, remote):
                return
            if not self._is_tracking_branch(branch):
                self._set_tracking_branch_commit(branch, remote, depth)
                return
        if self.existing_remote_branch(branch, remote):
            self.herd(url, remote, 'refs/heads/' + branch, depth=depth, rebase=rebase)
            return
        self.herd(url, remote, default_ref, depth=depth, rebase=rebase)

    def herd_tag(self, url, remote, tag, default_ref, depth=0, rebase=False):
        """Herd tag"""
        if not existing_git_repository(self.repo_path):
            self._init_repo()
            return_code = self._create_remote(remote, url)
            if return_code != 0:
                remove_directory_exit(self.repo_path)
            self.fetch(remote, depth=depth, remove_dir=True)
            if self._checkout_tag(tag):
                return
            self.herd(url, remote, default_ref, depth=depth, rebase=rebase)
            return
        return_code = self.fetch(remote, ref="refs/tags/" + tag, depth=depth)
        if return_code == 0:
            return_code = self._checkout_tag(tag)
            if return_code == 0:
                return
        self.herd(url, remote, default_ref, depth=depth, rebase=rebase)

    def herd_upstream(self, url, remote, default_ref, branch=None):
        """Herd fork's upstream repo"""
        return_code = self._create_remote(remote, url)
        if return_code != 0:
            sys.exit(1)
        if branch is not None:
            return_code = self.fetch(remote, ref=branch)
            if return_code == 0:
                return
        return_code = self.fetch(remote, ref=default_ref)
        if return_code != 0:
            sys.exit(1)

    def is_detached(self):
        """Check if HEAD is detached"""
        if not os.path.isdir(self.repo_path):
            return False
        return self.repo.head.is_detached

    def is_dirty(self):
        """Check whether repo is dirty"""
        if not os.path.isdir(self.repo_path):
            return False
        return (self._is_dirty() or
                self._is_rebase_in_progress() or
                self._untracked_files())

    def new_commits(self, upstream=False):
        """Returns the number of new commits"""
        try:
            local_branch = self.repo.active_branch
        except (GitError, TypeError):
            return 0
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)
        if local_branch is None:
            return 0
        tracking_branch = local_branch.tracking_branch()
        if tracking_branch is None:
            return 0
        try:
            commits = local_branch.commit.hexsha + '...' + tracking_branch.commit.hexsha
            rev_list_count = self.repo.git.rev_list('--count', '--left-right', commits)
            if upstream:
                count = str(rev_list_count).split()[1]
            else:
                count = str(rev_list_count).split()[0]
            return count
        except (GitError, ValueError):
            return 0
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def print_branches(self, local=False, remote=False):
        """Print branches"""
        if local and remote:
            command = ['git', 'branch', '-a']
        elif local:
            command = ['git', 'branch']
        elif remote:
            command = ['git', 'branch', '-r']
        else:
            return
        return_code = execute_command(command, self.repo_path)
        if return_code != 0:
            cprint(' - Failed to print branches', 'red')
            print_command_failed_error(command)
            sys.exit(return_code)

    def prune_branch_local(self, branch, default_ref, force):
        """Prune branch in repository"""
        branch_output = format_ref_string(branch)
        if branch not in self.repo.heads:
            print(' - Local branch ' + branch_output + " doesn't exist")
            return
        prune_branch = self.repo.heads[branch]
        if self.repo.head.ref == prune_branch:
            ref_output = format_ref_string(truncate_ref(default_ref))
            try:
                print(' - Checkout ref ' + ref_output)
                self.repo.git.checkout(truncate_ref(default_ref))
            except GitError as err:
                message = colored(' - Failed to checkout ref', 'red')
                print(message + ref_output)
                print_error(err)
                sys.exit(1)
            except (KeyboardInterrupt, SystemExit):
                sys.exit(1)
        try:
            print(' - Delete local branch ' + branch_output)
            self.repo.delete_head(branch, force=force)
            return
        except GitError as err:
            message = colored(' - Failed to delete local branch ', 'red')
            print(message + branch_output)
            print_error(err)
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def prune_branch_remote(self, branch, remote):
        """Prune remote branch in repository"""
        origin = self._remote(remote)
        if origin is None:
            sys.exit(1)
        branch_output = format_ref_string(branch)
        if branch not in origin.refs:
            print(' - Remote branch ' + branch_output + " doesn't exist")
            return
        try:
            print(' - Delete remote branch ' + branch_output)
            self.repo.git.push(remote, '--delete', branch)
        except GitError as err:
            message = colored(' - Failed to delete remote branch ', 'red')
            print(message + branch_output)
            print_error(err)
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def sha(self, short=False):
        """Return sha for currently checked out commit"""
        if short:
            return self.repo.git.rev_parse(self.repo.head.commit.hexsha, short=True)
        return self.repo.head.commit.hexsha

    def start(self, remote, branch, depth, tracking):
        """Start new branch in repository"""
        if branch not in self.repo.heads:
            if not is_offline():
                return_code = self.fetch(remote, depth=depth, ref=branch)
                if return_code != 0:
                    sys.exit(return_code)
            return_code = self._create_branch_local(branch)
            if return_code != 0:
                sys.exit(return_code)
            return_code = self._checkout_branch_local(branch)
            if return_code != 0:
                sys.exit(return_code)
        else:
            branch_output = format_ref_string(branch)
            print(' - ' + branch_output + ' already exists')
            correct_branch = self._is_branch_checked_out(branch)
            if correct_branch:
                print(' - On correct branch')
            else:
                return_code = self._checkout_branch_local(branch)
                if return_code != 0:
                    sys.exit(return_code)
        if tracking and not is_offline():
            self._create_branch_remote_tracking(branch, remote, depth)

    def stash(self):
        """Stash current changes in repository"""
        if not self.repo.is_dirty():
            print(' - No changes to stash')
            return
        print(' - Stash current changes')
        self.repo.git.stash()

    def sync(self, upstream_remote, fork_remote, ref, rebase=False):
        """Sync fork with upstream remote"""
        print(' - Sync fork with upstream remote')
        if ref_type(ref) != 'branch':
            cprint(' - Can only sync branches', 'red')
            sys.exit(1)
        fork_remote_output = format_remote_string(fork_remote)
        branch_output = format_ref_string(truncate_ref(ref))
        if rebase:
            self._rebase_remote_branch(upstream_remote, truncate_ref(ref))
        else:
            self._pull_remote_branch(upstream_remote, truncate_ref(ref))
        print(' - Push to ' + fork_remote_output + ' ' + branch_output)
        command = ['git', 'push', fork_remote, truncate_ref(ref)]
        return_code = execute_command(command, self.repo_path)
        if return_code != 0:
            message = colored(' - Failed to push to ', 'red')
            print(message + fork_remote_output + ' ' + branch_output)
            print_command_failed_error(command)
            sys.exit(return_code)

    def validate_repo(self):
        """Validate repo state"""
        if not existing_git_repository(self.repo_path):
            return True
        return not self.is_dirty()

    def _abort_rebase(self):
        """Abort rebase"""
        if not self._is_rebase_in_progress():
            return
        try:
            self.repo.git.rebase('--abort')
        except GitError as err:
            cprint(' - Failed to abort rebase', 'red')
            print_error(err)
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _checkout_branch_local(self, branch, remove_dir=False):
        """Checkout local branch"""
        branch_output = format_ref_string(branch)
        try:
            print(' - Checkout branch ' + branch_output)
            default_branch = self.repo.heads[branch]
            default_branch.checkout()
            return 0
        except GitError as err:
            message = colored(' - Failed to checkout branch ', 'red')
            print(message + branch_output)
            print_error(err)
            if remove_dir:
                remove_directory_exit(self.repo_path)
            return 1
        except (KeyboardInterrupt, SystemExit):
            if remove_dir:
                remove_directory_exit(self.repo_path)
            sys.exit(1)

    def _checkout_new_repo_branch(self, branch, remote, depth):
        """Checkout remote branch or fail and delete repo if it doesn't exist"""
        branch_output = format_ref_string(branch)
        origin = self._remote(remote)
        if origin is None:
            remove_directory_exit(self.repo_path)
        self.fetch(remote, depth=depth, ref=branch, remove_dir=True)
        if not self.existing_remote_branch(branch, remote):
            message = colored(' - No existing remote branch ', 'red')
            print(message + branch_output)
            remove_directory_exit(self.repo_path)
        self._create_branch_local_tracking(branch, remote, depth=depth, fetch=False, remove_dir=True)
        self._set_tracking_branch(remote, branch, remove_dir=True)
        self._checkout_branch_local(branch, remove_dir=True)

    def _checkout_new_repo_commit(self, commit, remote, depth):
        """Checkout commit or fail and delete repo if it doesn't exist"""
        commit_output = format_ref_string(commit)
        origin = self._remote(remote)
        if origin is None:
            remove_directory_exit(self.repo_path)
        self.fetch(remote, depth=depth, ref=commit, remove_dir=True)
        print(' - Checkout commit ' + commit_output)
        try:
            self.repo.git.checkout(commit)
        except GitError as err:
            message = colored(' - Failed to checkout commit ', 'red')
            print(message + commit_output)
            print_error(err)
            remove_directory_exit(self.repo_path)
        except (KeyboardInterrupt, SystemExit):
            remove_directory_exit(self.repo_path)

    def _checkout_new_repo_tag(self, tag, remote, depth):
        """Checkout tag or fail and delete repo if it doesn't exist"""
        tag_output = format_ref_string(tag)
        origin = self._remote(remote)
        if origin is None:
            remove_directory_exit(self.repo_path)
        self.fetch(remote, depth=depth, ref=tag, remove_dir=True)
        try:
            remote_tag = origin.tags[tag]
        except GitError:
            message = colored(' - No existing remote tag ', 'red')
            print(message + tag_output)
            remove_directory_exit(self.repo_path)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)
        else:
            try:
                print(' - Checkout tag ' + tag_output)
                self.repo.git.checkout(remote_tag)
            except GitError as err:
                message = colored(' - Failed to checkout tag ', 'red')
                print(message + tag_output)
                print_error(err)
                remove_directory_exit(self.repo_path)
            except (KeyboardInterrupt, SystemExit):
                remove_directory_exit(self.repo_path)

    def _checkout_sha(self, sha):
        """Checkout commit by sha"""
        commit_output = format_ref_string(sha)
        try:
            same_sha = self.repo.head.commit.hexsha == sha
            is_detached = self.repo.head.is_detached
            if same_sha and is_detached:
                print(' - On correct commit')
                return 0
            print(' - Checkout commit ' + commit_output)
            self.repo.git.checkout(sha)
        except GitError as err:
            message = colored(' - Failed to checkout commit ', 'red')
            print(message + commit_output)
            print_error(err)
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _checkout_tag(self, tag):
        """Checkout commit tag is pointing to"""
        tag_output = format_ref_string(tag)
        if tag not in self.repo.tags:
            print(' - No existing tag ' + tag_output)
            return 1
        try:
            same_commit = self.repo.head.commit == self.repo.tags[tag].commit
            is_detached = self.repo.head.is_detached
            if same_commit and is_detached:
                print(' - On correct commit for tag')
                return 0
            print(' - Checkout tag ' + tag_output)
            self.repo.git.checkout('refs/tags/' + tag)
            return 0
        except GitError as err:
            message = colored(' - Failed to checkout tag ', 'red')
            print(message + tag_output)
            print_error(err)
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _clean(self, args):
        """Clean git directory"""
        try:
            self.repo.git.clean(args)
        except GitError as err:
            cprint(' - Failed to clean git repo', 'red')
            print_error(err)
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _create_branch_local(self, branch):
        """Create local branch"""
        branch_output = format_ref_string(branch)
        try:
            print(' - Create branch ' + branch_output)
            self.repo.create_head(branch)
            return 0
        except GitError as err:
            message = colored(' - Failed to create branch ', 'red')
            print(message + branch_output)
            print_error(err)
            return 1
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _create_branch_local_tracking(self, branch, remote, depth, fetch=True, remove_dir=False):
        """Create and checkout tracking branch"""
        branch_output = format_ref_string(branch)
        origin = self._remote(remote)
        if origin is None:
            if remove_dir:
                remove_directory_exit(self.repo_path)
            return 1
        if fetch:
            return_code = self.fetch(remote, depth=depth, ref=branch, remove_dir=remove_dir)
            if return_code != 0:
                return return_code
        try:
            print(' - Create branch ' + branch_output)
            self.repo.create_head(branch, origin.refs[branch])
        except (GitError, IndexError) as err:
            message = colored(' - Failed to create branch ', 'red')
            print(message + branch_output)
            print_error(err)
            if remove_dir:
                remove_directory_exit(self.repo_path)
            return 1
        except (KeyboardInterrupt, SystemExit):
            if remove_dir:
                remove_directory_exit(self.repo_path)
            sys.exit(1)
        else:
            return_code = self._set_tracking_branch(remote, branch, remove_dir=remove_dir)
            if return_code != 0:
                return return_code
            return self._checkout_branch_local(branch, remove_dir=remove_dir)

    def _create_branch_remote_tracking(self, branch, remote, depth):
        """Create remote tracking branch"""
        branch_output = format_ref_string(branch)
        origin = self._remote(remote)
        if origin is None:
            sys.exit(1)
        return_code = self.fetch(remote, depth=depth, ref=branch)
        if return_code != 0:
            sys.exit(return_code)
        if branch in origin.refs:
            try:
                self.repo.git.config('--get', 'branch.' + branch + '.merge')
                print(' - Tracking branch ' + branch_output + ' already exists')
                return
            except GitError:
                message_1 = colored(' - Remote branch ', 'red')
                message_2 = colored(' already exists', 'red')
                print(message_1 + branch_output + message_2 + '\n')
                sys.exit(1)
            except (KeyboardInterrupt, SystemExit):
                sys.exit(1)
        try:
            print(' - Push remote branch ' + branch_output)
            self.repo.git.push(remote, branch)
            return_code = self._set_tracking_branch(remote, branch)
            if return_code != 0:
                sys.exit(return_code)
        except GitError as err:
            message = colored(' - Failed to push remote branch ', 'red')
            print(message + branch_output)
            print_error(err)
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _create_remote(self, remote, url):
        """Create new remote"""
        remote_names = [r.name for r in self.repo.remotes]
        if remote in remote_names:
            return 0
        remote_output = format_remote_string(remote)
        try:
            print(' - Create remote ' + remote_output)
            self.repo.create_remote(remote, url)
            return 0
        except GitError as err:
            message = colored(' - Failed to create remote ', 'red')
            print(message + remote_output)
            print_error(err)
            return 1
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _existing_remote_tag(self, tag, remote, depth=0):
        """Check if remote tag exists"""
        origin = self._remote(remote)
        if origin is None:
            remove_directory_exit(self.repo_path)
        self.fetch(remote, depth=depth, ref=tag, remove_dir=True)
        return tag in origin.tags

    def _herd_initial(self, url, remote, ref, depth=0):
        """Herd ref initial"""
        self._init_repo()
        return_code = self._create_remote(remote, url)
        if return_code != 0:
            remove_directory_exit(self.repo_path)
        if ref_type(ref) == 'branch':
            self._checkout_new_repo_branch(truncate_ref(ref), remote, depth)
        elif ref_type(ref) == 'tag':
            self._checkout_new_repo_tag(truncate_ref(ref), remote, depth)
        elif ref_type(ref) == 'sha':
            self._checkout_new_repo_commit(ref, remote, depth)

    def _herd_branch_initial(self, url, remote, branch, default_ref, depth=0):
        """Herd branch initial"""
        self._init_repo()
        return_code = self._create_remote(remote, url)
        if return_code != 0:
            remove_directory_exit(self.repo_path)
        self.fetch(remote, depth=depth, ref=branch, remove_dir=True)
        if not self.existing_remote_branch(branch, remote):
            print(' - No existing remote branch ' + format_ref_string(branch))
            self._herd_initial(url, remote, default_ref, depth=depth)
            return
        return_code = self._create_branch_local_tracking(branch, remote, depth=depth, fetch=False)
        if return_code != 0:
            remove_directory_exit(self.repo_path)
        if self._set_tracking_branch(remote, branch):
            remove_directory_exit(self.repo_path)
        if self._checkout_branch_local(branch):
            remove_directory_exit(self.repo_path)

    def _init_repo(self):
        """Initialize repository"""
        try:
            print(' - Initialize repo at ' + format_path(self.repo_path))
            if not os.path.isdir(self.repo_path):
                os.makedirs(self.repo_path)
            self.repo = Repo.init(self.repo_path)
        except GitError as err:
            cprint(' - Failed to initialize repository', 'red')
            print_error(err)
            remove_directory_exit(self.repo_path)
        except (KeyboardInterrupt, SystemExit):
            remove_directory_exit(self.repo_path)

    def _is_branch_checked_out(self, branch):
        """Check if branch is checked out"""
        try:
            default_branch = self.repo.heads[branch]
            not_detached = not self.repo.head.is_detached
            same_branch = self.repo.head.ref == default_branch
            return not_detached and same_branch
        except (GitError, TypeError):
            return False
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _is_dirty(self):
        """Check if repo is dirty"""
        return self.repo.is_dirty()

    def _is_rebase_in_progress(self):
        """Detect whether rebase is in progress"""
        rebase_apply = os.path.join(self.repo_path, '.git', 'rebase-apply')
        rebase_merge = os.path.join(self.repo_path, '.git', 'rebase-merge')
        is_rebase_apply = os.path.isdir(rebase_apply)
        is_rebase_merge = os.path.isdir(rebase_merge)
        return is_rebase_apply or is_rebase_merge

    def _is_tracking_branch(self, branch):
        """Check if branch is a tracking branch"""
        branch_output = format_ref_string(branch)
        try:
            local_branch = self.repo.heads[branch]
            tracking_branch = local_branch.tracking_branch()
            return True if tracking_branch else False
        except GitError as err:
            message = colored(' - No existing branch ', 'red')
            print(message + branch_output)
            print_error(err)
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _pull_remote_branch(self, remote, branch):
        """Pull from remote branch"""
        if self.repo.head.is_detached:
            print(' - HEAD is detached')
            return
        branch_output = format_ref_string(branch)
        remote_output = format_remote_string(remote)
        print(' - Pull from ' + remote_output + ' ' + branch_output)
        command = ['git', 'pull', remote, branch]
        return_code = execute_command(command, self.repo_path)
        if return_code != 0:
            message = colored(' - Failed to pull from ', 'red')
            print(message + remote_output + ' ' + branch_output)
            print_command_failed_error(command)
            sys.exit(return_code)

    def _rebase_remote_branch(self, remote, branch):
        """Rebase from remote branch"""
        if self.repo.head.is_detached:
            print(' - HEAD is detached')
            return
        branch_output = format_ref_string(branch)
        remote_output = format_remote_string(remote)
        print(' - Rebase from ' + remote_output + ' ' + branch_output)
        command = ['git', 'rebase', remote + '/' + branch]
        return_code = execute_command(command, self.repo_path)
        if return_code != 0:
            message = colored(' - Failed to rebase from ', 'red')
            print(message + remote_output + ' ' + branch_output)
            print_command_failed_error(command)
            sys.exit(return_code)

    def _remote(self, remote):
        """Get remote"""
        remote_output = format_remote_string(remote)
        try:
            return self.repo.remotes[remote]
        except GitError as err:
            message = colored(' - No existing remote ', 'red')
            print(message + remote_output)
            print_error(err)
            return None
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _rename_remote(self, remote_from, remote_to):
        """Rename remote"""
        remote_output_from = format_remote_string(remote_from)
        remote_output_to = format_remote_string(remote_to)
        print(' - Rename remote ' + remote_output_from + ' to ' + remote_output_to)
        try:
            self.repo.git.remote('rename', remote_from, remote_to)
        except GitError as err:
            cprint(' - Failed to rename remote', 'red')
            print_error(err)
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _repo(self):
        """Create Repo instance for path"""
        try:
            repo = Repo(self.repo_path)
            return repo
        except GitError as err:
            repo_path_output = format_path(self.repo_path)
            message = colored("Failed to create Repo instance for ", 'red')
            print(message + repo_path_output)
            print_error(err)
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _reset_head(self):
        """Reset head of repo, discarding changes"""
        self.repo.head.reset(index=True, working_tree=True)

    def _set_tracking_branch(self, remote, branch, remove_dir=False):
        """Set tracking branch"""
        branch_output = format_ref_string(branch)
        remote_output = format_remote_string(remote)
        origin = self._remote(remote)
        try:
            local_branch = self.repo.heads[branch]
            remote_branch = origin.refs[branch]
            print(' - Set tracking branch ' + branch_output +
                  ' -> ' + remote_output + ' ' + branch_output)
            local_branch.set_tracking_branch(remote_branch)
            return 0
        except GitError as err:
            message = colored(' - Failed to set tracking branch ', 'red')
            print(message + branch_output)
            print_error(err)
            if remove_dir:
                remove_directory_exit(self.repo_path)
            return 1
        except (KeyboardInterrupt, SystemExit):
            if remove_dir:
                remove_directory_exit(self.repo_path)
            sys.exit(1)

    def _set_tracking_branch_commit(self, branch, remote, depth):
        """Set tracking relationship between local and remote branch if on same commit"""
        branch_output = format_ref_string(branch)
        origin = self._remote(remote)
        if origin is None:
            sys.exit(1)
        return_code = self.fetch(remote, depth=depth, ref=branch)
        if return_code != 0:
            sys.exit(return_code)
        if not self.existing_local_branch(branch):
            message_1 = colored(' - No local branch ', 'red')
            print(message_1 + branch_output + '\n')
            sys.exit(1)
        if not self.existing_remote_branch(branch, remote):
            message_1 = colored(' - No remote branch ', 'red')
            print(message_1 + branch_output + '\n')
            sys.exit(1)
        local_branch = self.repo.heads[branch]
        remote_branch = origin.refs[branch]
        if local_branch.commit != remote_branch.commit:
            message_1 = colored(' - Existing remote branch ', 'red')
            message_2 = colored(' on different commit', 'red')
            print(message_1 + branch_output + message_2 + '\n')
            sys.exit(1)
        return_code = self._set_tracking_branch(remote, branch)
        if return_code != 0:
            sys.exit(return_code)

    def _untracked_files(self):
        """Execute command and display continuous output"""
        command = "git ls-files -o -d --exclude-standard | sed q | wc -l| tr -d '[:space:]'"
        try:
            output = subprocess.check_output(command, shell=True, cwd=self.repo_path)
            return output.decode('utf-8') == '1'
        except GitError as err:
            cprint(' - Failed to check untracked files', 'red')
            print_error(err)
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)
