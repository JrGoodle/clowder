"""Project git utilities"""

from __future__ import print_function

import sys

from git import GitError
from termcolor import colored, cprint

import clowder.util.formatting as fmt
from clowder.error.clowder_git_error import ClowderGitError
from clowder.git.repo import execute_command, GitRepo
from clowder.util.connectivity import is_offline

DEFAULT_REF = 'refs/heads/master'
DEFAULT_REMOTE = 'origin'


class ProjectRepo(GitRepo):
    """Class encapsulating git utilities"""

    def __init__(self, repo_path, remote, default_ref, parallel=False, print_output=True):
        GitRepo.__init__(self, repo_path, remote, default_ref, parallel=parallel, print_output=print_output)

    def create_clowder_repo(self, url, branch, depth=0):
        """Clone clowder git repo from url at path"""
        if self.existing_git_repository(self.repo_path):
            return
        self._init_repo()
        self._create_remote(self.remote, url, remove_dir=True)
        self._checkout_new_repo_branch(branch, depth)

    def configure_remotes(self, upstream_remote_name, upstream_remote_url, fork_remote_name, fork_remote_url):
        """Configure remotes names for fork and upstream"""
        if not self.existing_git_repository(self.repo_path):
            return
        try:
            remotes = self.repo.remotes
        except GitError:
            return
        except (KeyboardInterrupt, SystemExit):
            self._exit('')
        else:
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
                self._compare_remote_url(upstream_remote_name, upstream_remote_url)
            if fork_remote_name in remote_names:
                self._compare_remote_url(fork_remote_name, fork_remote_url)

    @staticmethod
    def exists(repo_path):
        """Print existence validation messages"""
        if not ProjectRepo.existing_git_repository(repo_path):
            cprint(' - Project is missing', 'red')

    @staticmethod
    def format_project_ref_string(repo_path):
        """Return formatted repo ref name"""
        repo = ProjectRepo(repo_path, DEFAULT_REMOTE, DEFAULT_REF)
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
        if not ProjectRepo.existing_git_repository(repo_path):
            return colored(name, 'green')
        repo = ProjectRepo(repo_path, DEFAULT_REMOTE, DEFAULT_REF)
        if not repo.validate_repo():
            color = 'red'
            symbol = '*'
        else:
            color = 'green'
            symbol = ''
        return colored(name + symbol, color)

    def herd(self, url, depth=0, fetch=True, rebase=False):
        """Herd ref"""
        if not self.existing_git_repository(self.repo_path):
            self._herd_initial(url, depth=depth)
            return
        return_code = self._create_remote(self.remote, url)
        if return_code != 0:
            raise ClowderGitError(msg=colored(' - Failed to create remote', 'red'))
        self._herd(self.remote, self.default_ref, depth=depth, fetch=fetch, rebase=rebase)

    def herd_branch(self, url, branch, depth=0, rebase=False, fork_remote=None):
        """Herd branch"""
        if not self.existing_git_repository(self.repo_path):
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
        if not self.existing_git_repository(self.repo_path):
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

    def prune_branch_local(self, branch, force):
        """Prune branch in repository"""
        branch_output = fmt.ref_string(branch)
        if branch not in self.repo.heads:
            self._print(' - Local branch ' + branch_output + " doesn't exist")
            return
        prune_branch = self.repo.heads[branch]
        if self.repo.head.ref == prune_branch:
            ref_output = fmt.ref_string(self.truncate_ref(self.default_ref))
            try:
                self._print(' - Checkout ref ' + ref_output)
                self.repo.git.checkout(self.truncate_ref(self.default_ref))
            except GitError as err:
                message = colored(' - Failed to checkout ref', 'red') + ref_output
                self._print(message)
                self._print(fmt.error(err))
                self._exit(message)
            except (KeyboardInterrupt, SystemExit):
                self._exit('')
        try:
            self._print(' - Delete local branch ' + branch_output)
            self.repo.delete_head(branch, force=force)
            return
        except GitError as err:
            message = colored(' - Failed to delete local branch ', 'red') + branch_output
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            self._exit('')

    def prune_branch_remote(self, branch, remote):
        """Prune remote branch in repository"""
        branch_output = fmt.ref_string(branch)
        if not self.existing_remote_branch(branch, remote):
            self._print(' - Remote branch ' + branch_output + " doesn't exist")
            return
        try:
            self._print(' - Delete remote branch ' + branch_output)
            self.repo.git.push(remote, '--delete', branch)
        except GitError as err:
            message = colored(' - Failed to delete remote branch ', 'red') + branch_output
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            self._exit('')

    def reset(self, depth=0):
        """Reset branch to upstream or checkout tag/sha as detached HEAD"""
        if self.ref_type(self.default_ref) == 'branch':
            branch = self.truncate_ref(self.default_ref)
            branch_output = fmt.ref_string(branch)
            if not self.existing_local_branch(branch):
                return_code = self._create_branch_local_tracking(branch, self.remote, depth=depth, fetch=True)
                if return_code != 0:
                    message = colored(' - Failed to create tracking branch ', 'red') + branch_output
                    self._print(message)
                    self._exit(message)
                return
            elif self._is_branch_checked_out(branch):
                self._print(' - Branch ' + branch_output + ' already checked out')
            else:
                self._checkout_branch_local(branch)
            remote_output = fmt.remote_string(self.remote)
            if not self.existing_remote_branch(branch, self.remote):
                message = colored(' - No existing remote branch ', 'red') + remote_output + ' ' + branch_output
                self._print(message)
                self._exit(message)
            self.fetch(self.remote, ref=self.default_ref, depth=depth)
            self._print(' - Reset branch ' + branch_output + ' to ' + remote_output + ' ' + branch_output)
            remote_branch = self.remote + '/' + branch
            self._reset_head(branch=remote_branch)
        elif self.ref_type(self.default_ref) == 'tag':
            self.fetch(self.remote, ref=self.default_ref, depth=depth)
            self._checkout_tag(self.truncate_ref(self.default_ref))
        elif self.ref_type(self.default_ref) == 'sha':
            self.fetch(self.remote, ref=self.default_ref, depth=depth)
            self._checkout_sha(self.default_ref)

    def reset_timestamp(self, timestamp, author, ref):
        """Reset branch to upstream or checkout tag/sha as detached HEAD"""
        rev = None
        if author:
            rev = self._find_rev_by_timestamp_author(timestamp, author, ref)
        if rev is None:
            rev = self._find_rev_by_timestamp(timestamp, ref)
        if rev is None:
            message = colored(' - Failed to find rev', 'red')
            self._print(message)
            self._exit(message)
        self._checkout_sha(rev)

    def start(self, remote, branch, depth, tracking):
        """Start new branch in repository"""
        if branch not in self.repo.heads:
            if not is_offline():
                return_code = self.fetch(remote, ref=branch, depth=depth)
                if return_code != 0:
                    sys.exit(1)
            return_code = self._create_branch_local(branch)
            if return_code != 0:
                self._exit('', return_code=return_code)
            return_code = self._checkout_branch_local(branch)
            if return_code != 0:
                self._exit('', return_code=return_code)
        else:
            branch_output = fmt.ref_string(branch)
            print(' - ' + branch_output + ' already exists')
            correct_branch = self._is_branch_checked_out(branch)
            if correct_branch:
                print(' - On correct branch')
            else:
                return_code = self._checkout_branch_local(branch)
                if return_code != 0:
                    self._exit('', return_code=return_code)
        if tracking and not is_offline():
            self._create_branch_remote_tracking(branch, remote, depth)

    def sync(self, fork_remote, rebase=False):
        """Sync fork with upstream remote"""
        self._print(' - Sync fork with upstream remote')
        if self.ref_type(self.default_ref) != 'branch':
            message = colored(' - Can only sync branches', 'red')
            self._print(message)
            self._exit(message)
        fork_remote_output = fmt.remote_string(fork_remote)
        branch_output = fmt.ref_string(self.truncate_ref(self.default_ref))
        if rebase:
            self._rebase_remote_branch(self.remote, self.truncate_ref(self.default_ref))
        else:
            self._pull(self.remote, self.truncate_ref(self.default_ref))
        self._print(' - Push to ' + fork_remote_output + ' ' + branch_output)
        command = ['git', 'push', fork_remote, self.truncate_ref(self.default_ref)]
        return_code = execute_command(command, self.repo_path, print_output=self.print_output)
        if return_code != 0:
            message = colored(' - Failed to push to ', 'red') + fork_remote_output + ' ' + branch_output
            self._print(message)
            self._print(fmt.command_failed_error(command))
            self._exit(message)

    def _compare_remote_url(self, remote, url):
        """Compare actual remote url to given url"""
        if url != self._remote_get_url(remote):
            actual_url = self._remote_get_url(remote)
            message = fmt.remote_already_exists_error(remote, url, actual_url)
            self._print(message)
            self._exit(message)

    def _herd(self, remote, ref, depth=0, fetch=True, rebase=False):
        """Herd ref"""
        if self.ref_type(ref) == 'branch':
            branch = self.truncate_ref(ref)
            branch_output = fmt.ref_string(branch)
            if not self.existing_local_branch(branch):
                return_code = self._create_branch_local_tracking(branch, remote, depth=depth, fetch=fetch)
                if return_code != 0:
                    message = colored(' - Failed to create tracking branch ', 'red') + branch_output
                    self._print(message)
                    self._exit(message)
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
        elif self.ref_type(ref) == 'tag':
            self.fetch(remote, depth=depth, ref=ref)
            self._checkout_tag(self.truncate_ref(ref))
        elif self.ref_type(ref) == 'sha':
            self.fetch(remote, depth=depth, ref=ref)
            self._checkout_sha(ref)

    def _herd_initial(self, url, depth=0):
        """Herd ref initial"""
        self._init_repo()
        self._create_remote(self.remote, url, remove_dir=True)
        if self.ref_type(self.default_ref) == 'branch':
            self._checkout_new_repo_branch(self.truncate_ref(self.default_ref), depth)
        elif self.ref_type(self.default_ref) == 'tag':
            self._checkout_new_repo_tag(self.truncate_ref(self.default_ref), self.remote, depth, remove_dir=True)
        elif self.ref_type(self.default_ref) == 'sha':
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

    def _set_tracking_branch_commit(self, branch, remote, depth):
        """Set tracking relationship between local and remote branch if on same commit"""
        branch_output = fmt.ref_string(branch)
        origin = self._remote(remote)
        return_code = self.fetch(remote, depth=depth, ref=branch)
        if return_code != 0:
            raise ClowderGitError(msg=colored(' - Failed to fech', 'red'))
        if not self.existing_local_branch(branch):
            message = colored(' - No local branch ', 'red') + branch_output + '\n'
            self._print(message)
            self._exit(message)
        if not self.existing_remote_branch(branch, remote):
            message = colored(' - No remote branch ', 'red') + branch_output + '\n'
            self._print(message)
            self._exit(message)
        local_branch = self.repo.heads[branch]
        remote_branch = origin.refs[branch]
        if local_branch.commit != remote_branch.commit:
            message_1 = colored(' - Existing remote branch ', 'red')
            message_2 = colored(' on different commit', 'red')
            message = message_1 + branch_output + message_2 + '\n'
            self._print(message)
            self._exit(message_1)
        return_code = self._set_tracking_branch(remote, branch)
        if return_code != 0:
            self._exit(colored(' - Failed to set tracking branch', 'red'))
