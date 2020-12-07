"""Clowder command line config controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import argparse

from pygoodle.app import Argument, Subcommand
from pygoodle.console import CONSOLE

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER, print_clowder_name, valid_clowder_yaml_required
from clowder.config import Config, print_config
from clowder.git import GitProtocol


class ConfigGetCommand(Subcommand):

    name = 'get'
    help = 'Get clowder config options'

    @valid_clowder_yaml_required
    @print_clowder_name
    @print_config
    def run(self, args) -> None:
        pass


class ConfigSetJobsCommand(Subcommand):

    name = 'jobs'
    help = 'Set default number of jobs for relevant commands'
    args = [
        Argument(
            'jobs',
            metavar='<n>',
            nargs=1,
            default=None,
            type=int,
            help='Set default number of jobs to use running commands in parallel'
        )
    ]

    @valid_clowder_yaml_required
    @print_clowder_name
    @print_config
    def run(self, args) -> None:
        CONSOLE.stdout(' - Set jobs config value')
        config = Config()
        config.jobs = args.jobs[0]
        config.save()


class ConfigSetProjectsCommand(Subcommand):

    name = 'projects'
    help = 'Set default projects and groups'
    args = [
        Argument(
            'projects',
            metavar='<project|group>',
            nargs='+',
            choices=CLOWDER_CONTROLLER.project_choices,
            help=fmt.project_options_help_message('Default projects and groups to run commands for')
        )
    ]

    @valid_clowder_yaml_required
    @print_clowder_name
    @print_config
    def run(self, args) -> None:
        CONSOLE.stdout(' - Set projects config value')
        config = Config()
        config.projects = tuple(args.projects)
        config.save()


class ConfigSetProtocolCommand(Subcommand):

    name = 'protocol'
    help = 'Set default git protocol'
    protocol_choices = ('https', 'ssh')
    args = [
        Argument(
            'protocol',
            metavar='<protocol>"',
            nargs=1,
            choices=protocol_choices,
            help=fmt.options_help_message(protocol_choices, 'Default git protocol to use'))
    ]

    @valid_clowder_yaml_required
    @print_clowder_name
    @print_config
    def run(self, args) -> None:
        CONSOLE.stdout(' - Set protocol config value')
        config = Config()
        config.protocol = GitProtocol(args.protocol[0])
        config.save()


class ConfigSetRebaseCommand(Subcommand):

    name = 'rebase'
    help = 'Set use rebase with herd command'

    @valid_clowder_yaml_required
    @print_clowder_name
    @print_config
    def run(self, args) -> None:
        CONSOLE.stdout(' - Set rebase config value')
        config = Config()
        config.rebase = True
        config.save()


class ConfigSetCommand(Subcommand):

    name = 'set'
    help = 'Set clowder config options'
    subcommands = [
        ConfigSetJobsCommand(),
        ConfigSetRebaseCommand(),
        ConfigSetProjectsCommand(),
        ConfigSetProtocolCommand()
    ]

    def run(self, args) -> None:
        pass


class ConfigCommand(Subcommand):

    name = 'config'
    help = 'Manage clowder config (EXPERIMENTAL)'
    subcommands = [
        ConfigSetCommand(),
        ConfigGetCommand()
    ]

    def run(self, args) -> None:
        pass


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
