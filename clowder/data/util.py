"""Clowder model utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from typing import Tuple

import clowder.util.formatting as fmt
from clowder.console import CONSOLE
from clowder.error import ProjectStatusError

from .resolved_project import ResolvedProject


def project_has_branch(projects: Tuple[ResolvedProject, ...], branch: str, is_remote: bool) -> bool:
    """Checks if given branch exists in any project

    :param Tuple[ResolvedProject, ...] projects: Projects to check
    :param str branch: Branch to check for
    :param bool is_remote: Check for remote branch
    :return: True, if at least one branch exists
    """

    return any([p.has_branch(branch, is_remote=is_remote) for p in projects])


def filter_projects(projects: Tuple[ResolvedProject, ...],
                    project_names: Tuple[str, ...]) -> Tuple[ResolvedProject, ...]:
    """Filter projects based on given project or group names

    :param Tuple[ResolvedProject, ...] projects: Projects to filter
    :param Tuple[str, ...] project_names: Project names to match against
    :return: Projects in groups matching given names
    """

    filtered_projects = []
    for name in project_names:
        filtered_projects += [p for p in projects if name in p.groups]
    return tuple(sorted(set(filtered_projects), key=lambda project: project.name))


def validate_project_statuses(projects: Tuple[ResolvedProject, ...], allow_missing_repo: bool = True) -> None:
    """Validate status of all projects

    :param Tuple[ResolvedProject, ...] projects: Projects to validate
    :param bool allow_missing_repo: Whether to allow validation to succeed with missing repo
    :raise ProjectStatusError:
    """

    for p in projects:
        p.print_validation(allow_missing_repo=allow_missing_repo)
    if not all([p.is_valid(allow_missing_repo=allow_missing_repo) for p in projects]):
        CONSOLE.stdout()
        raise ProjectStatusError("Invalid project state")


def _print_upstream_output(project: ResolvedProject) -> None:
    """Print upstream output if a upstream exists

    :param ResolvedProject project: Project to print upstream status for
    """

    if project.upstream:
        CONSOLE.stdout('  ' + fmt.upstream(project.name))
        CONSOLE.stdout('  ' + fmt.upstream(project.upstream.name))
