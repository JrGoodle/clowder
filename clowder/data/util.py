# -*- coding: utf-8 -*-
"""Clowder model utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import Tuple

import clowder.util.formatting as fmt
from clowder.error import ClowderError, ClowderErrorType

from .resolved_project import ResolvedProject


def existing_branch_projects(projects: Tuple[ResolvedProject, ...], branch: str, is_remote: bool) -> bool:
    """Checks if given branch exists in any project

    :param Tuple[ResolvedProject, ...] projects: Projects to check
    :param str branch: Branch to check for
    :param bool is_remote: Check for remote branch
    :return: True, if at least one branch exists
    :rtype: bool
    """

    return any([p.existing_branch(branch, is_remote=is_remote) for p in projects])


def filter_projects(projects: Tuple[ResolvedProject, ...], project_names: Tuple[str, ...]) -> Tuple[ResolvedProject, ...]:
    """Filter projects based on given project or group names

    :param Tuple[ResolvedProject, ...] projects: Projects to filter
    :param Tuple[str, ...] project_names: Project names to match against
    :return: Projects in groups matching given names
    :rtype: Tuple[ResolvedProject, ...]
    """

    filtered_projects = []
    for name in project_names:
        filtered_projects += [p for p in projects if name in p.groups]
    return tuple(sorted(set(filtered_projects), key=lambda project: project.name))


def print_parallel_projects_output(projects: Tuple[ResolvedProject, ...]) -> None:
    """Print output for parallel project command

    :param Tuple[ResolvedProject, ...] projects: Projects to print output for
    """

    for project in projects:
        print(project.status())
        _print_upstream_output(project)


def validate_project_statuses(projects: Tuple[ResolvedProject, ...], allow_missing_repo: bool = True) -> None:
    """Validate status of all projects

    :param Tuple[ResolvedProject, ...] projects: Projects to validate
    :param bool allow_missing_repo: Whether to allow validation to succeed with missing repo
    :raise ClowderError:
    """

    for p in projects:
        p.print_validation(allow_missing_repo=allow_missing_repo)
    if not all([p.is_valid(allow_missing_repo=allow_missing_repo) for p in projects]):
        print()
        raise ClowderError(ClowderErrorType.INVALID_PROJECT_STATUS, fmt.error_invalid_project_state())


def _print_upstream_output(project: ResolvedProject) -> None:
    """Print upstream output if a upstream exists

    :param ResolvedProject project: Project to print upstream status for
    """

    if project.upstream:
        print('  ' + fmt.upstream_string(project.name))
        print('  ' + fmt.upstream_string(project.upstream.name))
