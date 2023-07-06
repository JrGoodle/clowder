"""git remote

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pathlib import Path
from typing import List, Optional

from pygoodle.console import CONSOLE
from pygoodle.format import Format
# from pygoodle.git.decorators import error_msg
from pygoodle.git.log import GIT_LOG
from pygoodle.git.offline import GitOffline
from pygoodle.git.online import GitOnline

from .branch.remote_branch import RemoteBranch


class Remote:
    """Class encapsulating git ref

    :ivar Path path: Path to git repo
    :ivar str name: Branch
    :ivar str fetch_url: Fetch url
    :ivar str push_url: Push url
    """

    def __init__(self, path: Path, name: str):
        """GitRemote __init__

        :param Path path: Path to git repo
        :param str name: Branch
        """

        self.name: str = name
        self.path: Path = path

    def __eq__(self, other) -> bool:
        if isinstance(other, Remote):
            return self.path == other.path and self.name == other.name
        return False

    def __lt__(self, other: 'Remote') -> bool:
        return self.name < other.name

    @property
    def fetch_url(self) -> str:
        return GitOffline.get_remote_fetch_url(self.path, self.name)

    @property
    def push_url(self) -> str:
        return GitOffline.get_remote_push_url(self.path, self.name)

    def branches(self, url: Optional[str] = None, online: bool = False) -> List[RemoteBranch]:
        from pygoodle.git.model.factory import GitFactory
        if online or url is not None:
            return GitFactory.get_remote_branches_online(self.path, remote=self.name, url=url)
        return GitFactory.get_remote_branches_offline(self.path, self.name)

    # @error_msg('Failed to create remote')
    def create(self, url: str, fetch: bool = False, tags: bool = False) -> None:
        if self.exists:
            CONSOLE.stdout(f' - Remote {Format.Git.remote(self.name)} already exists')
            return
        CONSOLE.stdout(f' - Create remote {Format.Git.remote(self.name)}')
        GitOffline.create_remote(self.path, name=self.name, url=url, fetch=fetch, tags=tags)

    @property
    def exists(self) -> bool:
        from pygoodle.git.model.factory import GitFactory
        return GitFactory.has_remote(self.path, remote=self.name)

    def default_branch(self, url: str) -> Optional[RemoteBranch]:
        if GitOffline.is_repo_cloned(self.path):
            default_branch = GitOffline.get_default_branch(self.path, self.name)
            if default_branch is not None:
                return RemoteBranch(self.path, default_branch, self.name)
        default_branch = GitOnline.get_default_branch(url)
        if default_branch is None:
            return None
        git_dir = GitOffline.git_dir(self.path)
        if git_dir is not None and git_dir.is_dir():
            GitOffline.save_default_branch(git_dir, self.name, default_branch)
        return RemoteBranch(self.path, default_branch, self.name)

    # @error_msg('Failed to rename remote')
    def rename(self, name: str) -> None:
        CONSOLE.stdout(f' - Rename remote {Format.Git.remote(self.name)} to {Format.Git.remote(name)}')
        GitOffline.rename_remote(self.path, old_name=self.name, new_name=name)
        self.name = name

    def fetch(self, prune: bool = False, prune_tags: bool = False, tags: bool = False,
              depth: Optional[int] = None, branch: Optional[str] = None, unshallow: bool = False,
              jobs: Optional[int] = None, fetch_all: bool = False, check: bool = True,
              print_output: bool = True) -> None:
        output = self.name
        if branch is not None:
            branch = branch
            output = f'{output} {branch}'
        CONSOLE.stdout(f'Fetch from {output}')
        try:
            GitOnline.fetch(self.path, remote=self.name, prune=prune, prune_tags=prune_tags, tags=tags, depth=depth,
                            branch=branch, unshallow=unshallow, jobs=jobs, fetch_all=fetch_all, print_output=print_output)
        except Exception:  # noqa
            message = f'Failed to fetch from {output}'
            if check:
                GIT_LOG.error(message)
                raise
            CONSOLE.stdout(f' - {message}')

    def print_branches(self) -> None:
        raise NotImplementedError

    def _compare_remote_url(self, remote: str, url: str) -> None:
        """Compare actual remote url to given url

        If URL's are different print error message and exit

        :param str remote: Remote name
        :param str url: URL to compare with remote's URL
        :raise ClowderGitError:
        """

        # FIXME: Implement
        # if url != self._remote_get_url(remote):
        #     actual_url = self._remote_get_url(remote)
        #     message = f"Remote {fmt.remote(remote)} already exists with a different url\n" \
        #               f"{fmt.url_string(actual_url)} should be {fmt.url_string(url)}"
        #     raise ClowderGitError(message)
