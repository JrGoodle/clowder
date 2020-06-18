# -*- coding: utf-8 -*-
"""Clowder command line herd controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse
import os

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.config import Config
from clowder.model.util import (
    filter_projects,
    validate_project_statuses
)
from clowder.util.connectivity import network_connection_required
from clowder.util.decorators import (
    print_clowder_name,
    print_clowder_repo_status_fetch,
    valid_clowder_yaml_required
)
from clowder.util.parallel import herd_parallel

from .util import add_parser_arguments


def add_herd_parser(subparsers: argparse._SubParsersAction) -> None: # noqa
    """Add clowder herd parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    arguments = [
        (['projects'], dict(metavar='<project|group>', default='default', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices_with_default,
                            help=fmt.project_options_help_message('projects and groups to show branches for'))),
        (['--jobs', '-j'], dict(metavar='<n>', nargs=1, default=None, type=int,
                                help='number of jobs to use runnning commands in parallel')),
        (['--rebase', '-r'], dict(action='store_true', help='use rebase instead of pull')),
        (['--depth', '-d'], dict(default=None, type=int, nargs=1, metavar='<n>', help='depth to herd')),
        (['--protocol', '-p'], dict(default=None, nargs=1, metavar='<protocol>', choices=('ssh', 'https'),
                                    help='git protocol to use for cloning'))
    ]

    parser = subparsers.add_parser('herd', help='Clone and update projects with latest changes')
    parser.formatter_class = argparse.RawTextHelpFormatter
    add_parser_arguments(parser, arguments)

    mutually_exclusive_arguments = [
        (['--branch', '-b'], dict(nargs=1, default=None, metavar='<branch>', help='branch to herd if present')),
        (['--tag', '-t'], dict(nargs=1, default=None, metavar='<tag>', help='tag to herd if present'))
    ]
    mutually_exclusive_group = parser.add_mutually_exclusive_group()
    add_parser_arguments(mutually_exclusive_group, mutually_exclusive_arguments)

    parser.set_defaults(func=herd)


@valid_clowder_yaml_required
@print_clowder_name
@network_connection_required
@print_clowder_repo_status_fetch
def herd(args) -> None:
    """Clowder herd command private implementation"""

    branch = None if args.branch is None else args.branch[0]
    tag = None if args.tag is None else args.tag[0]
    depth = None if args.depth is None else args.depth[0]
    protocol = None if args.protocol is None else args.protocol[0]
    rebase = args.rebase

    config = Config(CLOWDER_CONTROLLER.name, CLOWDER_CONTROLLER.project_choices)

    rebase_config = config.current_clowder_config.rebase
    rebase = rebase_config if rebase_config is not None else rebase

    protocol_config = config.current_clowder_config.protocol
    protocol = protocol_config if protocol_config is not None else protocol
    for s in CLOWDER_CONTROLLER.sources:
        s.update_protocol(protocol)

    jobs = None
    if args.jobs:
        jobs = args.jobs[0]

    jobs_config = config.current_clowder_config.jobs
    jobs = jobs_config if jobs_config is not None else jobs

    projects = config.process_projects_arg(args.projects)
    projects = filter_projects(CLOWDER_CONTROLLER.projects, projects)

    if jobs is not None and jobs != 1 and os.name == "posix":
        if jobs <= 0:
            jobs = 4
        herd_parallel(projects, jobs, branch=branch, tag=tag, depth=depth, rebase=rebase)
        return

    validate_project_statuses(projects)
    for project in projects:
        project.herd(branch=branch, tag=tag, depth=depth, rebase=rebase)
