# -*- coding: utf-8 -*-
"""Clowder command controller class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

from clowder.commands.util import (
    filter_groups,
    filter_projects_on_project_names,
    run_group_command,
    run_project_command
)


def checkout(clowder, branch, group_names, **kwargs):
    """Checkout branches

    .. py:function:: checkout(branch, group_names, project_names=None, skip=[])

    :param ClowderController clowder: ClowderController instance
    :param str branch: Branch to checkout
    :param list(str) group_names: Group names to checkout branches for

    Keyword Args:
        project_names (list(str)): Project names to clean
        skip (list(str)): Project names to skip
    """

    project_names = kwargs.get('project_names', None)
    skip = kwargs.get('skip', [])

    if project_names is None:
        groups = filter_groups(clowder.groups, group_names)
        for group in groups:
            run_group_command(group, skip, 'checkout', branch)
        return

    projects = filter_projects_on_project_names(clowder.groups, project_names)
    for project in projects:
        run_project_command(project, skip, 'checkout', branch)
