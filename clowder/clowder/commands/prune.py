# -*- coding: utf-8 -*-
"""Clowder command controller class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import sys

from termcolor import cprint

from clowder.commands.util import (
    existing_branch_groups,
    existing_branch_projects,
    run_group_command,
    run_project_command,
    validate_groups,
    validate_projects
)


def prune(clowder, group_names, branch, **kwargs):
    """Prune branches

    .. py:function:: prune(group_names, local=False, remote=False, force=False, project_names=None, skip=[])

    :param ClowderController clowder: ClowderController instance
    :param list(str) group_names: Group names to prune branches for
    :param str branch: Branch to prune
    :param bool force: Force delete branch
    :param bool local: Delete local branch
    :param bool remote: Delete remote branch
    :param list(str) project_names: Project names to prune
    :param list(str) skip: Project names to skip
    """

    project_names = kwargs.get('project_names', None)
    skip = kwargs.get('skip', [])
    force = kwargs.get('force', False)
    local = kwargs.get('local', False)
    remote = kwargs.get('remote', False)

    if project_names is None:
        groups = [g for g in clowder.groups if g.name in group_names]
        validate_groups(groups)
        _prune_groups(groups, branch, skip=skip, force=force, local=local, remote=remote)
        return

    projects = [p for g in clowder.groups for p in g.projects if p.name in project_names]
    validate_projects(projects)
    _prune_projects(projects, branch, skip=skip, force=force, local=local, remote=remote)


def _prune_groups(groups, branch, **kwargs):
    """Prune group branches

    .. py:function:: _prune_groups(groups, branch, local=False, remote=False, force=False, skip=[])

    :param list(Group) groups: Groups to prune
    :param str branch: Branch to prune
    :param bool force: Force delete branch
    :param bool local: Delete local branch
    :param bool remote: Delete remote branch
    :param list(str) skip: Project names to skip
    """

    skip = kwargs.get('skip', [])
    force = kwargs.get('force', False)
    local = kwargs.get('local', False)
    remote = kwargs.get('remote', False)

    if local and remote:
        local_branch_exists = existing_branch_groups(groups, branch, is_remote=False)
        remote_branch_exists = existing_branch_groups(groups, branch, is_remote=True)
        branch_exists = local_branch_exists or remote_branch_exists
        if not branch_exists:
            cprint(' - No local or remote branches to prune\n', 'red')
            sys.exit()

        print(' - Prune local and remote branches\n')
        for group in groups:
            local_branch_exists = group.existing_branch(branch, is_remote=False)
            remote_branch_exists = group.existing_branch(branch, is_remote=True)
            if local_branch_exists or remote_branch_exists:
                run_group_command(group, skip, 'prune', branch, force=force, local=True, remote=True)
    elif local:
        if not existing_branch_groups(groups, branch, is_remote=False):
            print(' - No local branches to prune\n')
            sys.exit()

        for group in groups:
            if group.existing_branch(branch, is_remote=False):
                run_group_command(group, skip, 'prune', branch, force=force, local=True)
    elif remote:
        if not existing_branch_groups(groups, branch, is_remote=True):
            cprint(' - No remote branches to prune\n', 'red')
            sys.exit()

        for group in groups:
            if group.existing_branch(branch, is_remote=True):
                run_group_command(group, skip, 'prune', branch, remote=True)


def _prune_projects(projects, branch, **kwargs):
    """Prune project branches

    .. py:function:: _prune_projects(projects, branch, local=False, remote=False, force=False, skip=[])

    :param list(Project) projects: Projects to prune
    :param str branch: Branch to prune
    :param bool force: Force delete branch
    :param bool local: Delete local branch
    :param bool remote: Delete remote branch
    :param list(str) skip: Project names to skip
    """

    skip = kwargs.get('skip', [])
    force = kwargs.get('force', False)
    local = kwargs.get('local', False)
    remote = kwargs.get('remote', False)

    if local and remote:
        local_branch_exists = existing_branch_projects(projects, branch, is_remote=False)
        remote_branch_exists = existing_branch_projects(projects, branch, is_remote=True)
        branch_exists = local_branch_exists or remote_branch_exists
        if not branch_exists:
            cprint(' - No local or remote branches to prune\n', 'red')
            sys.exit()

        print(' - Prune local and remote branches\n')
        for project in projects:
            run_project_command(project, skip, 'prune', branch, force=force, local=True, remote=True)
    elif local:
        if not existing_branch_projects(projects, branch, is_remote=False):
            print(' - No local branches to prune\n')
            sys.exit()

        for project in projects:
            run_project_command(project, skip, 'prune', branch, force=force, local=True)
    elif remote:
        if not existing_branch_projects(projects, branch, is_remote=True):
            cprint(' - No remote branches to prune\n', 'red')
            sys.exit()

        for project in projects:
            run_project_command(project, skip, 'prune', branch, remote=True)
