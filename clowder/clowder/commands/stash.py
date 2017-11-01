# -*- coding: utf-8 -*-
"""Clowder stash command

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from clowder.commands.util import (
    filter_groups,
    filter_projects_on_project_names,
    run_group_command,
    run_project_command
)


def stash(clowder, group_names, **kwargs):
    """Stash changes for projects with changes

    .. py:function:: clean(group_names, project_names=None, skip=[])

    :param ClowderController clowder: ClowderController instance
    :param list[str] group_names: Group names to stash

    Keyword Args:
        project_names (list[str]): Project names to clean
        skip (list[str]): Project names to skip
    """

    project_names = kwargs.get('project_names', None)
    skip = kwargs.get('skip', [])

    if not any([g.is_dirty() for g in clowder.groups]):
        print('No changes to stash')
        return

    if project_names is None:
        groups = filter_groups(clowder.groups, group_names)
        for group in groups:
            run_group_command(group, skip, 'stash')
        return

    projects = filter_projects_on_project_names(clowder.groups, project_names)
    for project in projects:
        run_project_command(project, skip, 'stash')
