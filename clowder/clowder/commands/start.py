# -*- coding: utf-8 -*-
"""Clowder command controller class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from clowder.commands.util import (
    run_group_command,
    run_project_command,
    validate_groups,
    validate_projects
)


def start_groups(groups, group_names, skip, branch, tracking=False):
    """Start feature branch for groups

    :param list(Group) groups: List of all groups
    :param list(str) group_names: Group names to create branches for
    :param list(str) skip: Project names to skip
    :param str branch: Local branch name to create
    :param Optional[bool] tracking: Whether to create a remote branch with tracking relationship.
        Defaults to False
    """

    filtered_groups = [g for g in groups if g.name in group_names]
    validate_groups(filtered_groups)
    for group in filtered_groups:
        run_group_command(group, skip, 'start', branch, tracking)


def start_projects(groups, project_names, skip, branch, tracking=False):
    """Start feature branch for projects

    :param list(Group) groups: List of all groups
    :param list(str) project_names: Project names to creat branches for
    :param list(str) skip: Project names to skip
    :param str branch: Local branch name to create
    :param Optional[bool] tracking: Whether to create a remote branch with tracking relationship.
        Defaults to False
    """

    projects = [p for g in groups for p in g.projects if p.name in project_names]
    validate_projects(projects)
    for project in projects:
        run_project_command(project, skip, 'start', branch, tracking)
