"""Git utilities"""

from __future__ import print_function

import os
import subprocess
import sys

from git import Repo, GitError
from termcolor import colored, cprint

import clowder.util.formatting as fmt
from clowder.error.clowder_git_error import ClowderGitError
from clowder.util.execute import execute_command
from clowder.util.file_system import remove_directory

__repo_default_ref__ = 'refs/heads/master'
__repo_default_remote__ = 'origin'


class GitRepo(object):
    """Class encapsulating git utilities"""

    def __init__(self, repo_path, remote, default_ref, parallel=False, print_output=True):
        self.repo_path = repo_path
        self.default_ref = default_ref
        self.remote = remote
        self.print_output = print_output
        self.parallel = parallel
        self.repo = self._repo() if GitRepo.existing_git_repository(repo_path) else None

    def add(self, files):
        """Add files to git index"""

        self._print(' - Add files to git index')
        try:
            print(self.repo.git.add(files))
        except GitError as err:
            message = cprint(' - Failed to add files to git index\n', 'red') + fmt.error(err)
            self._print(message)
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            self._exit()
        else:
            self.status_verbose()

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
            self._exit()

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

    def commit(self, message):
        """Commit current changes"""

        try:
            self._print(' - Commit current changes')
            print(self.repo.git.commit(message=message))
        except GitError as err:
            message = colored(' - Failed to commit current changes', 'red')
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            self._exit()

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
            self._exit()

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

    def fetch(self, remote, ref=None, depth=0, remove_dir=False):
        """Fetch from a specific remote ref"""

        remote_output = fmt.remote_string(remote)
        if depth == 0:
            self._print(' - Fetch from ' + remote_output)
            message = colored(' - Failed to fetch from ', 'red')
            error = message + remote_output
            command = ['git fetch', remote, '--prune --tags']
        elif ref is None:
            command = ['git fetch', remote, '--depth', str(depth), '--prune --tags']
            message = colored(' - Failed to fetch remote ', 'red')
            error = message + remote_output
        else:
            ref_output = fmt.ref_string(GitRepo.truncate_ref(ref))
            self._print(' - Fetch from ' + remote_output + ' ' + ref_output)
            message = colored(' - Failed to fetch from ', 'red')
            error = message + remote_output + ' ' + ref_output
            command = ['git fetch', remote, GitRepo.truncate_ref(ref), '--depth', str(depth), '--prune --tags']

        return_code = execute_command(command, self.repo_path, print_output=self.print_output)
        if return_code != 0:
            if remove_dir:
                remove_directory(self.repo_path)
            self._print(error)
            self._exit(error)
        return return_code

    def get_current_timestamp(self):
        """Get current timestamp of HEAD commit"""

        try:
            return self.repo.git.log('-1', '--format=%cI')
        except GitError as err:
            message = colored(' - Failed to find rev from timestamp', 'red')
            self._print(message)
            self._print(fmt.error(err))
            self._exit(fmt.error(err))
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    def is_detached(self, print_output=False):
        """Check if HEAD is detached"""

        if not os.path.isdir(self.repo_path):
            return False
        if self.repo.head.is_detached:
            if print_output:
                self._print(' - HEAD is detached')
            return True
        return False

    def is_dirty(self):
        """Check whether repo is dirty"""

        if not os.path.isdir(self.repo_path):
            return False

        return self._is_dirty() or self._is_rebase_in_progress() or self._untracked_files()

    def new_commits(self, upstream=False):
        """Returns the number of new commits"""

        try:
            local_branch = self.repo.active_branch
        except (GitError, TypeError):
            return 0
        except (KeyboardInterrupt, SystemExit):
            self._exit()
        else:
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
                self._exit()

    def print_branches(self, local=False, remote=False):
        """Print branches"""

        if local and remote:
            command = 'git branch -a'
        elif local:
            command = 'git branch'
        elif remote:
            command = 'git branch -r'
        else:
            return

        return_code = execute_command(command, self.repo_path, print_output=self.print_output)
        if return_code != 0:
            message = colored(' - Failed to print branches', 'red')
            self._print(message)
            self._exit(message)

    def pull(self):
        """Pull upstream changes"""

        if self.is_detached(print_output=True):
            return

        try:
            self._print(' - Pull latest changes')
            print(self.repo.git.pull())
        except GitError as err:
            message = colored(' - Failed to pull latest changes', 'red')
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    def push(self):
        """Push changes"""

        if self.is_detached(print_output=True):
            return

        try:
            self._print(' - Push local changes')
            print(self.repo.git.push())
        except GitError as err:
            message = colored(' - Failed to push local changes', 'red')
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            self._exit()

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

    def sha(self, short=False):
        """Return sha for currently checked out commit"""

        if short:
            return self.repo.git.rev_parse(self.repo.head.commit.hexsha, short=True)
        return self.repo.head.commit.hexsha

    def sha_branch_remote(self, remote, branch):
        """Return sha for remote branch"""

        command = "git --git-dir={0}.git rev-parse {1}/{2}".format(self.repo_path, remote, branch)
        return_code = execute_command(command, self.repo_path)
        if return_code != 0:
            message = colored(' - Failed to get remote sha\n', 'red') + fmt.command_failed_error(command)
            self._print(message)
            self._exit(message, return_code=return_code)

    def stash(self):
        """Stash current changes in repository"""

        if not self.repo.is_dirty():
            self._print(' - No changes to stash')
            return

        self._print(' - Stash current changes')
        self.repo.git.stash()

    def status(self):
        """Print  git status"""

        self.repo.git.status()

    def status_verbose(self):
        """Print git status"""

        command = 'git status -vv'
        self._print(fmt.command(command))

        return_code = execute_command(command, self.repo_path)
        if return_code != 0:
            message = colored(' - Failed to print status\n', 'red') + fmt.command_failed_error(command)
            self._print(message)
            self._exit(message, return_code=return_code)

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

        repo = GitRepo(repo_path, __repo_default_remote__, __repo_default_ref__)
        if not GitRepo.existing_git_repository(repo_path):
            return

        if not repo.validate_repo():
            print(' - Dirty repo. Please stash, commit, or discard your changes')
            repo.status_verbose()

    def _abort_rebase(self):
        """Abort rebase"""

        if not self._is_rebase_in_progress():
            return

        try:
            self.repo.git.rebase('--abort')
        except GitError as err:
            self._print(colored(' - Failed to abort rebase', 'red'))
            self._print(fmt.error(err))
            self._exit(fmt.error(err))
        except (KeyboardInterrupt, SystemExit):
            self._exit()

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
            self._exit()

    def _checkout_new_repo_branch(self, branch, depth):
        """Checkout remote branch or fail and delete repo if it doesn't exist"""

        branch_output = fmt.ref_string(branch)
        remote_output = fmt.remote_string(self.remote)
        self._remote(self.remote, remove_dir=True)
        self.fetch(self.remote, depth=depth, ref=branch, remove_dir=True)

        if not self.existing_remote_branch(branch, self.remote):
            remove_directory(self.repo_path)
            message = colored(' - No existing remote branch ', 'red') + remote_output + ' ' + branch_output
            self._print(message)
            self._exit(fmt.parallel_exception_error(self.repo_path, message))

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
            self._exit()

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
                self._print(message + tag_output)
            return 1
        except (KeyboardInterrupt, SystemExit):
            if remove_dir:
                remove_directory(self.repo_path)
            self._exit()
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
                self._exit()

    def _checkout_sha(self, sha):
        """Checkout commit by sha"""

        commit_output = fmt.ref_string(sha)
        try:
            if self.repo.head.commit.hexsha == sha:
                self._print(' - On correct commit')
                return 0
            self._print(' - Checkout commit ' + commit_output)
            self.repo.git.checkout(sha)
        except GitError as err:
            message = colored(' - Failed to checkout commit ', 'red')
            self._print(message + commit_output)
            self._print(fmt.error(err))
            self._exit(fmt.parallel_exception_error(self.repo_path, message, commit_output))
        except (KeyboardInterrupt, SystemExit):
            self._exit()

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
            self._exit()

    def _clean(self, args):
        """Clean git directory"""

        try:
            self.repo.git.clean(args)
        except GitError as err:
            message = colored(' - Failed to clean git repo', 'red')
            self._print(message)
            self._print(fmt.error(err))
            self._exit(fmt.error(err))
        except (KeyboardInterrupt, SystemExit):
            self._exit()

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
            self._exit()

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
            message = colored(' - Failed to create branch ', 'red') + branch_output
            if remove_dir:
                remove_directory(self.repo_path)
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            if remove_dir:
                remove_directory(self.repo_path)
            self._exit()
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
            self._exit('', return_code=return_code)

        if branch in origin.refs:
            try:
                self.repo.git.config('--get', 'branch.' + branch + '.merge')
                self._print(' - Tracking branch ' + branch_output + ' already exists')
                return
            except GitError:
                message_1 = colored(' - Remote branch ', 'red')
                message_2 = colored(' already exists', 'red')
                message = message_1 + branch_output + message_2 + '\n'
                self._print(message)
                self._exit(message)
            except (KeyboardInterrupt, SystemExit):
                self._exit()

        try:
            self._print(' - Push remote branch ' + branch_output)
            self.repo.git.push(remote, branch)
            return_code = self._set_tracking_branch(remote, branch)
            if return_code != 0:
                self._exit('', return_code=return_code)
        except GitError as err:
            message = colored(' - Failed to push remote branch ', 'red') + branch_output
            self._print(message)
            self._print(fmt.error(err))
            self._exit(fmt.error(err))
        except (KeyboardInterrupt, SystemExit):
            self._exit()

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
            self._exit()

    def _existing_remote_tag(self, tag, remote, depth=0):
        """Check if remote tag exists"""

        origin = self._remote(remote, remove_dir=True)
        self.fetch(remote, depth=depth, ref=tag, remove_dir=True)
        return tag in origin.tags

    def _exit(self, message='', return_code=1):
        """Exit based on serial or parallel job"""

        if self.parallel:
            raise ClowderGitError(msg=fmt.parallel_exception_error(self.repo_path, message))
        sys.exit(return_code)

    def _find_rev_by_timestamp(self, timestamp, ref):
        """Find rev by timestamp"""

        try:
            return self.repo.git.log('-1', '--format=%H', '--before=' + timestamp, ref)
        except GitError as err:
            message = colored(' - Failed to find rev from timestamp', 'red')
            self._print(message)
            self._print(fmt.error(err))
            self._exit(fmt.error(err))
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    def _find_rev_by_timestamp_author(self, timestamp, author, ref):
        """Find rev by timestamp and author"""

        try:
            return self.repo.git.log('-1', '--format=%H', '--before=' + timestamp, '--author', author, ref)
        except GitError as err:
            message = colored(' - Failed to find rev from timestamp by author', 'red')
            self._print(message)
            self._print(fmt.error(err))
            self._exit(fmt.error(err))
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    def _init_repo(self):
        """Initialize repository"""

        if GitRepo.existing_git_repository(self.repo_path):
            return

        try:
            self._print(' - Initialize repo at ' + fmt.get_path(self.repo_path))
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
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            remove_directory(self.repo_path)
            self._exit()

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
            self._exit()

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
            message = colored(' - No existing branch ', 'red') + branch_output
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    def _print(self, val):
        """Print output if print_output is True"""

        if self.print_output:
            print(val)

    def _pull(self, remote, branch):
        """Pull from remote branch"""

        if self.is_detached(print_output=True):
            return

        branch_output = fmt.ref_string(branch)
        remote_output = fmt.remote_string(remote)
        self._print(' - Pull from ' + remote_output + ' ' + branch_output)
        command = ['git pull', remote, branch]

        return_code = execute_command(command, self.repo_path, print_output=self.print_output)
        if return_code != 0:
            message = colored(' - Failed to pull from ', 'red') + remote_output + ' ' + branch_output
            self._print(message)
            self._exit(message)

    def _rebase_remote_branch(self, remote, branch):
        """Rebase from remote branch"""

        if self.is_detached(print_output=True):
            return

        branch_output = fmt.ref_string(branch)
        remote_output = fmt.remote_string(remote)
        self._print(' - Rebase onto ' + remote_output + ' ' + branch_output)
        command = ['git pull --rebase', remote, branch]

        return_code = execute_command(command, self.repo_path, print_output=self.print_output)
        if return_code != 0:
            message = colored(' - Failed to rebase onto ', 'red') + remote_output + ' ' + branch_output
            self._print(message)
            self._print(fmt.command_failed_error(command))
            self._exit(message)

    def _remote(self, remote, remove_dir=False):
        """Get remote"""

        remote_output = fmt.remote_string(remote)
        try:
            return self.repo.remotes[remote]
        except GitError as err:
            message = colored(' - No existing remote ', 'red') + remote_output
            if remove_dir:
                remove_directory(self.repo_path)
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    def _remote_get_url(self, remote):
        """Get url of remote"""

        return self.repo.git.remote('get-url', remote)

    def _rename_remote(self, remote_from, remote_to):
        """Rename remote"""

        remote_output_f = fmt.remote_string(remote_from)
        remote_output_t = fmt.remote_string(remote_to)
        self._print(' - Rename remote ' + remote_output_f + ' to ' + remote_output_t)
        try:
            self.repo.git.remote('rename', remote_from, remote_to)
        except GitError as err:
            message = colored(' - Failed to rename remote from ', 'red') + remote_output_f + ' to ' + remote_output_t
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    def _repo(self):
        """Create Repo instance for path"""

        try:
            repo = Repo(self.repo_path)
            return repo
        except GitError as err:
            repo_path_output = fmt.get_path(self.repo_path)
            message = colored(" - Failed to create Repo instance for ", 'red') + repo_path_output
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    def _reset_head(self, branch=None):
        """Reset head of repo, discarding changes"""

        if branch is None:
            try:
                self.repo.head.reset(index=True, working_tree=True)
                return 0
            except GitError as err:
                ref_output = fmt.ref_string('HEAD')
                message = colored(' - Failed to reset ', 'red') + ref_output
                self._print(message)
                self._print(fmt.error(err))
                self._exit(message)
            except (KeyboardInterrupt, SystemExit):
                self._exit()

        try:
            self.repo.git.reset('--hard', branch)
            return 0
        except GitError as err:
            branch_output = fmt.ref_string(branch)
            message = colored(' - Failed to reset to ', 'red') + branch_output
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            self._exit()

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
            message = colored(' - Failed to set tracking branch ', 'red') + branch_output
            if remove_dir:
                remove_directory(self.repo_path)
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            if remove_dir:
                remove_directory(self.repo_path)
            self._exit()

    def _untracked_files(self):
        """Execute command and display continuous output"""

        command = "git ls-files -o -d --exclude-standard | sed q | wc -l| tr -d '[:space:]'"
        try:
            output = subprocess.check_output(command, shell=True, cwd=self.repo_path)
            return output.decode('utf-8') == '1'
        except GitError as err:
            message = colored(' - Failed to check untracked files', 'red')
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            self._exit()
