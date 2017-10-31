# -*- coding: utf-8 -*-
"""Clowder command controller class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from clowder.commands.util import (
    run_group_command,
    run_project_command
)


def diff(groups, group_names, project_names=None):
    """Show git diff

    :param list(Group) groups: List of all groups
    :param list(str) group_names: Group names to print diffs for
    :param Optional[list(str)] project_names: Project names to print diffs for. Defaults to None
    """

    if project_names is None:
        filtered_groups = [g for g in groups if g.name in group_names]
        for group in filtered_groups:
            run_group_command(group, [], 'diff')
        return

    projects = [p for g in groups for p in g.projects if p.name in project_names]
    for project in projects:
        run_project_command(project, [], 'diff')
