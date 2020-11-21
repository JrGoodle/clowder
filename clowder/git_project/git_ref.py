"""clowder ref enum

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from enum import auto, unique
from typing import Optional

from git import Repo, GitError

from clowder.error import *
from clowder.util.enum import AutoLowerName


@unique
class GitRefEnum(AutoLowerName):
    BRANCH = auto()
    TAG = auto()
    COMMIT = auto()


class GitRef(object):
    """Class encapsulating git ref

    :ivar GitRefEnum ref_type: Ref type
    :ivar Optional[str] branch: Branch
    :ivar Optional[str] tag: Tag
    :ivar Optional[str] commit: Commit
    :ivar str formatted_ref: Formatted ref
    """

    def __init__(self, branch: Optional[str] = None, tag: Optional[str] = None, commit: Optional[str] = None):
        """GitRepo __init__

        :param Optional[str] branch: Branch
        :param Optional[str] tag: Tag
        :param Optional[str] commit: Commit
        :raise ClowderError:
        :raise UnknownTypeError:
        """

        arguments_count = len([ref for ref in [branch, tag, commit] if ref is not None])
        if arguments_count == 0:
            raise CommandArgumentError('GitRef init requires one argument')
        elif arguments_count > 1:
            raise CommandArgumentError('GitRef init only allows one argument')

        self.branch: Optional[str] = branch
        self.tag: Optional[str] = tag
        self.commit: Optional[str] = commit

        if self.branch is not None:
            self.ref_type: GitRefEnum = GitRefEnum.BRANCH
        elif self.tag is not None:
            self.ref_type: GitRefEnum = GitRefEnum.TAG
        elif self.commit is not None:
            self.ref_type: GitRefEnum = GitRefEnum.COMMIT
        else:
            raise UnknownTypeError('Invalid GitRef type')

        self.check_ref_format(self.formatted_ref)

    @property
    def short_ref(self) -> str:
        """Short git ref

        :raise UnknownTypeError:
        """
        if self.ref_type is GitRefEnum.BRANCH:
            return self.truncate_ref(self.branch)
        elif self.ref_type is GitRefEnum.TAG:
            return self.truncate_ref(self.tag)
        elif self.ref_type is GitRefEnum.COMMIT:
            return self.commit
        else:
            raise UnknownTypeError('Invalid GitRefEnum type')

    @property
    def formatted_ref(self) -> str:
        """Formatted git ref

        :raise UnknownTypeError:
        """

        if self.ref_type is GitRefEnum.BRANCH:
            return self.format_git_branch(self.branch)
        elif self.ref_type is GitRefEnum.TAG:
            return self.format_git_tag(self.tag)
        elif self.ref_type is GitRefEnum.COMMIT:
            return self.commit
        else:
            raise UnknownTypeError('Invalid GitRefEnum type')

    @staticmethod
    def truncate_ref(ref: str) -> str:
        """Return bare branch, tag, or sha

        :param str ref: Full pathspec or short ref
        :return: Ref with 'refs/heads/' and 'refs/tags/' prefix removed
        """

        git_branch = "refs/heads/"
        git_tag = "refs/tags/"
        if ref.startswith(git_branch):
            length = len(git_branch)
        elif ref.startswith(git_tag):
            length = len(git_tag)
        else:
            length = 0
        return ref[length:]

    @staticmethod
    def format_git_branch(branch: str) -> str:
        """Returns properly formatted git branch

        :param str branch: Git branch name
        :return: Branch prefixed with 'refs/heads/'
        """

        prefix = "refs/heads/"
        return branch if branch.startswith(prefix) else f"{prefix}{branch}"

    @staticmethod
    def format_git_tag(tag: str) -> str:
        """Returns properly formatted git tag

        :param str tag: Git tag name
        :return: Tag prefixed with 'refs/heads/'
        """

        prefix = "refs/tags/"
        return tag if tag.startswith(prefix) else f"{prefix}{tag}"

    @classmethod
    def branch(cls, branch: str) -> 'GitRef':
        return GitRef(branch=branch)

    @classmethod
    def tag(cls, tag: str) -> 'GitRef':
        return GitRef(tag=tag)

    @classmethod
    def commit(cls, commit: str) -> 'GitRef':
        return GitRef(commit=commit)

    @staticmethod
    def check_ref_format(ref: str) -> bool:
        """Check if git ref is correctly formatted

        :param str ref: Git ref
        :return: True, if git ref is a valid format
        """
        try:
            Repo().git.check_ref_format('--normalize', ref)
        except GitError:
            return False
        else:
            return True
