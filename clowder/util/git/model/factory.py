"""git model factory

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pathlib import Path
from typing import List, Optional, Tuple

from pygoodle.git.offline import GitOffline
from pygoodle.git.online import GitOnline

from .change import Change
from .diff import Diff
from .branch.local_branch import LocalBranch
from .branch.remote_branch import RemoteBranch
from .branch.tracking_branch import TrackingBranch
from .remote import Remote
from .submodule import Submodule
from .tag.local_tag import LocalTag
from .tag.remote_tag import RemoteTag


class AllBranches:

    def __init__(self, local_branches: List[LocalBranch], remote_branches: List[RemoteBranch],
                 tracking_branches: List[TrackingBranch]):

        local_branches = [b for b in local_branches if not b.is_tracking_branch]
        remote_branches = [b for b in remote_branches if not b.is_tracking_branch]
        self.local_branches: Tuple[LocalBranch, ...] = tuple(local_branches)
        self.remote_branches: Tuple[RemoteBranch, ...] = tuple(remote_branches)
        self.tracking_branches: Tuple[TrackingBranch, ...] = tuple(tracking_branches)


class GitFactory:

    @classmethod
    def get_diff(cls, path: Path) -> Diff:
        diff_info = GitOffline.get_diff_index_info(path)
        changes = []
        for change_type, changes_list in diff_info.items():
            for change_info in changes_list:
                change = Change(path,
                                file_path=Path(change_info['file_path']),
                                change_type=change_type,
                                old_permissions=change_info['old_permissions'],
                                new_permissions=change_info['new_permissions'],
                                old_sha=change_info['old_sha'],
                                new_sha=change_info['new_sha'])
                changes.append(change)
        return Diff(path, changes=changes)

    @classmethod
    def get_remotes(cls, path: Path) -> List[Remote]:
        remotes = GitOffline.get_remotes_info(path)
        remotes = [Remote(path, name) for name in remotes.keys()]
        return sorted(remotes)

    @classmethod
    def has_remote(cls, path: Path, remote: Optional[str] = None, fetch_url: Optional[str] = None,
                   push_url: Optional[str] = None) -> bool:
        remote = GitFactory.get_remote(path, remote=remote, fetch_url=fetch_url, push_url=push_url)
        return remote is not None

    @classmethod
    def get_remote(cls, path: Path, remote: Optional[str] = None, fetch_url: Optional[str] = None,
                   push_url: Optional[str] = None) -> Optional[Remote]:
        remotes = GitFactory.get_remotes(path)
        if remote is not None:
            remotes = [r for r in remotes if r.name == remote]
        if fetch_url is not None:
            remotes = [r for r in remotes if r.fetch_url == fetch_url]
        if push_url is not None:
            remotes = [r for r in remotes if r.push_url == push_url]
        return remotes[0] if remotes else None

    @classmethod
    def get_local_branches(cls, path: Path) -> List[LocalBranch]:
        branches = GitOffline.get_local_branches_info(path)
        branches = [LocalBranch(path, branch) for branch in branches]
        return sorted(branches)

    @classmethod
    def get_local_tags(cls, path: Path) -> List[LocalTag]:
        tags = GitOffline.get_local_tags_info(path)
        tags = [LocalTag(path, tag) for tag in tags]
        return sorted(tags)

    @classmethod
    def get_submodule(cls, path: Path, submodule_path: Path) -> Optional[Remote]:
        submodules = GitFactory.get_submodules(path)
        full_path = path / submodule_path
        submodule = [s for s in submodules if s.path == full_path]
        return submodule[0] if submodule else None

    @classmethod
    def get_submodules(cls, path: Path) -> List[Submodule]:
        submodules_info = GitOffline.get_submodules_info(path)
        submodules = []
        for key in submodules_info.keys():
            submodule_info = submodules_info[key]
            # TODO: Save url from config and gitmodules
            url = submodule_info['url']
            submodule_path = Path(key)
            branch = submodule_info['branch'] if 'branch' in submodule_info else None
            active = submodule_info['active'] if 'active' in submodule_info else None
            active = True if active == 'true' else False
            submodule_commit = GitOffline.get_submodule_commit(path, submodule_path)
            submodule = Submodule(path, submodule_path, url=url, commit=submodule_commit, branch=branch, active=active)
            submodules.append(submodule)
            recursive_submodules = GitFactory.get_submodules(submodule.path)
            if recursive_submodules:
                submodules += recursive_submodules
        return sorted(submodules)

    @classmethod
    def has_submodule(cls, path: Path, submodule_path: Path) -> bool:
        submodule = GitFactory.get_submodule(path, submodule_path)
        return submodule is not None

    @classmethod
    def get_tracking_branches(cls, path: Path) -> List[TrackingBranch]:
        branches = GitOffline.get_tracking_branches_info(path)
        tracking_branches = []
        for local_branch, info in branches.items():
            tracking_branch = TrackingBranch(path,
                                             local_branch=local_branch,
                                             upstream_branch=info['upstream_branch'],
                                             upstream_remote=info['upstream_remote'],
                                             push_branch=info['push_branch'],
                                             push_remote=info['push_remote'])
            tracking_branches.append(tracking_branch)
        return sorted(tracking_branches)

    @classmethod
    def get_all_branches(cls, path: Path, online: bool = False) -> AllBranches:
        local_branches = GitFactory.get_local_branches(path)
        remote_branches = GitFactory.get_all_remote_branches(path, online=online)
        tracking_branches = GitFactory.get_tracking_branches(path)
        return AllBranches(
            local_branches=local_branches,
            remote_branches=remote_branches,
            tracking_branches=tracking_branches
        )

    @classmethod
    def get_all_remote_branches(cls, path: Path, online: bool = False) -> List[RemoteBranch]:
        branches = []
        for remote in GitFactory.get_remotes(path):
            branches += remote.branches(online=online)
        return sorted(branches)

    @classmethod
    def get_remote_branches_offline(cls, path: Path, remote: str) -> List[RemoteBranch]:
        branches, default_branch = GitOffline.get_remote_branches_info(path, remote)
        branches = [RemoteBranch(path, branch, remote) for branch in branches]
        if default_branch is not None:
            branches.append(RemoteBranch(path, default_branch, remote, is_default=True))
        return sorted(branches)

    @classmethod
    def get_remote_branches_online(cls, path: Path, remote: str,
                                   url: Optional[str] = None) -> List[RemoteBranch]:
        if url is None:
            branches = GitOnline.get_remote_branches_info(path, remote=remote)
        else:
            branches = GitOnline.get_remote_branches_info(remote=url)
        branches = [RemoteBranch(path, branch, remote) for branch in branches]
        return sorted(branches)

    @classmethod
    def get_remote_tags(cls, path: Path, remote: str, url: Optional[str] = None) -> List[RemoteTag]:
        if url is None:
            tags = GitOnline.get_remote_tags_info(path, remote=remote)
        else:
            tags = GitOnline.get_remote_tags_info(remote=url)
        tags = [RemoteTag(path, tag, remote) for tag in tags]
        return sorted(tags)

    @classmethod
    def get_local_branch(cls, path: Path, branch: str) -> Optional[LocalBranch]:
        branches = GitFactory.get_local_branches(path)
        branch = [b for b in branches if b.name == branch]
        return branch[0] if branch else None

    @classmethod
    def has_local_branch(cls, path: Path, branch: str) -> bool:
        branch = GitFactory.get_local_branch(path, branch)
        return branch is not None

    @classmethod
    def get_remote_branch_offline(cls, path: Path, branch: str, remote: str) -> Optional[RemoteBranch]:
        branches = GitFactory.get_remote_branches_offline(path, remote)
        branch = [b for b in branches if b.name == branch]
        return branch[0] if branch else None

    @classmethod
    def has_remote_branch_offline(cls, path: Path, branch: str, remote: str) -> bool:
        branch = GitFactory.get_remote_branch_offline(path, branch, remote)
        return branch is not None

    @classmethod
    def has_remote_branch_online(cls, path: Path, branch: str, remote: str, url: Optional[str] = None) -> bool:
        branch = GitFactory.get_remote_branch_online(path, branch, remote=remote, url=url)
        return branch is not None

    @classmethod
    def get_remote_branch_online(cls, path: Path, branch: str, remote: str,
                                 url: Optional[str] = None) -> Optional[RemoteBranch]:
        branches = GitFactory.get_remote_branches_online(path, remote=remote, url=url)
        branch = [b for b in branches if b.name == branch]
        return branch[0] if branch else None

    @classmethod
    def get_tracking_branch(cls, path: Path, branch: str, remote: Optional[str] = None) -> Optional[TrackingBranch]:
        branches = GitFactory.get_tracking_branches(path)
        branch = [b for b in branches if b.name == branch]
        if remote is None:
            return branch[0] if branch else None
        branch = [b for b in branch if b.upstream_branch.remote.name == remote]
        return branch[0] if branch else None

    @classmethod
    def has_tracking_branch(cls, path: Path, branch: str) -> bool:
        branch = GitFactory.get_tracking_branch(path, branch)
        return branch is not None

    @classmethod
    def get_local_tag(cls, path: Path, tag: str) -> Optional[LocalTag]:
        tags = GitFactory.get_local_tags(path)
        tag = [t for t in tags if t.name == tag]
        return tag[0] if tag else None

    @classmethod
    def has_local_tag(cls, path: Path, tag: str) -> bool:
        tag = GitFactory.get_local_tag(path, tag)
        return tag is not None

    @classmethod
    def get_remote_tag(cls, path: Path, tag: str, remote: str, url: Optional[str] = None) -> Optional[RemoteTag]:
        tags = GitFactory.get_remote_tags(path, remote, url=url)
        tag = [t for t in tags if t.name == tag]
        return tag[0] if tag else None

    @classmethod
    def has_remote_tag(cls, path: Path, tag: str, remote: str, url: Optional[str] = None) -> bool:
        tag = GitFactory.get_remote_tag(path, tag=tag, remote=remote, url=url)
        return tag is not None
