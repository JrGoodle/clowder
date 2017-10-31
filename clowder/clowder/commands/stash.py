# -*- coding: utf-8 -*-
"""Clowder command controller class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from clowder.commands.util import (
    run_group_command,
    run_project_command
)


def stash(clowder, group_names, **kwargs):
    """Stash changes for projects with changes

    .. py:function:: clean(group_names, project_names=None, skip=[])

    :param ClowderController clowder: ClowderController instance
    :param list(str) group_names: Group names to stash
    :param list(str) project_names: Project names to clean
    :param list(str) skip: Project names to skip
    """

    project_names = kwargs.get('project_names', None)
    skip = kwargs.get('skip', [])

    if not any([g.is_dirty() for g in clowder.groups]):
        print('No changes to stash')
        return

    if project_names is None:
        groups = [g for g in clowder.groups if g.name in group_names]
        for group in groups:
            run_group_command(group, skip, 'stash')
        return

    projects = [p for g in clowder.groups for p in g.projects if p.name in project_names]
    for project in projects:
        run_project_command(project, skip, 'stash')
