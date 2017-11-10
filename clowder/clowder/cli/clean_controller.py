# -*- coding: utf-8 -*-
"""Clowder command line clean controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import ArgparseController, expose

from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.clowder_repo import print_clowder_repo_status
from clowder.util.decorators import valid_clowder_yaml_required
from clowder.util.clowder_utils import (
    filter_groups,
    filter_projects,
    options_help_message,
    run_group_command,
    run_project_command
)


class CleanController(ArgparseController):
    """Clowder clean command controller"""

    class Meta:
        """Clowder clean Meta configuration"""

        label = 'clean'
        stacked_on = 'base'
        stacked_type = 'embedded'
        description = 'Discard current changes in projects'

    @expose(
        help='Discard current changes in projects',
        arguments=[
            (['--all', '-a'], dict(action='store_true', help='clean all the things')),
            (['--recursive', '-r'], dict(action='store_true', help='clean submodules recursively')),
            (['-d'], dict(action='store_true', help='remove untracked directories')),
            (['-f'], dict(action='store_true', help='remove directories with .git subdirectory or file')),
            (['-X'], dict(action='store_true', help='remove only files ignored by git')),
            (['-x'], dict(action='store_true', help='remove all untracked files')),
            (['--groups', '-g'], dict(choices=CLOWDER_CONTROLLER.get_all_group_names(),
                                      default=CLOWDER_CONTROLLER.get_all_group_names(),
                                      nargs='+', metavar='GROUP',
                                      help=options_help_message(CLOWDER_CONTROLLER.get_all_group_names(),
                                                                'groups to clean'))),
            (['--projects', '-p'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                        nargs='+', metavar='PROJECT',
                                        help=options_help_message(CLOWDER_CONTROLLER.get_all_project_names(),
                                                                  'projects to clean'))),
            (['--skip', '-s'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                    nargs='+', metavar='PROJECT', default=[],
                                    help=options_help_message(CLOWDER_CONTROLLER.get_all_project_names(),
                                                              'projects to skip')))
            ]
    )
    def clean(self):
        """Clowder clean command entry point"""

        self._clean()

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def _clean(self):
        """Clowder clean command private implementation"""

        if self.app.pargs.all:
            _clean_all(CLOWDER_CONTROLLER, group_names=self.app.pargs.groups,
                       project_names=self.app.pargs.projects, skip=self.app.pargs.skip)
            return

        clean_args = ''
        if self.app.pargs.d:
            clean_args += 'd'
        if self.app.pargs.f:
            clean_args += 'f'
        if self.app.pargs.X:
            clean_args += 'X'
        if self.app.pargs.x:
            clean_args += 'x'
        _clean(CLOWDER_CONTROLLER, group_names=self.app.pargs.groups, project_names=self.app.pargs.projects,
               skip=self.app.pargs.skip, args=clean_args, recursive=self.app.pargs.recursive)


def _clean(clowder, group_names, **kwargs):
    """Discard changes

    .. py:function:: clean(group_names, args='', recursive=False, project_names=None, skip=[])

    :param ClowderController clowder: ClowderController instance
    :param list[str] group_names: Group names to clean

    Keyword Args:
        args (str): Git clean options
            - ``d`` Remove untracked directories in addition to untracked files
            - ``f`` Delete directories with .git sub directory or file
            - ``X`` Remove only files ignored by git
            - ``x`` Remove all untracked files
        recursive (bool): Clean submodules recursively
        project_names (list[str]): Project names to clean
        skip (list[str]): Project names to skip
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

    projects = filter_projects(clowder.groups, project_names=project_names)
    for project in projects:
        run_project_command(project, skip, 'clean', args=args, recursive=recursive)


def _clean_all(clowder, group_names, **kwargs):
    """Discard all changes

    .. py:function:: clean_all(group_names, project_names=None, skip=[])

    :param ClowderController clowder: ClowderController instance
    :param list[str] group_names: Group names to clean

    Keyword Args:
        project_names (list[str]): Project names to clean
        skip (list[str]): Project names to skip
    """

    project_names = kwargs.get('project_names', None)
    skip = kwargs.get('skip', [])

    if project_names is None:
        groups = filter_groups(clowder.groups, group_names)
        for group in groups:
            run_group_command(group, skip, 'clean_all')
        return

    projects = filter_projects(clowder.groups, project_names=project_names)
    for project in projects:
        run_project_command(project, skip, 'clean_all')
