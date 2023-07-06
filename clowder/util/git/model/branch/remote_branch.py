"""clowder ref enum

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pathlib import Path
from typing import Optional

from pygoodle.console import CONSOLE
from pygoodle.git.constants import ORIGIN
# from pygoodle.git.decorators import not_detached
from pygoodle.format import Format
# from pygoodle.git.decorators import error_msg
from pygoodle.git.model.commit import Commit
from pygoodle.git.offline import GitOffline
from pygoodle.git.online import GitOnline

from .branch import Branch


class RemoteBranch(Branch):
    """Class encapsulating git branch

    :ivar Path path: Path to git repo
    :ivar str name: Branch name
    :ivar str formatted_ref: Formatted ref
    """

    def __init__(self, path: Path, name: str, remote: Optional[str] = None, is_default: bool = False):
        """Branch __init__

        :param str name: Branch name
        :param Remote remote: Remote
        :param bool is_default: Is branch default for remote repo
        """

        from pygoodle.git.model.remote import Remote
        super().__init__(path, name)
        remote = ORIGIN if remote is None else remote
        self.remote: Remote = Remote(self.path, remote)
        self.is_default: bool = is_default

    def __eq__(self, other) -> bool:
        if isinstance(other, RemoteBranch):
            return super().__eq__(other) and self.remote.name == other.remote.name
        return False

    def __lt__(self, other: 'RemoteBranch') -> bool:
        return f'{self.remote.name}/{self.name}' < f'{other.remote.name}/{other.name}'

    @property
    def short_ref(self) -> str:
        """Short git ref"""

        return f'{self.remote.name}/{self.truncate_ref(self.name)}'

    # TODO: Fix this
    # @property
    # def formatted_ref(self) -> str:
    #     """Formatted git ref"""
    #
    #     return f'refs/remotes/{self.remote.name}/heads/{self.name}'

    @property
    def is_tracking_branch(self) -> bool:
        from pygoodle.git.model.factory import GitFactory
        return GitFactory.has_tracking_branch(self.path, self.name)

    @property
    def sha(self) -> Optional[str]:
        """Commit sha"""
        return GitOffline.get_branch_sha(self.path, self.name, self.remote.name)

    # @error_msg('Failed to delete remote branch')
    def delete(self) -> None:
        from pygoodle.git.model.factory import GitFactory
        if not GitFactory.has_remote_branch_online(self.path, self.name, self.remote.name):
            CONSOLE.stdout(f" - Remote branch {Format.Git.ref(self.name)} doesn't exist")
            return
        CONSOLE.stdout(f' - Delete remote branch {Format.Git.ref(self.name)}')
        GitOnline.delete_remote_branch(self.path, branch=self.name, remote=self.remote.name, force=True)

    @property
    def exists(self) -> bool:
        from pygoodle.git.model.factory import GitFactory
        return GitFactory.has_remote_branch_offline(self.path, self.name, self.remote.name)

    def exists_online(self, url: Optional[str] = None) -> bool:
        from pygoodle.git.model.factory import GitFactory
        return GitFactory.has_remote_branch_online(self.path, branch=self.name, remote=self.remote.name, url=url)

    # @error_msg('Failed to create remote branch')
    def create(self, branch: Optional[str] = None, remote: Optional[str] = None) -> None:
        from pygoodle.git.model.factory import GitFactory
        if GitFactory.has_remote_branch_online(self.path, self.name, self.remote.name):
            CONSOLE.stdout(f' - Remote branch {Format.Git.ref(self.name)} already exists')
            return
        CONSOLE.stdout(f' - Create remote branch {Format.Git.ref(self.name)}')
        branch = self.name if branch is None else branch
        from pygoodle.git.model.branch.local_branch import LocalBranch
        local_branch = LocalBranch(self.path, branch)
        GitOnline.fetch(self.path, prune=True)
        has_existing_branch = local_branch.exists
        if not has_existing_branch:
            local_branch.create(branch=branch, remote=remote)
        local_branch.push(remote=self.remote.name, branch=self.name)
        if not has_existing_branch:
            GitOffline.delete_local_branch(self.path, branch)
        GitOnline.fetch(self.path, prune=True)

    @property
    def commit(self) -> Commit:
        sha = GitOffline.get_branch_sha(self.path, branch=self.name, remote=self.name)
        return Commit(self.path, sha)

    # @error_msg('Failed to pull')
    # @not_detached
    def pull(self, rebase: bool = False, prune: bool = False, tags: bool = False,
             jobs: Optional[int] = None, no_edit: bool = False, autostash: bool = False,
             depth: Optional[int] = None) -> None:
        # TODO: Check if detached
        message = f' - Pull'
        if rebase:
            message += ' with rebase'
        message += f' from {Format.Git.remote(self.remote.name)} {Format.Git.ref(self.name)}'
        CONSOLE.stdout(message)
        GitOnline.pull(self.path, remote=self.remote.name, branch=self.name, rebase=rebase, prune=prune,
                       tags=tags, jobs=jobs, no_edit=no_edit, autostash=autostash, depth=depth)
