# -*- coding: utf-8 -*-
"""Clowder command line prune controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

from cement.ext.ext_argparse import ArgparseController, expose
from termcolor import cprint

from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.clowder_repo import print_clowder_repo_status
from clowder.error.clowder_error import ClowderError
from clowder.util.connectivity import network_connection_required
from clowder.util.decorators import valid_clowder_yaml_required
from clowder.util.clowder_utils import (
    existing_branch_groups,
    existing_branch_projects,
    filter_groups,
    filter_projects,
    options_help_message,
    run_group_command,
    run_project_command,
    validate_groups,
    validate_projects
)


class PruneController(ArgparseController):
    """Clowder prune command controller"""

    class Meta:
        """Clowder prune Meta configuration"""

        label = 'prune'
        stacked_on = 'base'
        stacked_type = 'embedded'
        description = 'Prune branches'

    @expose(
        help='Prune branches',
        arguments=[
            (['branch'], dict(help='name of branch to remove', metavar='BRANCH')),
            (['--force', '-f'], dict(action='store_true', help='force prune branches')),
            (['--all', '-a'], dict(action='store_true', help='prune local and remote branches')),
            (['--remote', '-r'], dict(action='store_true', help='prune remote branches')),
            (['--groups', '-g'], dict(choices=CLOWDER_CONTROLLER.get_all_group_names(),
                                      default=CLOWDER_CONTROLLER.get_all_group_names(),
                                      nargs='+', metavar='GROUP',
                                      help=options_help_message(CLOWDER_CONTROLLER.get_all_group_names(),
                                                                'groups to prune'))),
            (['--projects', '-p'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                        nargs='+', metavar='PROJECT',
                                        help=options_help_message(CLOWDER_CONTROLLER.get_all_project_names(),
                                                                  'projects to prune'))),
            (['--skip', '-s'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                    nargs='+', metavar='PROJECT', default=[],
                                    help=options_help_message(CLOWDER_CONTROLLER.get_all_project_names(),
                                                              'projects to skip')))
        ]
    )
    def prune(self):
        """Clowder prune command entry point"""

        self._prune()

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def _prune(self):
        """Clowder prune command private implementation"""

        if self.app.pargs.all:
            self._prune_all()
            return

        if self.app.pargs.remote:
            self._prune_remote()
            return

        _prune(CLOWDER_CONTROLLER, self.app.pargs.groups, self.app.pargs.branch,
               project_names=self.app.pargs.projects,
               skip=self.app.pargs.skip, force=self.app.pargs.force, local=True)

    @network_connection_required
    def _prune_all(self):
        """clowder prune all command"""

        _prune(CLOWDER_CONTROLLER, self.app.pargs.groups, self.app.pargs.branch,
               project_names=self.app.pargs.projects, skip=self.app.pargs.skip,
               force=self.app.pargs.force, local=True, remote=True)

    @network_connection_required
    def _prune_remote(self):
        """clowder prune remote command"""

        _prune(CLOWDER_CONTROLLER, self.app.pargs.groups, self.app.pargs.branch,
               project_names=self.app.pargs.projects,
               skip=self.app.pargs.skip, remote=True)


def _prune(clowder, group_names, branch, **kwargs):
    """Prune branches

    .. py:function:: prune(group_names, local=False, remote=False, force=False, project_names=None, skip=[])

    :param ClowderController clowder: ClowderController instance
    :param list[str] group_names: Group names to prune branches for
    :param str branch: Branch to prune

    Keyword Args:
        force (bool): Force delete branch
        local (bool): Delete local branch
        remote (bool): Delete remote branch
        project_names (list[str]): Project names to prune
        skip (list[str]): Project names to skip
    """

    project_names = kwargs.get('project_names', None)
    skip = kwargs.get('skip', [])
    force = kwargs.get('force', False)
    local = kwargs.get('local', False)
    remote = kwargs.get('remote', False)

    if project_names is None:
        groups = filter_groups(clowder.groups, group_names)
        validate_groups(groups)
        _prune_groups(groups, branch, skip=skip, force=force, local=local, remote=remote)
        return

    projects = filter_projects(clowder.groups, project_names=project_names)
    validate_projects(projects)
    _prune_projects(projects, branch, skip=skip, force=force, local=local, remote=remote)


def _prune_groups(groups, branch, **kwargs):
    """Prune group branches

    .. py:function:: _prune_groups(groups, branch, local=False, remote=False, force=False, skip=[])

    :param list[Group] groups: Groups to prune
    :param str branch: Branch to prune

    Keyword Args:
        force (bool): Force delete branch
        local (bool): Delete local branch
        remote (bool): Delete remote branch
        skip (list[str]): Project names to skip
    """

    skip = kwargs.get('skip', [])
    force = kwargs.get('force', False)
    local = kwargs.get('local', False)
    remote = kwargs.get('remote', False)

    local_branch_exists = existing_branch_groups(groups, branch, is_remote=False)
    remote_branch_exists = existing_branch_groups(groups, branch, is_remote=True)

    try:
        _validate_branches(local, remote, local_branch_exists, remote_branch_exists)
    except ClowderError:
        pass
    else:
        for group in groups:
            if group.existing_branch(branch, is_remote=remote):
                run_group_command(group, skip, 'prune', branch, force=force, local=local, remote=remote)


def _prune_projects(projects, branch, **kwargs):
    """Prune project branches

    .. py:function:: _prune_projects(projects, branch, local=False, remote=False, force=False, skip=[])

    :param list[Project] projects: Projects to prune
    :param str branch: Branch to prune

    Keyword Args:
        force (bool): Force delete branch
        local (bool): Delete local branch
        remote (bool): Delete remote branch
        skip (list[str]): Project names to skip
    """

    skip = kwargs.get('skip', [])
    force = kwargs.get('force', False)
    local = kwargs.get('local', False)
    remote = kwargs.get('remote', False)

    local_branch_exists = existing_branch_projects(projects, branch, is_remote=False)
    remote_branch_exists = existing_branch_projects(projects, branch, is_remote=True)

    try:
        _validate_branches(local, remote, local_branch_exists, remote_branch_exists)
    except ClowderError:
        pass
    else:
        for project in projects:
            run_project_command(project, skip, 'prune', branch, force=force, local=local, remote=remote)


def _validate_branches(local, remote, local_branch_exists, remote_branch_exists):
    """Prune project branches

    .. py:function:: _prune_projects(projects, branch, local=False, remote=False, force=False, skip=[])

    :param bool local: Delete local branch
    :param bool remote: Delete remote branch
    :param bool local_branch_exists: Whether a local branch exists
    :param bool remote_branch_exists: Whether a remote branch exists
    :raise ClowderError:
    """

    if local and remote:
        branch_exists = local_branch_exists or remote_branch_exists
        if not branch_exists:
            cprint(' - No local or remote branches to prune\n', 'red')
            raise ClowderError
        print(' - Prune local and remote branches\n')
        return

    if remote:
        if not remote_branch_exists:
            cprint(' - No remote branches to prune\n', 'red')
            raise ClowderError
        print(' - Prune remote branches\n')
        return

    if not local_branch_exists:
        print(' - No local branches to prune\n')
        raise ClowderError
    print(' - Prune local branches\n')
