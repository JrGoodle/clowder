# -*- coding: utf-8 -*-
"""Clowder start command

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from clowder.commands.util import (
    filter_groups,
    filter_projects_on_project_names,
    run_group_command,
    run_project_command,
    validate_groups,
    validate_projects
)


def start_groups(clowder, group_names, skip, branch, tracking=False):
    """Start feature branch for groups

    :param ClowderController clowder: ClowderController instance
    :param list(str) group_names: Group names to create branches for
    :param list(str) skip: Project names to skip
    :param str branch: Local branch name to create
    :param Optional[bool] tracking: Whether to create a remote branch with tracking relationship.
        Defaults to False
    """

    groups = filter_groups(clowder.groups, group_names)
    validate_groups(groups)
    for group in groups:
        run_group_command(group, skip, 'start', branch, tracking)


def start_projects(clowder, project_names, skip, branch, tracking=False):
    """Start feature branch for projects

    :param ClowderController clowder: ClowderController instance
    :param list(str) project_names: Project names to creat branches for
    :param list(str) skip: Project names to skip
    :param str branch: Local branch name to create
    :param Optional[bool] tracking: Whether to create a remote branch with tracking relationship.
        Defaults to False
    """

    projects = filter_projects_on_project_names(clowder.groups, project_names)
    validate_projects(projects)
    for project in projects:
        run_project_command(project, skip, 'start', branch, tracking)
