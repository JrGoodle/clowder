"""Clowder command line forall controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import argparse
import os
from typing import List, Optional

import clowder.util.formatting as fmt
import clowder.util.parallel as parallel
from clowder.clowder_controller import CLOWDER_CONTROLLER, print_clowder_name, valid_clowder_yaml_required
from clowder.config import Config
from clowder.git.clowder_repo import print_clowder_repo_status
from clowder.util.console import CONSOLE
from clowder.util.error import CommandArgumentError

from .util import add_parser_arguments


def add_forall_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa
    """Add clowder forall parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    parser = subparsers.add_parser('forall', help='Run command or script in project directories')
    parser.formatter_class = argparse.RawTextHelpFormatter
    parser.set_defaults(func=forall)

    add_parser_arguments(parser, [
        (['command'], dict(metavar='<command>', nargs=1, default=None,
                           help='command to run in project directories')),
        (['projects'], dict(metavar='<project|group>', default='default', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices_with_default,
                            help=fmt.project_options_help_message('projects and groups to run command for'))),
        (['--ignore-errors', '-i'], dict(action='store_true', help='ignore errors in command or script')),
        (['--jobs', '-j'], dict(metavar='<n>', nargs=1, default=None, type=int,
                                help='number of jobs to use running commands in parallel')),
    ])


# TODO: Split out forall_handler() to parse args, then call typed forall() function
@valid_clowder_yaml_required
@print_clowder_name
@print_clowder_repo_status
def forall(args) -> None:
    """Clowder forall command private implementation

    :raise CommandArgumentError:
    """

    jobs = None
    if args.jobs:
        jobs = args.jobs[0]

    if not args.command:
        raise CommandArgumentError('Missing command')
    command = args.command[0]

    _forall_impl(command, args.ignore_errors, projects=args.projects, jobs=jobs)


def _forall_impl(command: str, ignore_errors: bool, projects: List[str], jobs: Optional[int] = None) -> None:
    """Runs script in project directories specified

    :param str command: Command or script and optional arguments
    :param bool ignore_errors: Whether to exit if command returns a non-zero exit code
    :param List[str] projects: Project names to clean
    :param Optional[int] jobs: Number of jobs to use running parallel commands
    """

    projects = Config().process_projects_arg(projects)
    projects = CLOWDER_CONTROLLER.filter_projects(CLOWDER_CONTROLLER.projects, projects)

    jobs_config = Config().jobs
    jobs = jobs_config if jobs_config is not None else jobs

    if jobs is not None and jobs != 1 and os.name == "posix":
        if jobs <= 0:
            jobs = 4
        parallel.forall(projects, jobs, command, ignore_errors)
        return

    for project in projects:
        CONSOLE.stdout(project.status())
        project.run(command, ignore_errors=ignore_errors)
