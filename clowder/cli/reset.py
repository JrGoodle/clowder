"""Clowder command line reset controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import os
from typing import Optional

from pygoodle.app import Argument, Subcommand
from pygoodle.connectivity import network_connection_required

import clowder.util.formatting as fmt
import clowder.util.parallel as parallel
from clowder.clowder_controller import CLOWDER_CONTROLLER, print_clowder_name, valid_clowder_yaml_required
from clowder.config import Config
from clowder.git.clowder_repo import print_clowder_repo_status_fetch


class ResetCommand(Subcommand):

    name = 'reset'
    help = 'Reset branches to upstream commits or check out detached HEADs for tags and shas'
    args = [
        Argument(
            'projects',
            metavar='<project|group>',
            default='default',
            nargs='*',
            choices=CLOWDER_CONTROLLER.project_choices_with_default,
            help=fmt.project_options_help_message('projects and groups to reset')
        ),
        Argument(
            '--jobs', '-j',
            metavar='<n>',
            nargs=1,
            default=None,
            type=int,
            help='number of jobs to use running commands in parallel')
        # Argument('--timestamp', '-t', choices=CLOWDER_CONTROLLER.project_names,
        #                              default=None, nargs=1, metavar='<timestamp>',
        #                              help='project to reset timestamps relative to')
    ]

    @network_connection_required
    @valid_clowder_yaml_required
    @print_clowder_name
    @print_clowder_repo_status_fetch
    def run(self, args) -> None:
        jobs = None
        if args.jobs:
            jobs = args.jobs[0]

        config = Config()

        jobs_config = config.jobs
        jobs = jobs_config if jobs_config is not None else jobs

        timestamp_project: Optional[str] = None
        # if args.timestamp:
        #     timestamp_project = args.timestamp[0]
        timestamp = None
        if timestamp_project:
            timestamp = CLOWDER_CONTROLLER.get_timestamp(timestamp_project)

        projects = config.process_projects_arg(args.projects)
        projects = CLOWDER_CONTROLLER.filter_projects(CLOWDER_CONTROLLER.projects, projects)

        if jobs is not None and jobs != 1 and os.name == "posix":
            if jobs <= 0:
                jobs = 4
            parallel.reset(projects, jobs, timestamp_project)
            return

        CLOWDER_CONTROLLER.validate_project_statuses(projects)
        for project in projects:
            project.reset(timestamp=timestamp)
