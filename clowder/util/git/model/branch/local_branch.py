"""clowder ref enum

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from typing import Optional

from pygoodle.console import CONSOLE
from pygoodle.format import Format
# from pygoodle.git.decorators import error_msg
from pygoodle.git.model.commit import Commit
from pygoodle.git.offline import GitOffline
from pygoodle.git.online import GitOnline

from .branch import Branch


class LocalBranch(Branch):
    """Class encapsulating git branch

    :ivar Path path: Path to git repo
    :ivar str name: Branch name
    """

    def __lt__(self, other: 'LocalBranch') -> bool:
        return self.name < other.name

    @property
    def is_tracking_branch(self) -> bool:
        from pygoodle.git.model.factory import GitFactory
        branches = GitFactory.get_tracking_branches(self.path)
        return any([branch.name == self.name for branch in branches])

    @property
    def sha(self) -> Optional[str]:
        """Commit sha"""
        return GitOffline.get_branch_sha(self.path, self.name)

    # @error_msg('Failed to create local branch')
    def create(self, branch: Optional[str] = None, remote: Optional[str] = None, track: bool = True) -> None:
        if self.exists:
            CONSOLE.stdout(f' - Local branch {Format.Git.ref(self.short_ref)} already exists')
            return
        CONSOLE.stdout(f' - Create local branch {Format.Git.ref(self.short_ref)}')
        if branch is not None:
            if remote is not None:
                from pygoodle.git.model.branch.remote_branch import RemoteBranch
                remote_branch = RemoteBranch(self.path, branch, remote)
                if not remote_branch.exists:
                    branch = None
                    remote = None
            else:
                local_branch = LocalBranch(self.path, branch)
                if not local_branch.exists:
                    branch = None
        GitOffline.create_local_branch(self.path, self.name, branch=branch, remote=remote, track=track)

    # @error_msg('Failed to delete local branch')
    def delete(self, force: bool = False) -> None:
        if not self.exists:
            CONSOLE.stdout(f" - Local branch {Format.Git.ref(self.short_ref)} doesn't exist")
            return
        CONSOLE.stdout(f' - Delete local branch {Format.Git.ref(self.short_ref)}')
        GitOffline.delete_local_branch(self.path, self.name, force=force)

    @property
    def exists(self) -> bool:
        from pygoodle.git.model.factory import GitFactory
        return GitFactory.has_local_branch(self.path, self.name)

    @property
    def commit(self) -> Commit:
        sha = GitOffline.get_branch_sha(self.path, branch=self.name)
        return Commit(self.path, sha)

    # @error_msg('Failed to push local changes')
    # @not_detached
    def push(self, remote: Optional[str] = None, branch: Optional[str] = None,
             force: bool = False, set_upstream: bool = False) -> None:
        # TODO: Check if detached
        CONSOLE.stdout(' - Push local changes')
        GitOnline.push(self.path,
                       local_branch=self.name,
                       remote_branch=branch,
                       remote=remote,
                       force=force,
                       set_upstream=set_upstream)
