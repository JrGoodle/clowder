# -*- coding: utf-8 -*-
"""Clowder diff command

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from clowder.commands.util import (
    filter_groups,
    filter_projects_on_project_names,
    run_group_command,
    run_project_command
)


def diff(clowder, group_names, project_names=None):
    """Show git diff

    :param ClowderController clowder: ClowderController instance
    :param list[str] group_names: Group names to print diffs for
    :param Optional[list[str]] project_names: Project names to print diffs for. Defaults to None
    """

    if project_names is None:
        groups = filter_groups(clowder.groups, group_names)
        for group in groups:
            run_group_command(group, [], 'diff')
        return

    projects = filter_projects_on_project_names(clowder.groups, project_names)
    for project in projects:
        run_project_command(project, [], 'diff')
