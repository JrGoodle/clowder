# -*- coding: utf-8 -*-
"""Clowder command controller class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

from clowder.commands.util import (
    run_group_command,
    run_project_command
)


def checkout(clowder, branch, group_names, **kwargs):
    """Checkout branches

    .. py:function:: checkout(branch, group_names, project_names=None, skip=[])

    :param ClowderController clowder: ClowderController instance
    :param str branch: Branch to checkout
    :param list(str) group_names: Group names to checkout branches for
    :param list(str) project_names: Project names to clean
    :param list(str) skip: Project names to skip
    """

    project_names = kwargs.get('project_names', None)
    skip = kwargs.get('skip', [])

    if project_names is None:
        groups = [g for g in clowder.groups if g.name in group_names]
        for group in groups:
            run_group_command(group, skip, 'checkout', branch)
        return

    projects = [p for g in clowder.groups for p in g.projects if p.name in project_names]
    for project in projects:
        run_project_command(project, skip, 'checkout', branch)
