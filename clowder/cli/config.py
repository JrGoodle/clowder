"""Clowder command line config controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import argparse

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER, print_clowder_name, valid_clowder_yaml_required
from clowder.config import Config, print_config
from clowder.git import GitProtocol
from clowder.util.console import CONSOLE

from .util import add_parser_arguments


def add_config_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa
    """Add clowder config parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    def config_help(_):
        """Clowder config help handler"""
        config_parser.print_help()

    config_parser = subparsers.add_parser('config', help='Manage clowder config (EXPERIMENTAL)')
    config_parser.set_defaults(func=config_help)
    config_subparsers = config_parser.add_subparsers()

    add_config_clear_parser(config_subparsers)
    add_config_get_parser(config_subparsers)
    add_config_set_parser(config_subparsers)


def add_config_clear_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa
    """Add clowder config clear parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    # clowder config clear
    config_clear_parser = subparsers.add_parser('clear', help='Clear clowder config options')
    config_clear_parser.set_defaults(func=config_clear_all)

    config_clear_subparsers = config_clear_parser.add_subparsers()

    # clowder config clear rebase
    rebase_parser = config_clear_subparsers.add_parser('rebase', help='Clear use rebase with herd command')
    rebase_parser.set_defaults(func=config_clear_rebase)

    # clowder config clear jobs
    jobs_parser = config_clear_subparsers.add_parser('jobs', help='Clear use jobs commands')
    jobs_parser.set_defaults(func=config_clear_jobs)

    # clowder config clear projects
    projects_parser = config_clear_subparsers.add_parser('projects', help='Clear default projects and groups')
    projects_parser.set_defaults(func=config_clear_projects)

    # clowder config clear protocol
    protocol_parser = config_clear_subparsers.add_parser('protocol', help='Clear default git protocol')
    protocol_parser.set_defaults(func=config_clear_protocol)


def add_config_get_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa
    """Add clowder config get parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    # clowder config get
    config_get_parser = subparsers.add_parser('get', help='Get clowder config options')
    config_get_parser.set_defaults(func=config_get_all)


def add_config_set_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa
    """Add clowder config set parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    def config_help_set(_):
        """Clowder config set help handler"""

        config_set_parser.print_help()

    # clowder config set
    config_set_parser = subparsers.add_parser('set', help='Set clowder config options')
    config_set_parser.set_defaults(func=config_help_set)
    config_set_subparsers = config_set_parser.add_subparsers()

    # clowder config set rebase
    rebase_parser = config_set_subparsers.add_parser('rebase', help='Set use rebase with herd command')
    rebase_parser.set_defaults(func=config_set_rebase)

    # clowder config set jobs
    jobs_arguments = [
        (['jobs'], dict(metavar='<n>', nargs=1, default=None, type=int,
                                help='Set default number of jobs to use running commands in parallel'))
    ]
    jobs_parser = config_set_subparsers.add_parser('jobs', help='Set default number of jobs for relevant commands')
    add_parser_arguments(jobs_parser, jobs_arguments)
    jobs_parser.set_defaults(func=config_set_jobs)

    # clowder config set projects
    projects_arguments = [
        (['projects'], dict(metavar='PROJECT', nargs='+', choices=CLOWDER_CONTROLLER.project_choices,
                            help=fmt.project_options_help_message('Default projects and groups to run commands for')))
    ]
    projects_parser = config_set_subparsers.add_parser('projects', help='Set default projects and groups')
    add_parser_arguments(projects_parser, projects_arguments)
    projects_parser.set_defaults(func=config_set_projects)

    # clowder config set protocol
    protocol_choices = ('https', 'ssh')
    protocol_arguments = [
        (['protocol'], dict(metavar='PROTOCOL', nargs=1, choices=protocol_choices,
                            help=fmt.options_help_message(protocol_choices, 'Default git protocol to use')))
    ]
    protocol_parser = config_set_subparsers.add_parser('protocol', help='Set default git protocol')
    add_parser_arguments(protocol_parser, protocol_arguments)
    protocol_parser.set_defaults(func=config_set_protocol)


@valid_clowder_yaml_required
@print_clowder_name
@print_config
def config_clear_all(_) -> None:
    """Clowder config clear all command entry point"""

    CONSOLE.stdout(' - Clear all config values')
    config = Config()
    config.clear()
    config.save()


@valid_clowder_yaml_required
@print_clowder_name
@print_config
def config_clear_jobs(_) -> None:
    """Clowder config clear jobs command entry point"""

    CONSOLE.stdout(' - Clear jobs config value')
    config = Config()
    config.jobs = None
    config.save()


@valid_clowder_yaml_required
@print_clowder_name
@print_config
def config_clear_projects(_) -> None:
    """Clowder config clear projects command entry point"""

    CONSOLE.stdout(' - Clear projects config value')
    config = Config()
    config.projects = None
    config.save()


@valid_clowder_yaml_required
@print_clowder_name
@print_config
def config_clear_protocol(_) -> None:
    """Clowder config clear protocol command entry point"""

    CONSOLE.stdout(' - Clear protocol config value')
    config = Config()
    config.protocol = None
    config.save()


@valid_clowder_yaml_required
@print_clowder_name
@print_config
def config_clear_rebase(_) -> None:
    """Clowder config clear rebase command entry point"""

    CONSOLE.stdout(' - Clear rebase config value')
    config = Config()
    config.rebase = None
    config.save()


@valid_clowder_yaml_required
@print_clowder_name
@print_config
def config_get_all(_) -> None:
    """Clowder config get all command entry point"""
    pass


@valid_clowder_yaml_required
@print_clowder_name
@print_config
def config_set_jobs(args) -> None:
    """Clowder config set jobs command entry point"""

    CONSOLE.stdout(' - Set jobs config value')
    config = Config()
    config.jobs = args.jobs[0]
    config.save()


@valid_clowder_yaml_required
@print_clowder_name
@print_config
def config_set_projects(args) -> None:
    """Clowder config set projects command entry point"""

    CONSOLE.stdout(' - Set projects config value')
    config = Config()
    config.projects = tuple(args.projects)
    config.save()


@valid_clowder_yaml_required
@print_clowder_name
@print_config
def config_set_protocol(args) -> None:
    """Clowder config set protocol command entry point"""

    CONSOLE.stdout(' - Set protocol config value')
    config = Config()
    config.protocol = GitProtocol(args.protocol[0])
    config.save()


@valid_clowder_yaml_required
@print_clowder_name
@print_config
def config_set_rebase(_) -> None:
    """Clowder config set rebase command entry point"""

    CONSOLE.stdout(' - Set rebase config value')
    config = Config()
    config.rebase = True
    config.save()
