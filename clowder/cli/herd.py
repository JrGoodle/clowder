"""Clowder command line herd controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import os

from pygoodle.app import Argument, Subcommand
from pygoodle.connectivity import network_connection_required

import clowder.util.formatting as fmt
import clowder.util.parallel as parallel
from clowder.clowder_controller import CLOWDER_CONTROLLER, print_clowder_name, valid_clowder_yaml_required
from clowder.config import Config
from clowder.data.source_controller import SOURCE_CONTROLLER
from clowder.git import GitProtocol
from clowder.git.clowder_repo import print_clowder_repo_status_fetch


class HerdCommand(Subcommand):

    name = 'herd'
    help = 'Clone and update projects with latest changes'
    args = [
        Argument(
            'projects',
            metavar='<project|group>',
            default='default',
            nargs='*',
            choices=CLOWDER_CONTROLLER.project_choices_with_default,
            help=fmt.project_options_help_message('projects and groups to herd')
        ),
        Argument(
            '--jobs', '-j',
            metavar='<n>',
            nargs=1,
            default=None,
            type=int,
            help='number of jobs to use running commands in parallel'
        ),
        Argument('--rebase', '-r', action='store_true', help='use rebase instead of pull'),
        Argument('--depth', '-d', default=None, type=int, nargs=1, metavar='<n>', help='depth to herd'),
        Argument(
            '--protocol', '-p',
            default=None,
            nargs=1,
            metavar='<protocol>',
            choices=('ssh', 'https'),
            help='git protocol to use for cloning')
    ]
    mutually_exclusive_args = [
        [
            Argument('--branch', '-b', nargs=1, default=None, metavar='<branch>', help='branch to herd if present'),
            Argument('--tag', '-t', nargs=1, default=None, metavar='<tag>', help='tag to herd if present')
        ]
    ]

    @valid_clowder_yaml_required
    @print_clowder_name
    @network_connection_required
    @print_clowder_repo_status_fetch
    def run(self, args) -> None:
        branch = None if args.branch is None else args.branch[0]
        tag = None if args.tag is None else args.tag[0]
        depth = None if args.depth is None else args.depth[0]
        protocol = None if args.protocol is None else GitProtocol(args.protocol[0])
        jobs = None if args.jobs is None else args.jobs[0]
        rebase = args.rebase

        config = Config()

        rebase_config = config.rebase
        rebase = rebase_config if rebase_config is not None else rebase

        protocol_config = config.protocol
        protocol = protocol_config if protocol_config is not None else protocol
        SOURCE_CONTROLLER.protocol_override = protocol

        jobs_config = config.jobs
        jobs = jobs_config if jobs_config is not None else jobs

        projects = config.process_projects_arg(args.projects)
        projects = CLOWDER_CONTROLLER.filter_projects(CLOWDER_CONTROLLER.projects, projects)

        if jobs is not None and jobs != 1 and os.name == "posix":
            if jobs <= 0:
                jobs = 4
            parallel.herd(projects, jobs, branch, tag, depth, rebase)
            return

        CLOWDER_CONTROLLER.validate_project_statuses(projects)
        for project in projects:
            project.herd(branch=branch, tag=tag, depth=depth, rebase=rebase)
