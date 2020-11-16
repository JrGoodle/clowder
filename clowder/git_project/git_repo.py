"""Base Git utility class

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pathlib import Path
from typing import Optional

from git import Repo, GitCommandError, GitError

import clowder.util.formatting as fmt
from clowder.console import CONSOLE
from clowder.error import ClowderError
from clowder.logging import LOG
from clowder.util.execute import execute_command
from clowder.util.file_system import remove_directory

from .util import (
    existing_git_repository,
    not_detached,
    truncate_ref,
)


class GitRepo(object):
    """Class encapsulating base git utilities

    :ivar str repo_path: Absolute path to repo
    :ivar str default_ref: Default ref
    :ivar str remote: Default remote name
    :ivar Repo Optional[repo]: Repo instance
    """

    def __init__(self, repo_path: Path, remote: str, default_ref: str):
        """GitRepo __init__

        :param Path repo_path: Absolute path to repo
        :param str remote: Default remote name
        :param str default_ref: Default ref
        """

        self.repo_path = repo_path
        self.default_ref = default_ref
        self.remote = remote
        self.repo = self._create_repo() if existing_git_repository(repo_path) else None

    def add(self, files: str) -> None:
        """Add files to git index

        :param str files: Files to git add
        :raise:
        """

        CONSOLE.stdout(' - Add files to git index')
        try:
            CONSOLE.stdout(self.repo.git.add(files))
        except GitError:
            CONSOLE.stderr("Failed to add files to git index")
            raise
        else:
            self.status_verbose()

    def checkout(self, truncated_ref: str, allow_failure: bool = False) -> None:
        """Checkout git ref

        :param str truncated_ref: Ref to git checkout
        :param bool allow_failure: Whether to allow failing to checkout branch
        :raise GitError:
        """

        ref_output = fmt.ref(truncated_ref)
        try:
            CONSOLE.stdout(f' - Check out {ref_output}')
            CONSOLE.stdout(self.repo.git.checkout(truncated_ref))
        except GitError:
            message = f'Failed to checkout {ref_output}'
            if allow_failure:
                CONSOLE.stdout(f' - {message}')
                return
            CONSOLE.stderr(message)
            raise

    def clean(self, args: str = '') -> None:
        """Discard changes for repo

        :param str args: Git clean options
            - ``d`` Remove untracked directories in addition to untracked files
            - ``f`` Delete directories with .git sub directory or file
            - ``X`` Remove only files ignored by git
            - ``x`` Remove all untracked files
        """

        CONSOLE.stdout(' - Clean project')
        clean_args = '-f' if args == '' else '-f' + args
        self._clean(args=clean_args)
        CONSOLE.stdout(' - Reset project')
        self._reset_head()
        if self._is_rebase_in_progress:
            CONSOLE.stdout(' - Abort rebase in progress')
            self._abort_rebase()

    def commit(self, message: str) -> None:
        """Commit current changes

        :param str message: Git commit message
        :raise ClowderError:
        """

        try:
            CONSOLE.stdout(' - Commit current changes')
            CONSOLE.stdout(self.repo.git.commit(message=message))
        except GitError:
            CONSOLE.stderr('Failed to commit current changes')
            raise

    @property
    def current_branch(self) -> str:
        """Return currently checked out branch of project

        :return: Name of currently checked out branch
        :rtype: str
        """

        return self.repo.head.ref.name

    def has_remote_branch(self, branch: str, remote: str) -> bool:
        """Check if remote branch exists

        :param str branch: Branch name
        :param str remote: Remote name
        :return: True, if remote branch exists
        :rtype: bool
        :raise ClowderError:
        """

        try:
            origin = self.repo.remotes[remote]
            return branch in origin.refs
        except (GitError, IndexError):
            return False

    def has_local_branch(self, branch: str) -> bool:
        """Check if local branch exists

        :param str branch: Branch name
        :return: True, if local branch exists
        :rtype: bool
        """

        return branch in self.repo.heads

    def fetch(self, remote: str, ref: Optional[str] = None, depth: int = 0,
              remove_dir: bool = False, allow_failure: bool = False) -> None:
        """Fetch from a specific remote ref

        :param str remote: Remote name
        :param Optional[str] ref: Ref to fetch
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool remove_dir: Whether to remove the directory if commands fail
        :param bool allow_failure: Whether to allow failure
        :raise ClowderError:
        """

        remote_output = fmt.remote(remote)
        if depth == 0 or ref is None:
            CONSOLE.stdout(f' - Fetch from {remote_output}')
            error_message = f'Failed to fetch from remote {remote_output}'
        else:
            ref_output = fmt.ref(truncate_ref(ref))
            CONSOLE.stdout(f' - Fetch from {remote_output} {ref_output}')
            error_message = f'Failed to fetch from {remote_output} {ref_output}'

        try:
            if depth == 0:
                execute_command(f'git fetch {remote} --prune --tags', self.repo_path)
            elif ref is None:
                command = f'git fetch {remote} --depth {depth} --prune --tags'
                execute_command(command, self.repo_path)
            else:
                command = f'git fetch {remote} {truncate_ref(ref)} --depth {depth} --prune --tags'
                execute_command(command, self.repo_path)
        except ClowderError as err:
            LOG.debug('Failed to fetch', err)
            if remove_dir:
                # TODO: Handle possible exceptions
                remove_directory(self.repo_path)
            if not allow_failure:
                CONSOLE.stderr(error_message)
                raise

    @property
    def formatted_ref(self) -> str:
        """Return formatted project ref string

        :return: Formmatted repo ref
        :rtype: str
        """

        local_commits = self.new_commits()
        upstream_commits = self.new_commits(upstream=True)
        no_local_commits = local_commits == 0 or local_commits == '0'
        no_upstream_commits = upstream_commits == 0 or upstream_commits == '0'
        if no_local_commits and no_upstream_commits:
            status = ''
        else:
            local_commits_output = fmt.yellow(f'+{local_commits}')
            upstream_commits_output = fmt.red(f'-{upstream_commits}')
            status = f'({local_commits_output}/{upstream_commits_output})'

        if self.is_detached:
            current_ref = self.sha()
            return fmt.magenta(fmt.escape(f'[HEAD @ {current_ref}]'))
        current_branch = self.current_branch
        return fmt.magenta(fmt.escape(f'[{current_branch}]')) + status

    def format_project_string(self, path: Path) -> str:
        """Return formatted project name

        :param Path path: Relative project path
        :return: Formatted project name
        :rtype: str
        """

        if not existing_git_repository(self.repo_path):
            return str(path)

        if not self.validate_repo():
            return f'{path}*'
        else:
            return str(path)

    @staticmethod
    def color_project_string(project: str) -> str:
        """Return formatted colored project name

        :param str project: Relative project path
        :return: Formatted project name
        :rtype: str
        """

        if '*' in project:
            return fmt.red(project)

        return fmt.green(project)

    @property
    def current_timestamp(self) -> str:
        """Get current timestamp of HEAD commit

        :return: HEAD commit timestamp
        :rtype: str
        :raise ClowderError:
        """

        try:
            return self.repo.git.log('-1', '--format=%cI')
        except GitError:
            CONSOLE.stderr('Failed to find current timestamp')
            raise

    def git_config_unset_all_local(self, variable: str) -> None:
        """Unset all local git config values for given variable key

        :param str variable: Fully qualified git config variable
        :raise ClowderError:
        """

        try:
            self.repo.git.config('--local', '--unset-all', variable)
        except GitCommandError as err:
            if err.status != 5:  # git returns error code 5 when trying to unset variable that doesn't exist
                CONSOLE.stderr(f'Failed to unset all local git config values for {variable}')
                raise
        except GitError:
            CONSOLE.stderr(f'Failed to unset all local git config values for {variable}')
            raise

    def git_config_add_local(self, variable: str, value: str) -> None:
        """Add local git config value for given variable key

        :param str variable: Fully qualified git config variable
        :param str value: Git config value
        :raise ClowderError:
        """

        try:
            self.repo.git.config('--local', '--add', variable, value)
        except GitError:
            CONSOLE.stderr(f'Failed to add local git config value {value} for variable {variable}')
            raise

    def install_lfs_hooks(self) -> None:
        """Install git lfs hooks

        :raise ClowderError:
        """

        CONSOLE.stdout(" - Update git lfs hooks")
        try:
            self.repo.git.lfs('install', '--local')
        except GitError:
            CONSOLE.stderr('Failed to update git lfs hooks')
            raise

    @property
    def is_detached(self) -> bool:
        """Check if HEAD is detached

        :return: True, if HEAD is detached
        :rtype: bool
        """

        if not self.repo_path.is_dir():
            return False
        if self.repo.head.is_detached:
            return True
        return False

    @property
    def is_dirty(self) -> bool:
        """Check whether repo is dirty

        :return: True, if repo is dirty
        :rtype: bool
        """

        if not self.repo_path.is_dir():
            return False

        return self.repo.is_dirty() or self._is_rebase_in_progress or self._has_untracked_files

    def is_lfs_installed(self) -> bool:
        """Check whether git lfs hooks are installed

        :return: True, if lfs hooks are installed
        :rtype: bool
        """

        try:
            self.repo.git.config('--get', 'filter.lfs.smudge')
            self.repo.git.config('--get', 'filter.lfs.clean')
            self.repo.git.config('--get', 'filter.lfs.process')
            self.repo.git.config('--get', 'filter.lfs.required')
        except GitError:
            return False
        else:
            return True

    def new_commits(self, upstream: bool = False) -> int:
        """Returns the number of new commits

        :param bool upstream: Whether to find number of new upstream or local commits
        :return: Int number of new commits
        :rtype: int
        """

        try:
            local_branch = self.repo.active_branch
        except (GitError, TypeError):
            return 0
        else:
            tracking_branch = local_branch.tracking_branch()
            if local_branch is None or tracking_branch is None:
                return 0

            try:
                commits = f'{local_branch.commit.hexsha}...{tracking_branch.commit.hexsha}'
                rev_list_count = self.repo.git.rev_list('--count', '--left-right', commits)
            except (GitError, ValueError):
                return 0
            else:
                index = 1 if upstream else 0
                return int(str(rev_list_count).split()[index])

    def print_local_branches(self) -> None:
        """Print local git branches"""

        for branch in self.repo.git.branch().split('\n'):
            if branch.startswith('* '):
                branch_name = fmt.green(branch[2:])
                CONSOLE.stdout(f"* {branch_name}")
            else:
                CONSOLE.stdout(branch)

    def print_remote_branches(self) -> None:
        """Print output if self._print_output is True"""

        for branch in self.repo.git.branch('-r', '-l', f"{self.remote}*").split('\n'):
            if ' -> ' in branch:
                components = branch.split(' -> ')
                local_branch = components[0]
                remote_branch = components[1]
                CONSOLE.stdout(f"  {fmt.red(local_branch)} -> {remote_branch}")
            else:
                CONSOLE.stdout(fmt.red(branch))

    def print_validation(self) -> None:
        """Print validation messages"""

        if not existing_git_repository(self.repo_path):
            return

        if not self.validate_repo():
            CONSOLE.stdout(f'Dirty repo. Please stash, commit, or discard your changes')
            self.status_verbose()

    @not_detached
    def pull(self) -> None:
        """Pull upstream changes

        :raise ClowderError:
        """

        try:
            CONSOLE.stdout(' - Pull latest changes')
            CONSOLE.stdout(self.repo.git.pull())
        except GitError:
            CONSOLE.stderr('Failed to pull latest changes')
            raise

    def pull_lfs(self) -> None:
        """Pull lfs files

        :raise ClowderError:
        """

        try:
            CONSOLE.stdout(' - Pull git lfs files')
            self.repo.git.lfs('pull')
        except GitError:
            CONSOLE.stderr('Failed to pull git lfs files')
            raise

    @not_detached
    def push(self) -> None:
        """Push changes

        :raise ClowderError:
        """

        try:
            CONSOLE.stdout(' - Push local changes')
            CONSOLE.stdout(self.repo.git.push())
        except GitError:
            CONSOLE.stderr('Failed to push local changes')
            raise

    def sha(self, short: bool = False) -> str:
        """Return sha for currently checked out commit

        :param bool short: Whether to return short or long commit sha
        :return: Commit sha
        :rtype: str
        """

        if short:
            return self.repo.git.rev_parse(self.repo.head.commit.hexsha, short=True)

        return self.repo.head.commit.hexsha

    def stash(self) -> None:
        """Stash current changes in repository"""

        if not self.repo.is_dirty:
            CONSOLE.stdout(' - No changes to stash')
            return

        CONSOLE.stdout(' - Stash current changes')
        self.repo.git.stash()

    def status(self) -> None:
        """Print  git status

        Equivalent to: ``git status``
        """

        CONSOLE.stdout(self.repo.git.status())

    def status_verbose(self) -> None:
        """Print git status

        Equivalent to: ``git status -vv``

        :raise ClowderError:
        """

        command = 'git status -vv'
        CONSOLE.stdout(fmt.command(command))
        try:
            execute_command(command, self.repo_path)
        except ClowderError:
            CONSOLE.stderr('Failed to print verbose status')
            raise

    def validate_repo(self, allow_missing_repo: bool = True) -> bool:
        """Validate repo state

        :param bool allow_missing_repo: Whether to allow validation to succeed with missing repo
        :return: True, if repo not dirty or doesn't exist on disk
        :rtype: bool
        """

        if not existing_git_repository(self.repo_path):
            return allow_missing_repo

        return not self.is_dirty

    def _abort_rebase(self) -> None:
        """Abort rebase

        :raise ClowderError:
        """

        if not self._is_rebase_in_progress:
            return

        try:
            self.repo.git.rebase('--abort')
        except GitError:
            CONSOLE.stderr('Failed to abort rebase')
            raise

    def _clean(self, args: str) -> None:
        """Clean git directory

        :param str args: Git clean args
        :raise ClowderError:
        """

        try:
            self.repo.git.clean(args)
        except GitError:
            CONSOLE.stderr('Failed to clean git repo')
            raise

    # def _existing_remote_tag(self, tag, remote, depth=0):
    #     """Check if remote tag exists
    #
    #     :param str tag: Tag name
    #     :param str remote: Remote name
    #     :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
    #         Defaults to 0
    #     :return: True, if remote tag exists
    #     :rtype: bool
    #     """
    #
    #     origin = self._remote(remote, remove_dir=True)
    #     self.fetch(remote, depth=depth, ref=tag, remove_dir=True)
    #     return tag in origin.tags

    @property
    def _is_rebase_in_progress(self) -> bool:
        """Detect whether rebase is in progress

        :return: True, if rebase is in progress
        :rtype: bool
        """

        is_rebase_apply = Path(self.repo_path / '.git' / 'rebase-apply').is_dir()
        is_rebase_merge = Path(self.repo_path / '.git' / 'rebase-merge').is_dir()
        return is_rebase_apply or is_rebase_merge

    def _create_repo(self) -> Repo:
        """Create Repo instance for self.repo_path

        :return: GitPython Repo instance
        :rtype: Repo
        :raise ClowderError:
        """

        try:
            repo = Repo(self.repo_path)
        except GitError:
            repo_path_output = fmt.path(self.repo_path)
            CONSOLE.stderr(f"Failed to create Repo instance for {repo_path_output}")
            raise
        else:
            return repo

    def _reset_head(self, branch: Optional[str] = None) -> None:
        """Reset head of repo, discarding changes

        :param Optional[str] branch: Branch to reset head to
        :raise ClowderError:
        """

        if branch is None:
            try:
                self.repo.head.reset(index=True, working_tree=True)
            except GitError:
                CONSOLE.stderr(f"Failed to reset {fmt.ref('HEAD')}")
                raise
            else:
                return

        try:
            self.repo.git.reset('--hard', branch)
        except GitError:
            CONSOLE.stderr(f'Failed to reset to {fmt.ref(branch)}')
            raise

    @property
    def _has_untracked_files(self) -> bool:
        """Check whether untracked files exist

        :return: True, if untracked files exist
        :rtype: bool
        """

        return True if self.repo.untracked_files else False
