"""Git utilities"""

from __future__ import print_function
import os
import subprocess
import sys
from git import Repo, GitError
from termcolor import colored, cprint
from clowder.exception.clowder_git_exception import ClowderGitException
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
    format_remote_already_exists_error
)


class Git(object):
    """Class encapsulating git utilities"""

    def __init__(self, repo_path, print_output=True):
        self.repo_path = repo_path
        self.print_output = print_output
        self.repo = self._repo() if existing_git_repository(repo_path) else None

    def checkout(self, truncated_ref):
        """Checkout git ref"""
        ref_output = format_ref_string(truncated_ref)
        try:
            if self.print_output:
                print(' - Check out ' + ref_output)
                print(self.repo.git.checkout(truncated_ref))
            else:
                self.repo.git.checkout(truncated_ref)
        except GitError as err:
            message = colored(' - Failed to checkout ref ', 'red')
            if self.print_output:
                print(message + ref_output)
                print_error(err)
            raise ClowderGitException(msg=message + ref_output)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def clean(self, args=''):
        """Discard changes for repo"""
        if self.print_output:
            print(' - Clean project')
        clean_args = '-f' if args == '' else '-f' + args
        self._clean(args=clean_args)
        if self.print_output:
            print(' - Reset project')
        self._reset_head()
        if self._is_rebase_in_progress():
            if self.print_output:
                print(' - Abort rebase in progress')
            self._abort_rebase()

    def create_clowder_repo(self, url, remote, branch, depth=0):
        """Clone clowder git repo from url at path"""
        if existing_git_repository(self.repo_path):
            return
        self._init_repo()
        self._create_remote(remote, url, remove_dir=True)
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
            if upstream_remote_url == self._remote_get_url(remote.name):
                if remote.name != upstream_remote_name:
                    self._rename_remote(remote.name, upstream_remote_name)
                    continue
            if fork_remote_url == self._remote_get_url(remote.name):
                if remote.name != fork_remote_name:
                    self._rename_remote(remote.name, fork_remote_name)
        remote_names = [r.name for r in self.repo.remotes]
        if upstream_remote_name in remote_names:
            if upstream_remote_url != self._remote_get_url(upstream_remote_name):
                actual_url = self._remote_get_url(upstream_remote_name)
                message = format_remote_already_exists_error(upstream_remote_name,
                                                             upstream_remote_url,
                                                             actual_url)
                if self.print_output:
                    print(message)
                raise ClowderGitException(msg=message)
        if fork_remote_name in remote_names:
            if fork_remote_url != self._remote_get_url(fork_remote_name):
                actual_url = self._remote_get_url(fork_remote_name)
                message = format_remote_already_exists_error(fork_remote_name,
                                                             fork_remote_url,
                                                             actual_url)
                if self.print_output:
                    print(message)
                raise ClowderGitException(msg=message)

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
            if self.print_output:
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
                if self.print_output:
                    print(' - Fetch from ' + remote_output + ' ' + ref_output)
                message = colored(' - Failed to fetch from ', 'red')
                error = message + remote_output + ' ' + ref_output
                command = ['git', 'fetch', remote, truncate_ref(ref), '--depth', str(depth), '--prune', '--tags']
        return_code = execute_command(command, self.repo_path, print_output=self.print_output)
        if return_code != 0:
            if self.print_output:
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
            raise ClowderGitException(msg=colored(' - Failed to create remote', 'red'))
        self._herd(remote, ref, depth=depth, fetch=fetch, rebase=rebase)

    def herd_branch(self, url, remote, branch, default_ref, depth=0, rebase=False, fork_remote=None):
        """Herd branch"""
        if not existing_git_repository(self.repo_path):
            self._herd_branch_initial(url, remote, branch, default_ref, depth=depth)
            return
        branch_output = format_ref_string(branch)
        branch_ref = 'refs/heads/' + branch
        if self.existing_local_branch(branch):
            if self._is_branch_checked_out(branch):
                if self.print_output:
                    print(' - Branch ' + branch_output + ' already checked out')
            else:
                self._checkout_branch_local(branch)
            self.fetch(remote, depth=depth, ref=branch_ref)
            if self.existing_remote_branch(branch, remote):
                self._herd_remote_branch(remote, branch, depth=depth, rebase=rebase)
                return
            if fork_remote is not None:
                self.fetch(fork_remote, depth=depth, ref=branch_ref)
                if self.existing_remote_branch(branch, fork_remote):
                    self._herd_remote_branch(fork_remote, branch, depth=depth, rebase=rebase)
            return
        self.fetch(remote, depth=depth, ref=branch_ref)
        if self.existing_remote_branch(branch, remote):
            self._herd(remote, branch_ref, depth=depth, fetch=False, rebase=rebase)
            return
        else:
            remote_output = format_remote_string(remote)
            if self.print_output:
                print(' - No existing remote branch ' + remote_output + ' ' + branch_output)
        if fork_remote is not None:
            self.fetch(fork_remote, depth=depth, ref=branch_ref)
            if self.existing_remote_branch(branch, fork_remote):
                self._herd(fork_remote, branch_ref, depth=depth, fetch=False, rebase=rebase)
                return
            else:
                remote_output = format_remote_string(fork_remote)
                if self.print_output:
                    print(' - No existing remote branch ' + remote_output + ' ' + branch_output)
        fetch = depth != 0
        self.herd(url, remote, default_ref, depth=depth, fetch=fetch, rebase=rebase)

    def herd_tag(self, url, remote, tag, default_ref, depth=0, rebase=False):
        """Herd tag"""
        if not existing_git_repository(self.repo_path):
            self._init_repo()
            self._create_remote(remote, url, remove_dir=True)
            return_code = self._checkout_new_repo_tag(tag, remote, depth)
            if return_code == 0:
                return
            fetch = depth != 0
            self.herd(url, remote, default_ref, depth=depth, fetch=fetch, rebase=rebase)
            return
        return_code = self.fetch(remote, ref='refs/tags/' + tag, depth=depth)
        if return_code == 0:
            return_code = self._checkout_tag(tag)
            if return_code == 0:
                return
        fetch = depth != 0
        self.herd(url, remote, default_ref, depth=depth, fetch=fetch, rebase=rebase)

    def herd_remote(self, url, remote, default_ref, branch=None):
        """Herd remote repo"""
        return_code = self._create_remote(remote, url)
        if return_code != 0:
            raise ClowderGitException(msg=colored(' - Failed to create remote', 'red'))
        if branch is not None:
            return_code = self.fetch(remote, ref=branch)
            if return_code == 0:
                return
        return_code = self.fetch(remote, ref=default_ref)
        if return_code != 0:
            raise ClowderGitException(msg=colored(' - Failed to fetch', 'red'))

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
        return_code = execute_command(command, self.repo_path, print_output=self.print_output)
        if return_code != 0:
            if self.print_output:
                cprint(' - Failed to print branches', 'red')
                print_command_failed_error(command)
            raise ClowderGitException

    def prune_branch_local(self, branch, default_ref, force):
        """Prune branch in repository"""
        branch_output = format_ref_string(branch)
        if branch not in self.repo.heads:
            if self.print_output:
                print(' - Local branch ' + branch_output + " doesn't exist")
            return
        prune_branch = self.repo.heads[branch]
        if self.repo.head.ref == prune_branch:
            ref_output = format_ref_string(truncate_ref(default_ref))
            try:
                if self.print_output:
                    print(' - Checkout ref ' + ref_output)
                self.repo.git.checkout(truncate_ref(default_ref))
            except GitError as err:
                if self.print_output:
                    message = colored(' - Failed to checkout ref', 'red')
                    print(message + ref_output)
                    print_error(err)
                raise ClowderGitException
            except (KeyboardInterrupt, SystemExit):
                sys.exit(1)
        try:
            if self.print_output:
                print(' - Delete local branch ' + branch_output)
            self.repo.delete_head(branch, force=force)
            return
        except GitError as err:
            if self.print_output:
                message = colored(' - Failed to delete local branch ', 'red')
                print(message + branch_output)
                print_error(err)
            raise ClowderGitException
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def prune_branch_remote(self, branch, remote):
        """Prune remote branch in repository"""
        origin = self._remote(remote)
        if origin is None:
            raise ClowderGitException
        branch_output = format_ref_string(branch)
        if branch not in origin.refs:
            if self.print_output:
                print(' - Remote branch ' + branch_output + " doesn't exist")
            return
        try:
            if self.print_output:
                print(' - Delete remote branch ' + branch_output)
            self.repo.git.push(remote, '--delete', branch)
        except GitError as err:
            if self.print_output:
                message = colored(' - Failed to delete remote branch ', 'red')
                print(message + branch_output)
                print_error(err)
            raise ClowderGitException
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def reset(self, remote, ref, depth=0):
        """Reset branch to upstream or checkout tag/sha as detached HEAD"""
        if ref_type(ref) == 'branch':
            branch = truncate_ref(ref)
            branch_output = format_ref_string(branch)
            if not self.existing_local_branch(branch):
                return_code = self._create_branch_local_tracking(branch, remote, depth=depth, fetch=True)
                if return_code != 0:
                    raise ClowderGitException(msg=colored(' - Failed to create tracking branch', 'red'))
                return
            elif self._is_branch_checked_out(branch):
                if self.print_output:
                    print(' - Branch ' + branch_output + ' already checked out')
            else:
                self._checkout_branch_local(branch)
            remote_output = format_remote_string(remote)
            if not self.existing_remote_branch(branch, remote):
                message = colored(' - No existing remote branch ', 'red')
                if self.print_output:
                    print(message + remote_output + ' ' + branch_output)
                raise ClowderGitException(msg=message + remote_output + ' ' + branch_output)
            self.fetch(remote, depth=depth, ref=ref)
            if self.print_output:
                print(' - Reset branch ' + branch_output + ' to ' + remote_output + ' ' + branch_output)
            remote_branch = remote + '/' + branch
            self._reset_head(branch=remote_branch)
        elif ref_type(ref) == 'tag':
            self.fetch(remote, depth=depth, ref=ref)
            self._checkout_tag(truncate_ref(ref))
        elif ref_type(ref) == 'sha':
            self.fetch(remote, depth=depth, ref=ref)
            self._checkout_sha(ref)

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
                    raise ClowderGitException
            return_code = self._create_branch_local(branch)
            if return_code != 0:
                raise ClowderGitException
            return_code = self._checkout_branch_local(branch)
            if return_code != 0:
                raise ClowderGitException
        else:
            branch_output = format_ref_string(branch)
            if self.print_output:
                print(' - ' + branch_output + ' already exists')
            correct_branch = self._is_branch_checked_out(branch)
            if correct_branch:
                if self.print_output:
                    print(' - On correct branch')
            else:
                return_code = self._checkout_branch_local(branch)
                if return_code != 0:
                    raise ClowderGitException
        if tracking and not is_offline():
            self._create_branch_remote_tracking(branch, remote, depth)

    def stash(self):
        """Stash current changes in repository"""
        if not self.repo.is_dirty():
            if self.print_output:
                print(' - No changes to stash')
            return
        if self.print_output:
            print(' - Stash current changes')
        self.repo.git.stash()

    def sync(self, upstream_remote, fork_remote, ref, rebase=False):
        """Sync fork with upstream remote"""
        if self.print_output:
            print(' - Sync fork with upstream remote')
        if ref_type(ref) != 'branch':
            message = colored(' - Can only sync branches', 'red')
            if self.print_output:
                print(message)
            raise ClowderGitException(msg=message)
        fork_remote_output = format_remote_string(fork_remote)
        branch_output = format_ref_string(truncate_ref(ref))
        if rebase:
            self._rebase_remote_branch(upstream_remote, truncate_ref(ref))
        else:
            self._pull(upstream_remote, truncate_ref(ref))
        if self.print_output:
            print(' - Push to ' + fork_remote_output + ' ' + branch_output)
        command = ['git', 'push', fork_remote, truncate_ref(ref)]
        return_code = execute_command(command, self.repo_path, print_output=self.print_output)
        if return_code != 0:
            if self.print_output:
                message = colored(' - Failed to push to ', 'red')
                print(message + fork_remote_output + ' ' + branch_output)
                print_command_failed_error(command)
            raise ClowderGitException(msg=colored(' - Failed to push', 'red'))

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
            if self.print_output:
                cprint(' - Failed to abort rebase', 'red')
                print_error(err)
            raise ClowderGitException
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _checkout_branch_local(self, branch, remove_dir=False):
        """Checkout local branch"""
        branch_output = format_ref_string(branch)
        try:
            if self.print_output:
                print(' - Checkout branch ' + branch_output)
            default_branch = self.repo.heads[branch]
            default_branch.checkout()
            return 0
        except GitError as err:
            if self.print_output:
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
        remote_output = format_remote_string(remote)
        origin = self._remote(remote)
        if origin is None:
            remove_directory_exit(self.repo_path)
        self.fetch(remote, depth=depth, ref=branch, remove_dir=True)
        if not self.existing_remote_branch(branch, remote):
            if self.print_output:
                message = colored(' - No existing remote branch ', 'red')
                print(message + remote_output + ' ' + branch_output)
            remove_directory_exit(self.repo_path)
        self._create_branch_local_tracking(branch, remote, depth=depth, fetch=False, remove_dir=True)

    def _checkout_new_repo_commit(self, commit, remote, depth):
        """Checkout commit or fail and delete repo if it doesn't exist"""
        commit_output = format_ref_string(commit)
        origin = self._remote(remote)
        if origin is None:
            remove_directory_exit(self.repo_path)
        self.fetch(remote, depth=depth, ref=commit, remove_dir=True)
        if self.print_output:
            print(' - Checkout commit ' + commit_output)
        try:
            self.repo.git.checkout(commit)
        except GitError as err:
            if self.print_output:
                message = colored(' - Failed to checkout commit ', 'red')
                print(message + commit_output)
                print_error(err)
            remove_directory_exit(self.repo_path)
        except (KeyboardInterrupt, SystemExit):
            remove_directory_exit(self.repo_path)

    def _checkout_new_repo_tag(self, tag, remote, depth, remove_dir=False):
        """Checkout tag or fail and delete repo if it doesn't exist"""
        tag_output = format_ref_string(tag)
        origin = self._remote(remote)
        if origin is None:
            if remove_dir:
                remove_directory_exit(self.repo_path)
            return 1
        self.fetch(remote, depth=depth, ref='refs/tags/' + tag, remove_dir=remove_dir)
        try:
            remote_tag = self.repo.tags[tag]
        except (GitError, IndexError):
            message = ' - No existing tag '
            if remove_dir:
                if self.print_output:
                    print(colored(message, 'red') + tag_output)
                remove_directory_exit(self.repo_path)
            if self.print_output:
                print(message + tag_output)
            return 1
        except (KeyboardInterrupt, SystemExit):
            if remove_dir:
                remove_directory_exit(self.repo_path)
            sys.exit(1)
        else:
            try:
                if self.print_output:
                    print(' - Checkout tag ' + tag_output)
                self.repo.git.checkout(remote_tag)
                return 0
            except GitError as err:
                if self.print_output:
                    message = colored(' - Failed to checkout tag ', 'red')
                    print(message + tag_output)
                    print_error(err)
                if remove_dir:
                    remove_directory_exit(self.repo_path)
                return 1
            except (KeyboardInterrupt, SystemExit):
                if remove_dir:
                    remove_directory_exit(self.repo_path)
                sys.exit(1)

    def _checkout_sha(self, sha):
        """Checkout commit by sha"""
        commit_output = format_ref_string(sha)
        try:
            same_sha = self.repo.head.commit.hexsha == sha
            is_detached = self.repo.head.is_detached
            if same_sha and is_detached:
                if self.print_output:
                    print(' - On correct commit')
                return 0
            if self.print_output:
                print(' - Checkout commit ' + commit_output)
            self.repo.git.checkout(sha)
        except GitError as err:
            message = colored(' - Failed to checkout commit ', 'red')
            if self.print_output:
                print(message + commit_output)
                print_error(err)
            raise ClowderGitException(msg=message + commit_output)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _checkout_tag(self, tag):
        """Checkout commit tag is pointing to"""
        tag_output = format_ref_string(tag)
        if tag not in self.repo.tags:
            if self.print_output:
                print(' - No existing tag ' + tag_output)
            return 1
        try:
            same_commit = self.repo.head.commit == self.repo.tags[tag].commit
            is_detached = self.repo.head.is_detached
            if same_commit and is_detached:
                if self.print_output:
                    print(' - On correct commit for tag')
                return 0
            if self.print_output:
                print(' - Checkout tag ' + tag_output)
            self.repo.git.checkout('refs/tags/' + tag)
            return 0
        except (GitError, ValueError) as err:
            message = colored(' - Failed to checkout tag ', 'red')
            if self.print_output:
                print(message + tag_output)
                print_error(err)
            raise ClowderGitException(msg=message + tag_output)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _clean(self, args):
        """Clean git directory"""
        try:
            self.repo.git.clean(args)
        except GitError as err:
            if self.print_output:
                cprint(' - Failed to clean git repo', 'red')
                print_error(err)
            raise ClowderGitException
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _create_branch_local(self, branch):
        """Create local branch"""
        branch_output = format_ref_string(branch)
        try:
            if self.print_output:
                print(' - Create branch ' + branch_output)
            self.repo.create_head(branch)
            return 0
        except GitError as err:
            if self.print_output:
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
            if self.print_output:
                print(' - Create branch ' + branch_output)
            self.repo.create_head(branch, origin.refs[branch])
        except (GitError, IndexError) as err:
            if self.print_output:
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
            raise ClowderGitException
        return_code = self.fetch(remote, depth=depth, ref=branch)
        if return_code != 0:
            raise ClowderGitException
        if branch in origin.refs:
            try:
                self.repo.git.config('--get', 'branch.' + branch + '.merge')
                if self.print_output:
                    print(' - Tracking branch ' + branch_output + ' already exists')
                return
            except GitError:
                if self.print_output:
                    message_1 = colored(' - Remote branch ', 'red')
                    message_2 = colored(' already exists', 'red')
                    print(message_1 + branch_output + message_2 + '\n')
                raise ClowderGitException
            except (KeyboardInterrupt, SystemExit):
                sys.exit(1)
        try:
            if self.print_output:
                print(' - Push remote branch ' + branch_output)
            self.repo.git.push(remote, branch)
            return_code = self._set_tracking_branch(remote, branch)
            if return_code != 0:
                raise ClowderGitException
        except GitError as err:
            if self.print_output:
                message = colored(' - Failed to push remote branch ', 'red')
                print(message + branch_output)
                print_error(err)
            raise ClowderGitException
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _create_remote(self, remote, url, remove_dir=False):
        """Create new remote"""
        remote_names = [r.name for r in self.repo.remotes]
        if remote in remote_names:
            return 0
        remote_output = format_remote_string(remote)
        try:
            if self.print_output:
                print(' - Create remote ' + remote_output)
            self.repo.create_remote(remote, url)
            return 0
        except GitError as err:
            if self.print_output:
                message = colored(' - Failed to create remote ', 'red')
                print(message + remote_output)
                print_error(err)
            if remove_dir:
                remove_directory_exit(self.repo_path)
            return 1
        except (KeyboardInterrupt, SystemExit):
            if remove_dir:
                remove_directory_exit(self.repo_path)
            sys.exit(1)

    def _existing_remote_tag(self, tag, remote, depth=0):
        """Check if remote tag exists"""
        origin = self._remote(remote)
        if origin is None:
            remove_directory_exit(self.repo_path)
        self.fetch(remote, depth=depth, ref=tag, remove_dir=True)
        return tag in origin.tags

    def _herd(self, remote, ref, depth=0, fetch=True, rebase=False):
        """Herd ref"""
        if ref_type(ref) == 'branch':
            branch = truncate_ref(ref)
            if not self.existing_local_branch(branch):
                return_code = self._create_branch_local_tracking(branch, remote, depth=depth, fetch=fetch)
                if return_code != 0:
                    raise ClowderGitException(msg=colored(' - Failed to create tracking branch', 'red'))
                return
            elif self._is_branch_checked_out(branch):
                branch_output = format_ref_string(branch)
                if self.print_output:
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
            self._pull(remote, branch)
        elif ref_type(ref) == 'tag':
            self.fetch(remote, depth=depth, ref=ref)
            self._checkout_tag(truncate_ref(ref))
        elif ref_type(ref) == 'sha':
            self.fetch(remote, depth=depth, ref=ref)
            self._checkout_sha(ref)

    def _herd_initial(self, url, remote, ref, depth=0):
        """Herd ref initial"""
        self._init_repo()
        self._create_remote(remote, url, remove_dir=True)
        if ref_type(ref) == 'branch':
            self._checkout_new_repo_branch(truncate_ref(ref), remote, depth)
        elif ref_type(ref) == 'tag':
            self._checkout_new_repo_tag(truncate_ref(ref), remote, depth, remove_dir=True)
        elif ref_type(ref) == 'sha':
            self._checkout_new_repo_commit(ref, remote, depth)

    def _herd_branch_initial(self, url, remote, branch, default_ref, depth=0):
        """Herd branch initial"""
        self._init_repo()
        self._create_remote(remote, url, remove_dir=True)
        self.fetch(remote, depth=depth, ref=branch)
        if not self.existing_remote_branch(branch, remote):
            remote_output = format_remote_string(remote)
            if self.print_output:
                print(' - No existing remote branch ' + remote_output + ' ' + format_ref_string(branch))
            self._herd_initial(url, remote, default_ref, depth=depth)
            return
        self._create_branch_local_tracking(branch, remote, depth=depth, fetch=False, remove_dir=True)

    def _herd_remote_branch(self, remote, branch, depth=0, rebase=False):
        """Herd remote branch"""
        if not self._is_tracking_branch(branch):
            self._set_tracking_branch_commit(branch, remote, depth)
            return
        if rebase:
            self._rebase_remote_branch(remote, branch)
            return
        self._pull(remote, branch)

    def _init_repo(self):
        """Initialize repository"""
        if existing_git_repository(self.repo_path):
            return
        try:
            if self.print_output:
                print(' - Initialize repo at ' + format_path(self.repo_path))
            if not os.path.isdir(self.repo_path):
                os.makedirs(self.repo_path)
            self.repo = Repo.init(self.repo_path)
        except GitError as err:
            if self.print_output:
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
            if self.print_output:
                message = colored(' - No existing branch ', 'red')
                print(message + branch_output)
                print_error(err)
            raise ClowderGitException
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _pull(self, remote, branch):
        """Pull from remote branch"""
        if self.repo.head.is_detached:
            if self.print_output:
                print(' - HEAD is detached')
            return
        branch_output = format_ref_string(branch)
        remote_output = format_remote_string(remote)
        if self.print_output:
            print(' - Pull from ' + remote_output + ' ' + branch_output)
        command = ['git', 'pull', remote, branch]
        return_code = execute_command(command, self.repo_path, print_output=self.print_output)
        if return_code != 0:
            message = colored(' - Failed to pull from ', 'red')
            if self.print_output:
                print(message + remote_output + ' ' + branch_output)
                print_command_failed_error(command)
            raise ClowderGitException(msg=message + remote_output + ' ' + branch_output)

    def _rebase_remote_branch(self, remote, branch):
        """Rebase from remote branch"""
        if self.repo.head.is_detached:
            if self.print_output:
                print(' - HEAD is detached')
            return
        branch_output = format_ref_string(branch)
        remote_output = format_remote_string(remote)
        if self.print_output:
            print(' - Rebase onto ' + remote_output + ' ' + branch_output)
        command = ['git', 'pull', '--rebase', remote, branch]
        return_code = execute_command(command, self.repo_path, print_output=self.print_output)
        if return_code != 0:
            message = colored(' - Failed to rebase onto ', 'red')
            if self.print_output:
                print(message + remote_output + ' ' + branch_output)
                print_command_failed_error(command)
            raise ClowderGitException(msg=message + remote_output + ' ' + branch_output)

    def _remote(self, remote):
        """Get remote"""
        remote_output = format_remote_string(remote)
        try:
            return self.repo.remotes[remote]
        except GitError as err:
            if self.print_output:
                message = colored(' - No existing remote ', 'red')
                print(message + remote_output)
                print_error(err)
            return None
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _remote_get_url(self, remote):
        """Reset head of repo, discarding changes"""
        return self.repo.git.remote('get-url', remote)

    def _rename_remote(self, remote_from, remote_to):
        """Rename remote"""
        remote_output_from = format_remote_string(remote_from)
        remote_output_to = format_remote_string(remote_to)
        if self.print_output:
            print(' - Rename remote ' + remote_output_from + ' to ' + remote_output_to)
        try:
            self.repo.git.remote('rename', remote_from, remote_to)
        except GitError as err:
            message = colored(' - Failed to rename remote', 'red')
            if self.print_output:
                print(message)
                print_error(err)
            raise ClowderGitException(msg=message)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _repo(self):
        """Create Repo instance for path"""
        try:
            repo = Repo(self.repo_path)
            return repo
        except GitError as err:
            message = colored("Failed to create Repo instance for ", 'red')
            repo_path_output = format_path(self.repo_path)
            if self.print_output:
                print(message + repo_path_output)
                print_error(err)
            raise ClowderGitException(msg=message + repo_path_output)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _reset_head(self, branch=None):
        """Reset head of repo, discarding changes"""
        if branch is None:
            try:
                self.repo.head.reset(index=True, working_tree=True)
                return 0
            except GitError as err:
                if self.print_output:
                    message = colored(' - Failed to reset ', 'red')
                    print(message + format_ref_string('HEAD'))
                    print_error(err)
                return 1
            except (KeyboardInterrupt, SystemExit):
                sys.exit(1)
        else:
            try:
                self.repo.git.reset('--hard', branch)
                return 0
            except GitError as err:
                if self.print_output:
                    message = colored(' - Failed to reset to ', 'red')
                    print(message + format_ref_string(branch))
                    print_error(err)
                return 1
            except (KeyboardInterrupt, SystemExit):
                sys.exit(1)

    def _set_tracking_branch(self, remote, branch, remove_dir=False):
        """Set tracking branch"""
        branch_output = format_ref_string(branch)
        remote_output = format_remote_string(remote)
        origin = self._remote(remote)
        try:
            local_branch = self.repo.heads[branch]
            remote_branch = origin.refs[branch]
            if self.print_output:
                print(' - Set tracking branch ' + branch_output + ' -> ' + remote_output + ' ' + branch_output)
            local_branch.set_tracking_branch(remote_branch)
            return 0
        except GitError as err:
            if self.print_output:
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
            raise ClowderGitException(msg=colored(' - Failed to fech', 'red'))
        if not self.existing_local_branch(branch):
            if self.print_output:
                message_1 = colored(' - No local branch ', 'red')
                print(message_1 + branch_output + '\n')
            raise ClowderGitException(msg=colored(' - No local branch', 'red'))
        if not self.existing_remote_branch(branch, remote):
            if self.print_output:
                message_1 = colored(' - No remote branch ', 'red')
                print(message_1 + branch_output + '\n')
            raise ClowderGitException(msg=colored(' - No remote branch', 'red'))
        local_branch = self.repo.heads[branch]
        remote_branch = origin.refs[branch]
        if local_branch.commit != remote_branch.commit:
            message_1 = colored(' - Existing remote branch ', 'red')
            message_2 = colored(' on different commit', 'red')
            if self.print_output:
                print(message_1 + branch_output + message_2 + '\n')
            raise ClowderGitException(msg=message_1 + branch_output + message_2 + '\n')
        return_code = self._set_tracking_branch(remote, branch)
        if return_code != 0:
            raise ClowderGitException(msg=colored(' - Failed to set tracking branch', 'red'))

    def _untracked_files(self):
        """Execute command and display continuous output"""
        command = "git ls-files -o -d --exclude-standard | sed q | wc -l| tr -d '[:space:]'"
        try:
            output = subprocess.check_output(command, shell=True, cwd=self.repo_path)
            return output.decode('utf-8') == '1'
        except GitError as err:
            if self.print_output:
                cprint(' - Failed to check untracked files', 'red')
                print_error(err)
            raise ClowderGitException
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)
