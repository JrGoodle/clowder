# -*- coding: utf-8 -*-
"""Clowder command line clean controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import List, Optional

from cement.ext.ext_argparse import ArgparseController, expose

from clowder.clowder_controller import CLOWDER_CONTROLLER, ClowderController
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
    def clean(self) -> None:
        """Clowder clean command entry point"""

        self._clean()

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def _clean(self) -> None:
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
               skip=self.app.pargs.skip, clean_args=clean_args, recursive=self.app.pargs.recursive)


def _clean(clowder: ClowderController, group_names: List[str], clean_args: str = '', recursive: bool = False,
           project_names: Optional[List[str]] = None, skip: Optional[List[str]] = None) -> None:
    """Discard changes

    :param ClowderController clowder: ClowderController instance
    :param list[str] group_names: Group names to clean
    :param str clean_args: Git clean options
        - ``d`` Remove untracked directories in addition to untracked files
        - ``f`` Delete directories with .git sub directory or file
        - ``X`` Remove only files ignored by git
        - ``x`` Remove all untracked files
    :param bool recursive: Clean submodules recursively
    :param Optional[List[str]] project_names: Project names to clean
    :param Optional[List[str]] skip: Project names to skip
    """

    skip = [] if skip is None else skip

    if project_names is None:
        groups = filter_groups(clowder.groups, group_names)
        for group in groups:
            run_group_command(group, skip, 'clean', args=clean_args, recursive=recursive)
        return

    projects = filter_projects(clowder.groups, project_names=project_names)
    for project in projects:
        run_project_command(project, skip, 'clean', args=clean_args, recursive=recursive)


def _clean_all(clowder: ClowderController, group_names: List[str],
               project_names: Optional[List[str]] = None, skip: Optional[List[str]] = None) -> None:
    """Discard all changes

    :param ClowderController clowder: ClowderController instance
    :param list[str] group_names: Group names to clean
    :param Optional[List[str]] project_names: Project names to clean
    :param Optional[List[str]] skip: Project names to skip
    """

    skip = [] if skip is None else skip

    if project_names is None:
        groups = filter_groups(clowder.groups, group_names)
        for group in groups:
            run_group_command(group, skip, 'clean_all')
        return

    projects = filter_projects(clowder.groups, project_names=project_names)
    for project in projects:
        run_project_command(project, skip, 'clean_all')
