# -*- coding: utf-8 -*-
"""Clowder command controller class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import clowder.util.formatting as fmt
from clowder.commands.util import run_group_command
from clowder.util.decorators import network_connection_required


def status(clowder_repo, clowder, fetch):
    """Print status for groups

    :param ClowderRepo clowder_repo: ClowderRepo instance
    :param ClowderController clowder: ClowderController instance
    :param bool fetch: Whether to fetch before printing status
    """

    if fetch:
        _fetch_projects(clowder_repo, clowder)
    else:
        clowder_repo.print_status()

    padding = len(max(clowder.get_all_project_paths(), key=len))

    for group in clowder.groups:
        print(fmt.group_name(group.name))
        for project in group.projects:
            print(project.status(padding=padding))


@network_connection_required
def _fetch_projects(clowder_repo, clowder):
    """fetch all projects

    :param ClowderRepo clowder_repo: ClowderRepo instance
    :param ClowderController clowder: ClowderController instance
    """

    clowder_repo.print_status(fetch=True)

    print(' - Fetch upstream changes for projects\n')
    for group in clowder.groups:
        run_group_command(group, [], 'fetch_all')
