"""Clowder command line reset controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import argparse
import os
from typing import List, Optional

import clowder.util.formatting as fmt
import clowder.util.parallel as parallel
from clowder.clowder_controller import CLOWDER_CONTROLLER, print_clowder_name, valid_clowder_yaml_required
from clowder.config import Config
from clowder.git.clowder_repo import print_clowder_repo_status_fetch
from clowder.util.connectivity import network_connection_required

from .util import add_parser_arguments


def add_reset_parser(subparsers: argparse._SubParsersAction):  # noqa
    """Add clowder reset parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    parser = subparsers.add_parser('reset', help='Reset branches to upstream commits or '
                                                 'check out detached HEADs for tags and shas')
    parser.formatter_class = argparse.RawTextHelpFormatter
    parser.set_defaults(func=reset)

    add_parser_arguments(parser, [
        (['projects'], dict(metavar='<project|group>', default='default', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices_with_default,
                            help=fmt.project_options_help_message('projects and groups to reset'))),
        (['--jobs', '-j'], dict(metavar='<n>', nargs=1, default=None, type=int,
                                help='number of jobs to use running commands in parallel')),
        # (['--timestamp', '-t'], dict(choices=CLOWDER_CONTROLLER.project_names,
        #                              default=None, nargs=1, metavar='<timestamp>',
        #                              help='project to reset timestamps relative to'))
    ])


@network_connection_required
@valid_clowder_yaml_required
@print_clowder_name
@print_clowder_repo_status_fetch
def reset(args) -> None:
    """Clowder reset command private implementation"""

    timestamp_project = None
    # if args.timestamp:
    #     timestamp_project = args.timestamp[0]

    jobs = None
    if args.jobs:
        jobs = args.jobs[0]

    _reset_impl(args.projects, timestamp_project=timestamp_project, jobs=jobs)


def _reset_impl(project_names: List[str], timestamp_project: Optional[str] = None, jobs: Optional[int] = None) -> None:
    """Reset project branches to upstream or checkout tag/sha as detached HEAD

    :param List[str] project_names: Project names to reset
    :param Optional[str] timestamp_project: Reference project to checkout other project commit timestamps relative to
    :param Optional[int] jobs: Number of jobs to use running commands in parallel
    """

    config = Config()

    jobs_config = config.jobs
    jobs = jobs_config if jobs_config is not None else jobs

    projects = config.process_projects_arg(project_names)
    projects = CLOWDER_CONTROLLER.filter_projects(CLOWDER_CONTROLLER.projects, projects)

    if jobs is not None and jobs != 1 and os.name == "posix":
        if jobs <= 0:
            jobs = 4
        parallel.reset(projects, jobs, timestamp_project)
        return

    timestamp = None
    if timestamp_project:
        timestamp = CLOWDER_CONTROLLER.get_timestamp(timestamp_project)

    CLOWDER_CONTROLLER.validate_project_statuses(projects)
    for project in projects:
        project.reset(timestamp=timestamp)
