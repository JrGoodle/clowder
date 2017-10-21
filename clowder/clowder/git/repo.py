"""Git utilities"""

from __future__ import print_function

import os
import subprocess
import sys

from git import Repo, GitError
from termcolor import colored, cprint

import clowder.util.formatting as fmt
from clowder.error.clowder_git_error import ClowderGitError
from clowder.util.connectivity import is_offline
from clowder.util.execute import execute_command
from clowder.util.file_system import remove_directory


DEFAULT_REF = 'refs/heads/master'
DEFAULT_REMOTE = 'origin'


class GitRepo(object):
    """Class encapsulating git utilities"""

    def __init__(self, repo_path, remote, default_ref, print_output=True):
        self.repo_path = repo_path
        self.default_ref = default_ref
        self.remote = remote
        self.print_output = print_output
        self.repo = self._repo() if GitRepo.existing_git_repository(repo_path) else None

    def checkout(self, truncated_ref):
        """Checkout git ref"""
        ref_output = fmt.ref_string(truncated_ref)
        try:
            self._print(' - Check out ' + ref_output)
            if self.print_output:
                print(self.repo.git.checkout(truncated_ref))
                return
            self.repo.git.checkout(truncated_ref)
        except GitError as err:
            message = colored(' - Failed to checkout ref ', 'red')
            self._print(message + ref_output)
            self._print(fmt.error(err))
            self._exit(fmt.parallel_exception_error(self.repo_path, message, ref_output))
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def clean(self, args=''):
        """Discard changes for repo"""
        self._print(' - Clean project')
        clean_args = '-f' if args == '' else '-f' + args
        self._clean(args=clean_args)
        self._print(' - Reset project')
        self._reset_head()
        if self._is_rebase_in_progress():
            self._print(' - Abort rebase in progress')
            self._abort_rebase()

    def create_clowder_repo(self, url, branch, depth=0):
        """Clone clowder git repo from url at path"""
        if GitRepo.existing_git_repository(self.repo_path):
            return
        self._init_repo()
        self._create_remote(self.remote, url, remove_dir=True)
        self._checkout_new_repo_branch(branch, depth)

    def configure_remotes(self, upstream_remote_name, upstream_remote_url, fork_remote_name, fork_remote_url):
        """Configure remotes names for fork and upstream"""
        if not GitRepo.existing_git_repository(self.repo_path):
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
                message = fmt.remote_already_exists_error(upstream_remote_name, upstream_remote_url, actual_url)
                self._print(message)
                self._exit(fmt.parallel_exception_error(self.repo_path, message))
        if fork_remote_name in remote_names:
            if fork_remote_url != self._remote_get_url(fork_remote_name):
                actual_url = self._remote_get_url(fork_remote_name)
                message = fmt.remote_already_exists_error(fork_remote_name, fork_remote_url, actual_url)
                self._print(message)
                self._exit(fmt.parallel_exception_error(self.repo_path, message))

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

    @staticmethod
    def existing_git_repository(path):
        """Check if a git repository exists"""
        return os.path.isdir(os.path.join(path, '.git'))

    @staticmethod
    def existing_git_submodule(path):
        """Check if a git submodule exists"""
        return os.path.isfile(os.path.join(path, '.git'))

    @staticmethod
    def exists(repo_path):
        """Print existence validation messages"""
        if not GitRepo.existing_git_repository(repo_path):
            cprint(' - Project is missing', 'red')

    def fetch(self, remote, ref=None, depth=0, remove_dir=False):
        """Fetch from a specific remote ref"""
        remote_output = fmt.remote_string(remote)
        if depth == 0:
            self._print(' - Fetch from ' + remote_output)
            message = colored(' - Failed to fetch from ', 'red')
            error = message + remote_output
            command = ['git', 'fetch', remote, '--prune', '--tags']
        else:
            if ref is None:
                command = ['git', 'fetch', remote, '--depth', str(depth), '--prune', '--tags']
                message = colored(' - Failed to fetch remote ', 'red')
                error = message + remote_output
            else:
                ref_output = fmt.ref_string(GitRepo.truncate_ref(ref))
                self._print(' - Fetch from ' + remote_output + ' ' + ref_output)
                message = colored(' - Failed to fetch from ', 'red')
                error = message + remote_output + ' ' + ref_output
                command = ['git', 'fetch', remote, GitRepo.truncate_ref(ref),
                           '--depth', str(depth), '--prune', '--tags']
        return_code = execute_command(command, self.repo_path, print_output=self.print_output)
        if return_code != 0:
            if remove_dir:
                remove_directory(self.repo_path)
            self._print(error)
            self._exit(fmt.parallel_exception_error(self.repo_path, error))
        return return_code

    @staticmethod
    def format_project_ref_string(repo_path):
        """Return formatted repo ref name"""
        repo = GitRepo(repo_path, DEFAULT_REMOTE, DEFAULT_REF)
        local_commits = repo.new_commits()
        upstream_commits = repo.new_commits(upstream=True)
        no_local_commits = local_commits == 0 or local_commits == '0'
        no_upstream_commits = upstream_commits == 0 or upstream_commits == '0'
        if no_local_commits and no_upstream_commits:
            status = ''
        else:
            local_commits_output = colored('+' + str(local_commits), 'yellow')
            upstream_commits_output = colored('-' + str(upstream_commits), 'red')
            status = '[' + local_commits_output + '/' + upstream_commits_output + ']'

        if repo.is_detached():
            current_ref = repo.sha(short=True)
            return colored('(HEAD @ ' + current_ref + ')', 'magenta')
        current_branch = repo.current_branch()
        return colored('(' + current_branch + ')', 'magenta') + status

    @staticmethod
    def format_project_string(repo_path, name):
        """Return formatted project name"""
        if not GitRepo.existing_git_repository(repo_path):
            return colored(name, 'green')
        repo = GitRepo(repo_path, DEFAULT_REMOTE, DEFAULT_REF)
        if not repo.validate_repo():
            color = 'red'
            symbol = '*'
        else:
            color = 'green'
            symbol = ''
        return colored(name + symbol, color)

    def herd(self, url, depth=0, fetch=True, rebase=False):
        """Herd ref"""
        if not GitRepo.existing_git_repository(self.repo_path):
            self._herd_initial(url, depth=depth)
            return
        return_code = self._create_remote(self.remote, url)
        if return_code != 0:
            raise ClowderGitError(msg=colored(' - Failed to create remote', 'red'))
        self._herd(self.remote, self.default_ref, depth=depth, fetch=fetch, rebase=rebase)

    def herd_branch(self, url, branch, depth=0, rebase=False, fork_remote=None):
        """Herd branch"""
        if not GitRepo.existing_git_repository(self.repo_path):
            self._herd_branch_initial(url, branch, depth=depth)
            return
        branch_output = fmt.ref_string(branch)
        branch_ref = 'refs/heads/' + branch
        if self.existing_local_branch(branch):
            if self._is_branch_checked_out(branch):
                self._print(' - Branch ' + branch_output + ' already checked out')
            else:
                self._checkout_branch_local(branch)
            self.fetch(self.remote, depth=depth, ref=branch_ref)
            if self.existing_remote_branch(branch, self.remote):
                self._herd_remote_branch(self.remote, branch, depth=depth, rebase=rebase)
                return
            if fork_remote:
                self.fetch(fork_remote, depth=depth, ref=branch_ref)
                if self.existing_remote_branch(branch, fork_remote):
                    self._herd_remote_branch(fork_remote, branch, depth=depth, rebase=rebase)
            return
        self.fetch(self.remote, depth=depth, ref=branch_ref)
        if self.existing_remote_branch(branch, self.remote):
            self._herd(self.remote, branch_ref, depth=depth, fetch=False, rebase=rebase)
            return
        else:
            remote_output = fmt.remote_string(self.remote)
            self._print(' - No existing remote branch ' + remote_output + ' ' + branch_output)
        if fork_remote:
            self.fetch(fork_remote, depth=depth, ref=branch_ref)
            if self.existing_remote_branch(branch, fork_remote):
                self._herd(fork_remote, branch_ref, depth=depth, fetch=False, rebase=rebase)
                return
            else:
                remote_output = fmt.remote_string(fork_remote)
                self._print(' - No existing remote branch ' + remote_output + ' ' + branch_output)
        fetch = depth != 0
        self.herd(url, depth=depth, fetch=fetch, rebase=rebase)

    def herd_tag(self, url, tag, depth=0, rebase=False):
        """Herd tag"""
        if not GitRepo.existing_git_repository(self.repo_path):
            self._init_repo()
            self._create_remote(self.remote, url, remove_dir=True)
            return_code = self._checkout_new_repo_tag(tag, self.remote, depth)
            if return_code == 0:
                return
            fetch = depth != 0
            self.herd(url, depth=depth, fetch=fetch, rebase=rebase)
            return
        return_code = self.fetch(self.remote, ref='refs/tags/' + tag, depth=depth)
        if return_code == 0:
            return_code = self._checkout_tag(tag)
            if return_code == 0:
                return
        fetch = depth != 0
        self.herd(url, depth=depth, fetch=fetch, rebase=rebase)

    def herd_remote(self, url, remote, branch=None):
        """Herd remote repo"""
        return_code = self._create_remote(remote, url)
        if return_code != 0:
            raise ClowderGitError(msg=colored(' - Failed to create remote', 'red'))
        if branch:
            return_code = self.fetch(remote, ref=branch)
            if return_code == 0:
                return
        return_code = self.fetch(remote, ref=self.default_ref)
        if return_code != 0:
            raise ClowderGitError(msg=colored(' - Failed to fetch', 'red'))

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
            cprint(' - Failed to print branches', 'red')
            print(fmt.command_failed_error(command))
            sys.exit(1)

    def prune_branch_local(self, branch, force):
        """Prune branch in repository"""
        branch_output = fmt.ref_string(branch)
        if branch not in self.repo.heads:
            self._print(' - Local branch ' + branch_output + " doesn't exist")
            return
        prune_branch = self.repo.heads[branch]
        if self.repo.head.ref == prune_branch:
            ref_output = fmt.ref_string(GitRepo.truncate_ref(self.default_ref))
            try:
                self._print(' - Checkout ref ' + ref_output)
                self.repo.git.checkout(GitRepo.truncate_ref(self.default_ref))
            except GitError as err:
                message = colored(' - Failed to checkout ref', 'red')
                print(message + ref_output)
                print(fmt.error(err))
                sys.exit(1)
            except (KeyboardInterrupt, SystemExit):
                sys.exit(1)
        try:
            self._print(' - Delete local branch ' + branch_output)
            self.repo.delete_head(branch, force=force)
            return
        except GitError as err:
            message = colored(' - Failed to delete local branch ', 'red')
            print(message + branch_output)
            print(fmt.error(err))
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def prune_branch_remote(self, branch, remote):
        """Prune remote branch in repository"""
        origin = self._remote(remote)
        branch_output = fmt.ref_string(branch)
        if branch not in origin.refs:
            self._print(' - Remote branch ' + branch_output + " doesn't exist")
            return
        try:
            self._print(' - Delete remote branch ' + branch_output)
            self.repo.git.push(remote, '--delete', branch)
        except GitError as err:
            message = colored(' - Failed to delete remote branch ', 'red')
            print(message + branch_output)
            print(fmt.error(err))
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    @staticmethod
    def ref_type(ref):
        """Return branch, tag, sha, or unknown ref type"""
        git_branch = "refs/heads/"
        git_tag = "refs/tags/"
        if ref.startswith(git_branch):
            return 'branch'
        elif ref.startswith(git_tag):
            return 'tag'
        elif len(ref) == 40:
            return 'sha'
        return 'unknown'

    def reset(self, depth=0):
        """Reset branch to upstream or checkout tag/sha as detached HEAD"""
        if GitRepo.ref_type(self.default_ref) == 'branch':
            branch = GitRepo.truncate_ref(self.default_ref)
            branch_output = fmt.ref_string(branch)
            if not self.existing_local_branch(branch):
                return_code = self._create_branch_local_tracking(branch, self.remote, depth=depth, fetch=True)
                if return_code != 0:
                    message = colored(' - Failed to create tracking branch ', 'red') + branch_output
                    self._print(message)
                    self._exit(fmt.parallel_exception_error(self.repo_path, message))
                return
            elif self._is_branch_checked_out(branch):
                self._print(' - Branch ' + branch_output + ' already checked out')
            else:
                self._checkout_branch_local(branch)
            remote_output = fmt.remote_string(self.remote)
            if not self.existing_remote_branch(branch, self.remote):
                message = colored(' - No existing remote branch ', 'red') + remote_output + ' ' + branch_output
                self._print(message)
                self._exit(fmt.parallel_exception_error(self.repo_path, message))
            self.fetch(self.remote, ref=self.default_ref, depth=depth)
            self._print(' - Reset branch ' + branch_output + ' to ' + remote_output + ' ' + branch_output)
            remote_branch = self.remote + '/' + branch
            self._reset_head(branch=remote_branch)
        elif GitRepo.ref_type(self.default_ref) == 'tag':
            self.fetch(self.remote, ref=self.default_ref, depth=depth)
            self._checkout_tag(GitRepo.truncate_ref(self.default_ref))
        elif GitRepo.ref_type(self.default_ref) == 'sha':
            self.fetch(self.remote, ref=self.default_ref, depth=depth)
            self._checkout_sha(self.default_ref)

    def sha(self, short=False):
        """Return sha for currently checked out commit"""
        if short:
            return self.repo.git.rev_parse(self.repo.head.commit.hexsha, short=True)
        return self.repo.head.commit.hexsha

    def start(self, remote, branch, depth, tracking):
        """Start new branch in repository"""
        if branch not in self.repo.heads:
            if not is_offline():
                return_code = self.fetch(remote, ref=branch, depth=depth)
                if return_code != 0:
                    sys.exit(1)
            return_code = self._create_branch_local(branch)
            if return_code != 0:
                sys.exit(1)
            return_code = self._checkout_branch_local(branch)
            if return_code != 0:
                sys.exit(1)
        else:
            branch_output = fmt.ref_string(branch)
            print(' - ' + branch_output + ' already exists')
            correct_branch = self._is_branch_checked_out(branch)
            if correct_branch:
                print(' - On correct branch')
            else:
                return_code = self._checkout_branch_local(branch)
                if return_code != 0:
                    sys.exit(1)
        if tracking and not is_offline():
            self._create_branch_remote_tracking(branch, remote, depth)

    def stash(self):
        """Stash current changes in repository"""
        if not self.repo.is_dirty():
            print(' - No changes to stash')
            return
        print(' - Stash current changes')
        self.repo.git.stash()

    def status(self):
        """Print  git status"""
        self.repo.git.status()

    @staticmethod
    def status_verbose(repo_path):
        """Print git status"""
        command = ['git', 'status', '-vv']
        print(fmt.command(command))
        return_code = execute_command(command, repo_path)
        if return_code != 0:
            cprint(' - Failed to print status', 'red')
            print(fmt.command_failed_error(command))
            sys.exit(return_code)

    def sync(self, fork_remote, rebase=False):
        """Sync fork with upstream remote"""
        if self.print_output:
            print(' - Sync fork with upstream remote')
        if GitRepo.ref_type(self.default_ref) != 'branch':
            message = colored(' - Can only sync branches', 'red')
            self._print(message)
            self._exit(fmt.parallel_exception_error(self.repo_path, message))
        fork_remote_output = fmt.remote_string(fork_remote)
        branch_output = fmt.ref_string(GitRepo.truncate_ref(self.default_ref))
        if rebase:
            self._rebase_remote_branch(self.remote, GitRepo.truncate_ref(self.default_ref))
        else:
            self._pull(self.remote, GitRepo.truncate_ref(self.default_ref))
        self._print(' - Push to ' + fork_remote_output + ' ' + branch_output)
        command = ['git', 'push', fork_remote, GitRepo.truncate_ref(self.default_ref)]
        return_code = execute_command(command, self.repo_path, print_output=self.print_output)
        if return_code != 0:
            message = colored(' - Failed to push to ', 'red')
            self._print(message + fork_remote_output + ' ' + branch_output)
            self._print(fmt.command_failed_error(command))
            self._exit(fmt.parallel_exception_error(self.repo_path, message, fork_remote_output, ' ', branch_output))

    @staticmethod
    def truncate_ref(ref):
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

    def validate_repo(self):
        """Validate repo state"""
        if not GitRepo.existing_git_repository(self.repo_path):
            return True
        return not self.is_dirty()

    @staticmethod
    def validation(repo_path):
        """Print validation messages"""
        repo = GitRepo(repo_path, DEFAULT_REMOTE, DEFAULT_REF)
        if not GitRepo.existing_git_repository(repo_path):
            return
        if not repo.validate_repo():
            print(' - Dirty repo. Please stash, commit, or discard your changes')
            GitRepo.status_verbose(repo_path)

    def _abort_rebase(self):
        """Abort rebase"""
        if not self._is_rebase_in_progress():
            return
        try:
            self.repo.git.rebase('--abort')
        except GitError as err:
            self._print(colored(' - Failed to abort rebase', 'red'))
            self._print(fmt.error(err))
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _checkout_branch_local(self, branch, remove_dir=False):
        """Checkout local branch"""
        branch_output = fmt.ref_string(branch)
        try:
            self._print(' - Checkout branch ' + branch_output)
            default_branch = self.repo.heads[branch]
            default_branch.checkout()
            return 0
        except GitError as err:
            if remove_dir:
                remove_directory(self.repo_path)
            message = colored(' - Failed to checkout branch ', 'red')
            self._print(message + branch_output)
            self._print(fmt.error(err))
            self._exit(fmt.parallel_exception_error(self.repo_path, message, branch_output))
        except (KeyboardInterrupt, SystemExit):
            if remove_dir:
                remove_directory(self.repo_path)
            sys.exit(1)

    def _checkout_new_repo_branch(self, branch, depth):
        """Checkout remote branch or fail and delete repo if it doesn't exist"""
        branch_output = fmt.ref_string(branch)
        remote_output = fmt.remote_string(self.remote)
        self._remote(self.remote, remove_dir=True)
        self.fetch(self.remote, depth=depth, ref=branch, remove_dir=True)
        if not self.existing_remote_branch(branch, self.remote):
            remove_directory(self.repo_path)
            message = colored(' - No existing remote branch ', 'red')
            self._print(message + remote_output + ' ' + branch_output)
            self._exit(fmt.parallel_exception_error(self.repo_path, message, remote_output, ' ', branch_output))
        self._create_branch_local_tracking(branch, self.remote, depth=depth, fetch=False, remove_dir=True)

    def _checkout_new_repo_commit(self, commit, remote, depth):
        """Checkout commit or fail and delete repo if it doesn't exist"""
        commit_output = fmt.ref_string(commit)
        self._remote(remote, remove_dir=True)
        self.fetch(remote, depth=depth, ref=commit, remove_dir=True)
        self._print(' - Checkout commit ' + commit_output)
        try:
            self.repo.git.checkout(commit)
        except GitError as err:
            remove_directory(self.repo_path)
            message = colored(' - Failed to checkout commit ', 'red')
            self._print(message + commit_output)
            self._print(fmt.error(err))
            self._exit(fmt.parallel_exception_error(self.repo_path, message, commit_output))
        except (KeyboardInterrupt, SystemExit):
            remove_directory(self.repo_path)
            sys.exit(1)

    def _checkout_new_repo_tag(self, tag, remote, depth, remove_dir=False):
        """Checkout tag or fail and delete repo if it doesn't exist"""
        tag_output = fmt.ref_string(tag)
        self._remote(remote, remove_dir=remove_dir)
        self.fetch(remote, depth=depth, ref='refs/tags/' + tag, remove_dir=remove_dir)
        try:
            remote_tag = self.repo.tags[tag]
        except (GitError, IndexError):
            message = ' - No existing tag '
            if remove_dir:
                remove_directory(self.repo_path)
                self._print(colored(message, 'red') + tag_output)
                self._exit(fmt.parallel_exception_error(self.repo_path, colored(message, 'red'), tag_output))
            if self.print_output:
                print(message + tag_output)
            return 1
        except (KeyboardInterrupt, SystemExit):
            if remove_dir:
                remove_directory(self.repo_path)
            sys.exit(1)
        else:
            try:
                self._print(' - Checkout tag ' + tag_output)
                self.repo.git.checkout(remote_tag)
                return 0
            except GitError as err:
                message = colored(' - Failed to checkout tag ', 'red')
                self._print(message + tag_output)
                self._print(fmt.error(err))
                if remove_dir:
                    remove_directory(self.repo_path)
                    self._exit(fmt.parallel_exception_error(self.repo_path, message, tag_output))
                return 1
            except (KeyboardInterrupt, SystemExit):
                if remove_dir:
                    remove_directory(self.repo_path)
                sys.exit(1)

    def _checkout_sha(self, sha):
        """Checkout commit by sha"""
        commit_output = fmt.ref_string(sha)
        try:
            same_sha = self.repo.head.commit.hexsha == sha
            is_detached = self.repo.head.is_detached
            self._print(' - On correct commit')
            if same_sha and is_detached:
                return 0
            self._print(' - Checkout commit ' + commit_output)
            self.repo.git.checkout(sha)
        except GitError as err:
            message = colored(' - Failed to checkout commit ', 'red')
            self._print(message + commit_output)
            self._print(fmt.error(err))
            self._exit(fmt.parallel_exception_error(self.repo_path, message, commit_output))
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _checkout_tag(self, tag):
        """Checkout commit tag is pointing to"""
        tag_output = fmt.ref_string(tag)
        if tag not in self.repo.tags:
            self._print(' - No existing tag ' + tag_output)
            return 1
        try:
            same_commit = self.repo.head.commit == self.repo.tags[tag].commit
            is_detached = self.repo.head.is_detached
            if same_commit and is_detached:
                self._print(' - On correct commit for tag')
                return 0
            self._print(' - Checkout tag ' + tag_output)
            self.repo.git.checkout('refs/tags/' + tag)
            return 0
        except (GitError, ValueError) as err:
            message = colored(' - Failed to checkout tag ', 'red')
            self._print(message + tag_output)
            self._print(fmt.error(err))
            self._exit(fmt.parallel_exception_error(self.repo_path, message, tag_output))
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _clean(self, args):
        """Clean git directory"""
        try:
            self.repo.git.clean(args)
        except GitError as err:
            cprint(' - Failed to clean git repo', 'red')
            print(fmt.error(err))
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _create_branch_local(self, branch):
        """Create local branch"""
        branch_output = fmt.ref_string(branch)
        try:
            self._print(' - Create branch ' + branch_output)
            self.repo.create_head(branch)
            return 0
        except GitError as err:
            message = colored(' - Failed to create branch ', 'red')
            self._print(message + branch_output)
            self._print(fmt.error(err))
            return 1
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _create_branch_local_tracking(self, branch, remote, depth, fetch=True, remove_dir=False):
        """Create and checkout tracking branch"""
        branch_output = fmt.ref_string(branch)
        origin = self._remote(remote, remove_dir=remove_dir)
        if fetch:
            return_code = self.fetch(remote, depth=depth, ref=branch, remove_dir=remove_dir)
            if return_code != 0:
                return return_code
        try:
            self._print(' - Create branch ' + branch_output)
            self.repo.create_head(branch, origin.refs[branch])
        except (GitError, IndexError) as err:
            message = colored(' - Failed to create branch ', 'red')
            if remove_dir:
                remove_directory(self.repo_path)
            self._print(message + branch_output)
            self._print(fmt.error(err))
            self._exit(fmt.parallel_exception_error(self.repo_path, message, branch_output))
        except (KeyboardInterrupt, SystemExit):
            if remove_dir:
                remove_directory(self.repo_path)
            sys.exit(1)
        else:
            return_code = self._set_tracking_branch(remote, branch, remove_dir=remove_dir)
            if return_code != 0:
                return return_code
            return self._checkout_branch_local(branch, remove_dir=remove_dir)

    def _create_branch_remote_tracking(self, branch, remote, depth):
        """Create remote tracking branch"""
        branch_output = fmt.ref_string(branch)
        origin = self._remote(remote)
        return_code = self.fetch(remote, depth=depth, ref=branch)
        if return_code != 0:
            sys.exit(1)
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
                sys.exit(1)
        except GitError as err:
            message = colored(' - Failed to push remote branch ', 'red')
            print(message + branch_output)
            print(fmt.error(err))
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _create_remote(self, remote, url, remove_dir=False):
        """Create new remote"""
        remote_names = [r.name for r in self.repo.remotes]
        if remote in remote_names:
            return 0
        remote_output = fmt.remote_string(remote)
        try:
            self._print(' - Create remote ' + remote_output)
            self.repo.create_remote(remote, url)
            return 0
        except GitError as err:
            message = colored(' - Failed to create remote ', 'red')
            if remove_dir:
                remove_directory(self.repo_path)
            self._print(message + remote_output)
            self._print(fmt.error(err))
            self._exit(fmt.parallel_exception_error(self.repo_path, message, remote_output))
        except (KeyboardInterrupt, SystemExit):
            if remove_dir:
                remove_directory(self.repo_path)
            sys.exit(1)

    def _existing_remote_tag(self, tag, remote, depth=0):
        """Check if remote tag exists"""
        origin = self._remote(remote, remove_dir=True)
        self.fetch(remote, depth=depth, ref=tag, remove_dir=True)
        return tag in origin.tags

    def _exit(self, message):
        """Print output if print_output is True"""
        if self.print_output:
            sys.exit(1)
        raise ClowderGitError(msg=message)

    def _herd(self, remote, ref, depth=0, fetch=True, rebase=False):
        """Herd ref"""
        if GitRepo.ref_type(ref) == 'branch':
            branch = GitRepo.truncate_ref(ref)
            branch_output = fmt.ref_string(branch)
            if not self.existing_local_branch(branch):
                return_code = self._create_branch_local_tracking(branch, remote, depth=depth, fetch=fetch)
                if return_code != 0:
                    message = colored(' - Failed to create tracking branch ', 'red')
                    self._exit(fmt.parallel_exception_error(self.repo_path, message, branch_output))
                return
            elif self._is_branch_checked_out(branch):
                self._print(' - Branch ' + branch_output + ' already checked out')
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
        elif GitRepo.ref_type(ref) == 'tag':
            self.fetch(remote, depth=depth, ref=ref)
            self._checkout_tag(GitRepo.truncate_ref(ref))
        elif GitRepo.ref_type(ref) == 'sha':
            self.fetch(remote, depth=depth, ref=ref)
            self._checkout_sha(ref)

    def _herd_initial(self, url, depth=0):
        """Herd ref initial"""
        self._init_repo()
        self._create_remote(self.remote, url, remove_dir=True)
        if GitRepo.ref_type(self.default_ref) == 'branch':
            self._checkout_new_repo_branch(GitRepo.truncate_ref(self.default_ref), depth)
        elif GitRepo.ref_type(self.default_ref) == 'tag':
            self._checkout_new_repo_tag(GitRepo.truncate_ref(self.default_ref), self.remote, depth, remove_dir=True)
        elif GitRepo.ref_type(self.default_ref) == 'sha':
            self._checkout_new_repo_commit(self.default_ref, self.remote, depth)

    def _herd_branch_initial(self, url, branch, depth=0):
        """Herd branch initial"""
        self._init_repo()
        self._create_remote(self.remote, url, remove_dir=True)
        self.fetch(self.remote, depth=depth, ref=branch)
        if not self.existing_remote_branch(branch, self.remote):
            remote_output = fmt.remote_string(self.remote)
            self._print(' - No existing remote branch ' + remote_output + ' ' + fmt.ref_string(branch))
            self._herd_initial(url, depth=depth)
            return
        self._create_branch_local_tracking(branch, self.remote, depth=depth, fetch=False, remove_dir=True)

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
        if GitRepo.existing_git_repository(self.repo_path):
            return
        try:
            self._print(' - Initialize repo at ' + fmt.path(self.repo_path))
            if not os.path.isdir(self.repo_path):
                try:
                    os.makedirs(self.repo_path)
                except OSError as err:
                    if err.errno != os.errno.EEXIST:
                        raise
            self.repo = Repo.init(self.repo_path)
        except GitError as err:
            remove_directory(self.repo_path)
            message = colored(' - Failed to initialize repository', 'red')
            self._print(message)
            self._print(fmt.error(err))
            self._exit(fmt.parallel_exception_error(self.repo_path, message))
        except (KeyboardInterrupt, SystemExit):
            remove_directory(self.repo_path)
            sys.exit(1)

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
        branch_output = fmt.ref_string(branch)
        try:
            local_branch = self.repo.heads[branch]
            tracking_branch = local_branch.tracking_branch()
            return True if tracking_branch else False
        except GitError as err:
            message = colored(' - No existing branch ', 'red')
            self._print(message + branch_output)
            self._print(fmt.error(err))
            self._exit(fmt.parallel_exception_error(self.repo_path, message, branch_output))
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _print(self, val):
        """Print output if print_output is True"""
        if self.print_output:
            print(val)

    def _pull(self, remote, branch):
        """Pull from remote branch"""
        if self.repo.head.is_detached:
            self._print(' - HEAD is detached')
            return
        branch_output = fmt.ref_string(branch)
        remote_output = fmt.remote_string(remote)
        self._print(' - Pull from ' + remote_output + ' ' + branch_output)
        command = ['git', 'pull', remote, branch]
        return_code = execute_command(command, self.repo_path, print_output=self.print_output)
        if return_code != 0:
            message = colored(' - Failed to pull from ', 'red')
            self._print(message + remote_output + ' ' + branch_output)
            self._print(fmt.command_failed_error(command))
            self._exit(fmt.parallel_exception_error(self.repo_path, message, remote_output, ' ', branch_output))

    def _rebase_remote_branch(self, remote, branch):
        """Rebase from remote branch"""
        if self.repo.head.is_detached:
            self._print(' - HEAD is detached')
            return
        branch_output = fmt.ref_string(branch)
        remote_output = fmt.remote_string(remote)
        self._print(' - Rebase onto ' + remote_output + ' ' + branch_output)
        command = ['git', 'pull', '--rebase', remote, branch]
        return_code = execute_command(command, self.repo_path, print_output=self.print_output)
        if return_code != 0:
            message = colored(' - Failed to rebase onto ', 'red')
            self._print(message + remote_output + ' ' + branch_output)
            self._print(fmt.command_failed_error(command))
            self._exit(fmt.parallel_exception_error(self.repo_path, message, remote_output, ' ', branch_output))

    def _remote(self, remote, remove_dir=False):
        """Get remote"""
        remote_output = fmt.remote_string(remote)
        try:
            return self.repo.remotes[remote]
        except GitError as err:
            message = colored(' - No existing remote ', 'red')
            if remove_dir:
                remove_directory(self.repo_path)
            self._print(message + remote_output)
            self._print(fmt.error(err))
            self._exit(fmt.parallel_exception_error(self.repo_path, message, remote_output))
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _remote_get_url(self, remote):
        """Reset head of repo, discarding changes"""
        return self.repo.git.remote('get-url', remote)

    def _rename_remote(self, remote_from, remote_to):
        """Rename remote"""
        remote_output_from = fmt.remote_string(remote_from)
        remote_output_to = fmt.remote_string(remote_to)
        self._print(' - Rename remote ' + remote_output_from + ' to ' + remote_output_to)
        try:
            self.repo.git.remote('rename', remote_from, remote_to)
        except GitError as err:
            message_1 = colored(' - Failed to rename remote from ', 'red')
            message_2 = remote_output_from + ' to ' + remote_output_to
            self._print(message_1 + message_2)
            self._print(fmt.error(err))
            self._exit(fmt.parallel_exception_error(self.repo_path, message_1, message_2))
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _repo(self):
        """Create Repo instance for path"""
        try:
            repo = Repo(self.repo_path)
            return repo
        except GitError as err:
            message = colored(" - Failed to create Repo instance for ", 'red')
            repo_path_output = fmt.path(self.repo_path)
            self._print(message + repo_path_output)
            self._print(fmt.error(err))
            self._exit(fmt.parallel_exception_error(self.repo_path, message, repo_path_output))
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def _reset_head(self, branch=None):
        """Reset head of repo, discarding changes"""
        if branch is None:
            try:
                self.repo.head.reset(index=True, working_tree=True)
                return 0
            except GitError as err:
                message = colored(' - Failed to reset ', 'red')
                ref_output = fmt.ref_string('HEAD')
                self._print(message + ref_output)
                self._print(fmt.error(err))
                self._exit(fmt.parallel_exception_error(self.repo_path, message, ref_output))
            except (KeyboardInterrupt, SystemExit):
                sys.exit(1)
        else:
            try:
                self.repo.git.reset('--hard', branch)
                return 0
            except GitError as err:
                message = colored(' - Failed to reset to ', 'red')
                branch_output = fmt.ref_string(branch)
                self._print(message + branch_output)
                self._print(fmt.error(err))
                self._exit(fmt.parallel_exception_error(self.repo_path, message, branch_output))
            except (KeyboardInterrupt, SystemExit):
                sys.exit(1)

    def _set_tracking_branch(self, remote, branch, remove_dir=False):
        """Set tracking branch"""
        branch_output = fmt.ref_string(branch)
        remote_output = fmt.remote_string(remote)
        origin = self._remote(remote)
        try:
            local_branch = self.repo.heads[branch]
            remote_branch = origin.refs[branch]
            self._print(' - Set tracking branch ' + branch_output + ' -> ' + remote_output + ' ' + branch_output)
            local_branch.set_tracking_branch(remote_branch)
            return 0
        except GitError as err:
            message = colored(' - Failed to set tracking branch ', 'red')
            if remove_dir:
                remove_directory(self.repo_path)
            self._print(message + branch_output)
            self._print(fmt.error(err))
            self._exit(fmt.parallel_exception_error(self.repo_path, message, branch_output))
        except (KeyboardInterrupt, SystemExit):
            if remove_dir:
                remove_directory(self.repo_path)
            sys.exit(1)

    def _set_tracking_branch_commit(self, branch, remote, depth):
        """Set tracking relationship between local and remote branch if on same commit"""
        branch_output = fmt.ref_string(branch)
        origin = self._remote(remote)
        return_code = self.fetch(remote, depth=depth, ref=branch)
        if return_code != 0:
            raise ClowderGitError(msg=colored(' - Failed to fech', 'red'))
        if not self.existing_local_branch(branch):
            message = colored(' - No local branch ', 'red')
            self._print(message + branch_output + '\n')
            self._exit(fmt.parallel_exception_error(self.repo_path, message, branch_output, '\n'))
        if not self.existing_remote_branch(branch, remote):
            message = colored(' - No remote branch ', 'red')
            self._print(message + branch_output + '\n')
            self._exit(fmt.parallel_exception_error(self.repo_path, message, branch_output, '\n'))
        local_branch = self.repo.heads[branch]
        remote_branch = origin.refs[branch]
        if local_branch.commit != remote_branch.commit:
            message_1 = colored(' - Existing remote branch ', 'red')
            message_2 = colored(' on different commit', 'red')
            self._print(message_1 + branch_output + message_2 + '\n')
            self._exit(fmt.parallel_exception_error(self.repo_path, message_1, branch_output, message_2, '\n'))
        return_code = self._set_tracking_branch(remote, branch)
        if return_code != 0:
            self._exit(colored(' - Failed to set tracking branch', 'red'))

    def _untracked_files(self):
        """Execute command and display continuous output"""
        command = "git ls-files -o -d --exclude-standard | sed q | wc -l| tr -d '[:space:]'"
        try:
            output = subprocess.check_output(command, shell=True, cwd=self.repo_path)
            return output.decode('utf-8') == '1'
        except GitError as err:
            self._print(fmt.error(err))
            self._exit(colored(' - Failed to check untracked files', 'red'))
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)
