"""Clowder command line forall controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import os

from pygoodle.app import BoolArgument, SingleArgument, Subcommand
from pygoodle.console import CONSOLE

import clowder.util.parallel as parallel
from clowder.controller import (
    CLOWDER_CONTROLLER,
    print_clowder_name,
    print_clowder_repo_status,
    valid_clowder_yaml_required
)
from clowder.config import Config
from clowder.util.error import CommandArgumentError

from .util import JobsArgument, ProjectsArgument


class ForallCommand(Subcommand):
    class Meta:
        name = 'forall'
        help = 'Run command or script in project directories'
        args = [
            SingleArgument('command', default=None,  help='command to run in project directories'),
            ProjectsArgument('projects and groups to run command for'),
            BoolArgument('--ignore-errors', '-i', help='ignore errors in command or script'),
            JobsArgument()
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

        check = not args.ignore_errors

        if jobs is not None and jobs != 1 and os.name == "posix":
            if jobs <= 0:
                jobs = 4
            parallel.forall(projects, jobs, command, check)
            return

        for project in projects:
            CONSOLE.stdout(project.status())
            project.run(command, check=check)
