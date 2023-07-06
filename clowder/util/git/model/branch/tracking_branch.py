"""clowder ref enum

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pathlib import Path
from typing import Optional

from pygoodle.console import CONSOLE
from pygoodle.git.constants import ORIGIN
# from pygoodle.git.decorators import not_detached
from pygoodle.git.offline import GitOffline
from pygoodle.git.online import GitOnline
from pygoodle.format import Format
# from pygoodle.git.decorators import error_msg

from .branch import Branch


class TrackingBranch(Branch):
    """Class encapsulating git branch

    :ivar Path path: Path to git repo
    :ivar str name: Local branch name
    :ivar RemoteBranch upstream_branch: Upstream branch name
    :ivar Optional[RemoteBranch] push_branch: Push branch name
    :ivar str formatted_ref: Formatted ref
    """

    def __init__(self, path: Path, local_branch: str,
                 upstream_branch: Optional[str] = None, upstream_remote: Optional[str] = None,
                 push_branch: Optional[str] = None, push_remote: Optional[str] = None):
        super().__init__(path, local_branch)
        from .local_branch import LocalBranch
        from .remote_branch import RemoteBranch
        upstream_branch = local_branch if upstream_branch is None else upstream_branch
        upstream_remote = ORIGIN if upstream_remote is None else upstream_remote
        push_branch = upstream_branch if push_branch is None else push_branch
        push_remote = upstream_remote if push_remote is None else push_remote
        self.local_branch: LocalBranch = LocalBranch(self.path, self.name)
        self.upstream_branch: RemoteBranch = RemoteBranch(self.path, upstream_branch, upstream_remote)
        self.push_branch: RemoteBranch = RemoteBranch(self.path, push_branch, push_remote)

    def __eq__(self, other) -> bool:
        if isinstance(other, TrackingBranch):
            return super().__eq__(other) and self.upstream_branch == other.upstream_branch
        return False

    def __lt__(self, other: 'TrackingBranch') -> bool:
        return f'{self.name}/{self.upstream_branch.remote.name}/{self.upstream_branch.name}' \
               < f'{other.name}/{other.upstream_branch.remote.name}/{other.upstream_branch.name}'

    @property
    def sha(self) -> Optional[str]:
        """Commit sha"""
        raise self.local_branch.sha

    def delete(self, force: bool = False) -> None:
        self.local_branch.delete(force=force)
        self.upstream_branch.delete()

    @property
    def is_branch(self) -> bool:
        return True

    @property
    def exists(self) -> bool:
        from pygoodle.git.model.factory import GitFactory
        return GitFactory.has_tracking_branch(self.path, self.name)

    # @error_msg('Failed to set tracking branch')
    def set_upstream(self) -> None:
        CONSOLE.stdout(f' - Set tracking branch {Format.Git.ref(self.name)} -> '
                       f'{Format.Git.remote(self.upstream_branch.remote.name)} '
                       f'{Format.Git.ref(self.upstream_branch.name)}')
        GitOffline.set_upstream_branch(self.path,
                                       local_branch=self.name,
                                       upstream_branch=self.upstream_branch.name,
                                       remote=self.upstream_branch.remote.name)

    # @error_msg('Failed to create tracking branch')
    def create(self) -> None:
        if GitOffline.has_tracking_branch(self.path, self.local_branch.name):
            CONSOLE.stdout(' - Tracking branch already exists')
            return
        # TODO: Add Format util to format tracking branch output: local_branch -> remote remote_branch
        CONSOLE.stdout(f' - Create tracking branch {Format.Git.ref(self.name)}')
        GitOnline.fetch(self.path, prune=True)
        # local and remote branches exist
        if self.local_branch.exists and self.upstream_branch.exists:
            self.set_upstream()
            return

        # only local branch exists
        if self.local_branch.exists:
            # GitOnline.push(self.path,
            #                local_branch=self.name,
            #                remote_branch=self.upstream_branch.name,
            #                remote=self.upstream_branch.remote.name,
            #                set_upstream=True)
            self.upstream_branch.create(branch=self.local_branch.name)
            self.set_upstream()
            GitOnline.fetch(self.path, prune=True)
            return

        # only remote branch exists
        if self.upstream_branch.exists:
            self.local_branch.create(branch=self.upstream_branch.name, remote=self.upstream_branch.remote.name)
            # GitOffline.create_local_branch(self.path, self.name,
            #                                branch=self.upstream_branch.name,
            #                                remote=self.upstream_branch.remote)
            return

        # local and remote branches DO NOT exist
        self.upstream_branch.create()
        GitOnline.fetch(self.path, prune=True)
        self.local_branch.create(branch=self.upstream_branch.name, remote=self.upstream_branch.remote.name)

    # @error_msg('Failed to pull')
    # @not_detached
    def pull(self, rebase: bool = False, prune: bool = False, tags: bool = False,
             jobs: Optional[int] = None, no_edit: bool = False, autostash: bool = False,
             depth: Optional[int] = None) -> None:
        # TODO: Check if detached
        self.upstream_branch.pull(rebase=rebase, prune=prune, tags=tags, jobs=jobs,
                                  no_edit=no_edit, autostash=autostash, depth=depth)

    def _set_tracking_branch_commit(self, branch: str, remote: str, depth: int) -> None:
        """Set tracking relationship between local and remote branch if on same commit

        :param str branch: Branch name
        :param str remote: Remote name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :raise ClowderGitError:
        """

        # FIXME: Try to set this in any scenario where it makes sense
        # origin = self._remote(remote)
        # self.fetch(remote, depth=depth, ref=GitRef(branch=branch))
        #
        # if not self.has_local_branch(branch):
        #     raise ClowderGitError(f'No local branch {fmt.ref(branch)}')
        #
        # if not self.has_remote_branch(branch, remote):
        #     raise ClowderGitError(f'No remote branch {fmt.ref(branch)}')
        #
        # local_branch = self.repo.heads[branch]
        # remote_branch = origin.refs[branch]
        # if local_branch.commit != remote_branch.commit:
        #     raise ClowderGitError(f' - Existing remote branch {fmt.ref(branch)} on different commit')
        #
        # self._set_tracking_branch(remote, branch)
