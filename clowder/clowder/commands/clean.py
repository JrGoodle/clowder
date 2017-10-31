# -*- coding: utf-8 -*-
"""Clowder command controller class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from clowder.commands.util import (
    run_group_command,
    run_project_command
)


def clean(groups, group_names, **kwargs):
    """Discard changes

    .. py:function:: clean(group_names, args='', recursive=False, project_names=None, skip=[])

    :param list(Group) groups: List of all groups
    :param list(str) group_names: Group names to clean
    :param str args: Git clean options
        - ``d`` Remove untracked directories in addition to untracked files
        - ``f`` Delete directories with .git sub directory or file
        - ``X`` Remove only files ignored by git
        - ``x`` Remove all untracked files
    :param bool recursive: Clean submodules recursively
    :param list(str) project_names: Project names to clean
    :param list(str) skip: Project names to skip
    """

    project_names = kwargs.get('project_names', None)
    skip = kwargs.get('skip', [])
    args = kwargs.get('args', '')
    recursive = kwargs.get('recursive', False)

    if project_names is None:
        filtered_groups = [g for g in groups if g.name in group_names]
        for group in filtered_groups:
            run_group_command(group, skip, 'clean', args=args, recursive=recursive)
        return

    projects = [p for g in groups for p in g.projects if p.name in project_names]
    for project in projects:
        run_project_command(project, skip, 'clean', args=args, recursive=recursive)


def clean_all(groups, group_names, **kwargs):
    """Discard all changes

    .. py:function:: clean_all(group_names, project_names=None, skip=[])

    :param list(Group) groups: List of all groups
    :param list(str) group_names: Group names to clean
    :param list(str) project_names: Project names to clean
    :param list(str) skip: Project names to skip
    """

    project_names = kwargs.get('project_names', None)
    skip = kwargs.get('skip', [])

    if project_names is None:
        filtered_groups = [g for g in groups if g.name in group_names]
        for group in filtered_groups:
            run_group_command(group, skip, 'clean_all')
        return

    projects = [p for g in groups for p in g.projects if p.name in project_names]
    for project in projects:
        run_project_command(project, skip, 'clean_all')
