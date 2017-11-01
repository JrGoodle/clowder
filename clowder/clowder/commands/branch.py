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


def branch(clowder, group_names, **kwargs):
    """Print branches

    .. py:function:: branch(group_names, local=False, remote=False, project_names=None, skip=[])

    :param ClowderController clowder: ClowderController instance
    :param list(str) group_names: Group names to print branches for
    :param bool local: Print local branches
    :param bool remote: Print remote branches
    :param list(str) project_names: Project names to print branches for
    :param list(str) skip: Project names to skip
    """

    project_names = kwargs.get('project_names', None)
    skip = kwargs.get('skip', [])
    local = kwargs.get('local', False)
    remote = kwargs.get('remote', False)

    if project_names is None:
        groups = filter_groups(clowder.groups, group_names)
        for group in groups:
            run_group_command(group, skip, 'branch', local=local, remote=remote)
        return

    projects = filter_projects_on_project_names(clowder.groups, project_names)
    for project in projects:
        run_project_command(project, skip, 'branch', local=local, remote=remote)
