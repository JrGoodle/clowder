"""Clowder command line forall controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import os

from pygoodle.app import Argument, Subcommand
from pygoodle.console import CONSOLE

import clowder.util.formatting as fmt
import clowder.util.parallel as parallel
from clowder.clowder_controller import CLOWDER_CONTROLLER, print_clowder_name, valid_clowder_yaml_required
from clowder.config import Config
from clowder.git.clowder_repo import print_clowder_repo_status
from clowder.util.error import CommandArgumentError


class ForallCommand(Subcommand):

    name = 'forall'
    help = 'Run command or script in project directories'
    args = [
        Argument(
            'command',
            nargs=1,
            default=None,
            help='command to run in project directories'
        ),
        Argument(
            'projects',
            metavar='<project|group>',
            default='default',
            nargs='*',
            choices=CLOWDER_CONTROLLER.project_choices_with_default,
            help=fmt.project_options_help_message('projects and groups to run command for')
        ),
        Argument('--ignore-errors', '-i', action='store_true', help='ignore errors in command or script'),
        Argument(
            '--jobs', '-j',
            metavar='<n>',
            nargs=1,
            default=None,
            type=int,
            help='number of jobs to use running commands in parallel')
    ]

    @valid_clowder_yaml_required
    @print_clowder_name
    @print_clowder_repo_status
    def run(self, args) -> None:
        jobs = None
        if args.jobs:
            jobs = args.jobs[0]
        jobs_config = Config().jobs
        jobs = jobs_config if jobs_config is not None else jobs

        if not args.command:
            raise CommandArgumentError('Missing command')
        command = args.command[0]

        projects = Config().process_projects_arg(args.projects)
        projects = CLOWDER_CONTROLLER.filter_projects(CLOWDER_CONTROLLER.projects, projects)

        ignore_errors = args.ignore_errors

        if jobs is not None and jobs != 1 and os.name == "posix":
            if jobs <= 0:
                jobs = 4
            parallel.forall(projects, jobs, command, ignore_errors)
            return

        for project in projects:
            CONSOLE.stdout(project.status())
            project.run(command, ignore_errors=ignore_errors)
