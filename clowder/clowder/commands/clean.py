# -*- coding: utf-8 -*-
"""Clowder clean command

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from clowder.commands.util import (
    filter_groups,
    filter_projects_on_project_names,
    run_group_command,
    run_project_command
)


def clean(clowder, group_names, **kwargs):
    """Discard changes

    .. py:function:: clean(group_names, args='', recursive=False, project_names=None, skip=[])

    :param ClowderController clowder: ClowderController instance
    :param list(str) group_names: Group names to clean

    Keyword Args:
        args (str): Git clean options
            - ``d`` Remove untracked directories in addition to untracked files
            - ``f`` Delete directories with .git sub directory or file
            - ``X`` Remove only files ignored by git
            - ``x`` Remove all untracked files
        recursive (bool): Clean submodules recursively
        project_names (list(str)): Project names to clean
        skip (list(str)): Project names to skip
    """

    project_names = kwargs.get('project_names', None)
    skip = kwargs.get('skip', [])
    args = kwargs.get('args', '')
    recursive = kwargs.get('recursive', False)

    if project_names is None:
        groups = filter_groups(clowder.groups, group_names)
        for group in groups:
            run_group_command(group, skip, 'clean', args=args, recursive=recursive)
        return

    projects = filter_projects_on_project_names(clowder.groups, project_names)
    for project in projects:
        run_project_command(project, skip, 'clean', args=args, recursive=recursive)


def clean_all(clowder, group_names, **kwargs):
    """Discard all changes

    .. py:function:: clean_all(group_names, project_names=None, skip=[])

    :param ClowderController clowder: ClowderController instance
    :param list(str) group_names: Group names to clean

    Keyword Args:
        project_names (list(str)): Project names to clean
        skip (list(str)): Project names to skip
    """

    project_names = kwargs.get('project_names', None)
    skip = kwargs.get('skip', [])

    if project_names is None:
        groups = filter_groups(clowder.groups, group_names)
        for group in groups:
            run_group_command(group, skip, 'clean_all')
        return

    projects = filter_projects_on_project_names(clowder.groups, project_names)
    for project in projects:
        run_project_command(project, skip, 'clean_all')
