# -*- coding: utf-8 -*-
"""Clowder command line clean controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import List

from cement.ext.ext_argparse import ArgparseController, expose

from clowder.clowder_controller import CLOWDER_CONTROLLER, ClowderController
from clowder.clowder_repo import print_clowder_repo_status
from clowder.util.decorators import valid_clowder_yaml_required
from clowder.util.clowder_utils import (
    filter_projects,
    options_help_message
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
            (['--projects', '-p'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                        default=['all'], nargs='+', metavar='PROJECT',
                                        help=options_help_message(CLOWDER_CONTROLLER.get_all_project_names(),
                                                                  'projects to clean')))
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
            projects = filter_projects(CLOWDER_CONTROLLER.projects, self.app.pargs.projects)
            for project in projects:
                print(project.status())
                project.clean_all()
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
        _clean(CLOWDER_CONTROLLER, self.app.pargs.projects, clean_args=clean_args, recursive=self.app.pargs.recursive)


def _clean(clowder: ClowderController, project_names: List[str], clean_args: str = '', recursive: bool = False) -> None:
    """Discard changes

    :param ClowderController clowder: ClowderController instance
    :param List[str] project_names: Project names to clean
    :param str clean_args: Git clean options
        - ``d`` Remove untracked directories in addition to untracked files
        - ``f`` Delete directories with .git sub directory or file
        - ``X`` Remove only files ignored by git
        - ``x`` Remove all untracked files
    :param bool recursive: Clean submodules recursively
    """

    projects = filter_projects(clowder.projects, project_names)
    for project in projects:
        print(project.status())
        project.clean(args=clean_args, recursive=recursive)
