# -*- coding: utf-8 -*-
"""Clowder command line config controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.util.decorators import (
    print_clowder_name,
    valid_clowder_yaml_required
)
from clowder.config import Config, ClowderConfigType

from .util import add_parser_arguments


def add_config_parser(subparsers: argparse._SubParsersAction) -> None: # noqa
    """Add clowder config parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    parser = subparsers.add_parser('config', help='Manage clowder config (EXPERIMENTAL)')
    config_subparsers = parser.add_subparsers()

    add_config_clear_parser(config_subparsers)
    add_config_get_parser(config_subparsers)
    add_config_set_parser(config_subparsers)


def add_config_clear_parser(subparsers: argparse._SubParsersAction) -> None: # noqa
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

    # clowder config clear parallel
    parallel_parser = config_clear_subparsers.add_parser('parallel', help='Clear use parallel commands')
    parallel_parser.set_defaults(func=config_clear_parallel)

    # clowder config clear projects
    projects_parser = config_clear_subparsers.add_parser('projects', help='Clear default projects and groups')
    projects_parser.set_defaults(func=config_clear_projects)

    # clowder config clear protocol
    protocol_parser = config_clear_subparsers.add_parser('protocol', help='Clear default git protocol')
    protocol_parser.set_defaults(func=config_clear_protocol)


def add_config_get_parser(subparsers: argparse._SubParsersAction) -> None: # noqa
    """Add clowder config get parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    # clowder config get
    config_get_parser = subparsers.add_parser('get', help='Get clowder config options')
    config_get_parser.set_defaults(func=config_get_all)

    config_get_subparsers = config_get_parser.add_subparsers()

    # clowder config get rebase
    rebase_parser = config_get_subparsers.add_parser('rebase', help='Get use rebase with herd command')
    rebase_parser.set_defaults(func=config_get_rebase)

    # clowder config get parallel
    parallel_parser = config_get_subparsers.add_parser('parallel', help='Get use parallel commands')
    parallel_parser.set_defaults(func=config_get_parallel)

    # clowder config get projects
    projects_parser = config_get_subparsers.add_parser('projects', help='Get default projects and groups')
    projects_parser.set_defaults(func=config_get_projects)

    # clowder config get protocol
    protocol_parser = config_get_subparsers.add_parser('protocol', help='Get default git protocol')
    protocol_parser.set_defaults(func=config_get_protocol)


def add_config_set_parser(subparsers: argparse._SubParsersAction) -> None: # noqa
    """Add clowder config set parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    # clowder config set
    parser = subparsers.add_parser('set', help='Set clowder config options')
    config_set_subparsers = parser.add_subparsers()

    # clowder config set rebase
    rebase_parser = config_set_subparsers.add_parser('rebase', help='Set use rebase with herd command')
    rebase_parser.set_defaults(func=config_set_rebase)

    # clowder config set parallel
    parallel_parser = config_set_subparsers.add_parser('parallel', help='Set use parallel commands')
    parallel_parser.set_defaults(func=config_set_parallel)

    # clowder config set projects
    projects_arguments = [
        (['projects'], dict(metavar='PROJECT', nargs='+', choices=CLOWDER_CONTROLLER.project_choices,
                            help=fmt.options_help_message(CLOWDER_CONTROLLER.project_choices,
                                                          'Default projects and groups to run commands for')))
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
def config_clear_all(args) -> None: # noqa
    """Clowder config clear all command entry point"""

    print(' - Clear all config values')
    config = Config(CLOWDER_CONTROLLER.name, CLOWDER_CONTROLLER.project_choices)
    config.current_clowder_config.clear()
    config.save()


@valid_clowder_yaml_required
@print_clowder_name
def config_clear_parallel(args) -> None: # noqa
    """Clowder config clear parallel command entry point"""

    print(' - Clear parallel config value')
    config = Config(CLOWDER_CONTROLLER.name, CLOWDER_CONTROLLER.project_choices)
    config.current_clowder_config.parallel = None
    config.save()
    print()
    config.current_clowder_config.print_configuration()


@valid_clowder_yaml_required
@print_clowder_name
def config_clear_projects(args) -> None: # noqa
    """Clowder config clear projects command entry point"""

    print(' - Clear projects config value')
    config = Config(CLOWDER_CONTROLLER.name, CLOWDER_CONTROLLER.project_choices)
    config.current_clowder_config.projects = None
    config.save()
    print()
    config.current_clowder_config.print_configuration()


@valid_clowder_yaml_required
@print_clowder_name
def config_clear_protocol(args) -> None: # noqa
    """Clowder config clear protocol command entry point"""

    print(' - Clear protocol config value')
    config = Config(CLOWDER_CONTROLLER.name, CLOWDER_CONTROLLER.project_choices)
    config.current_clowder_config.protocol = None
    config.save()
    print()
    config.current_clowder_config.print_configuration()


@valid_clowder_yaml_required
@print_clowder_name
def config_clear_rebase(args) -> None: # noqa
    """Clowder config clear rebase command entry point"""

    print(' - Clear rebase config value')
    config = Config(CLOWDER_CONTROLLER.name, CLOWDER_CONTROLLER.project_choices)
    config.current_clowder_config.rebase = None
    config.save()
    print()
    config.current_clowder_config.print_configuration()


@valid_clowder_yaml_required
@print_clowder_name
def config_get_all(args) -> None: # noqa
    """Clowder config get all command entry point"""

    print(' - Get all config values\n')
    config = Config(CLOWDER_CONTROLLER.name, CLOWDER_CONTROLLER.project_choices)
    config.current_clowder_config.print_configuration()


@valid_clowder_yaml_required
@print_clowder_name
def config_get_parallel(args) -> None: # noqa
    """Clowder config get parallel command entry point"""

    print(' - Get parallel config value')
    config = Config(CLOWDER_CONTROLLER.name, CLOWDER_CONTROLLER.project_choices)
    config.current_clowder_config.print_config_value(ClowderConfigType.PARALLEL)


@valid_clowder_yaml_required
@print_clowder_name
def config_get_projects(args) -> None: # noqa
    """Clowder config get projects command entry point"""

    print(' - Get projects config value')
    config = Config(CLOWDER_CONTROLLER.name, CLOWDER_CONTROLLER.project_choices)
    config.current_clowder_config.print_config_value(ClowderConfigType.PROJECTS)


@valid_clowder_yaml_required
@print_clowder_name
def config_get_protocol(args) -> None: # noqa
    """Clowder config get protocol command entry point"""

    print(' - Get protocol config value')
    config = Config(CLOWDER_CONTROLLER.name, CLOWDER_CONTROLLER.project_choices)
    config.current_clowder_config.print_config_value(ClowderConfigType.PROTOCOL)


@valid_clowder_yaml_required
@print_clowder_name
def config_get_rebase(args) -> None: # noqa
    """Clowder config get rebase command entry point"""

    print(' - Get rebase config value')
    config = Config(CLOWDER_CONTROLLER.name, CLOWDER_CONTROLLER.project_choices)
    config.current_clowder_config.print_config_value(ClowderConfigType.REBASE)


@valid_clowder_yaml_required
@print_clowder_name
def config_set_parallel(args) -> None: # noqa
    """Clowder config set parallel command entry point"""

    print(' - Set parallel config value')
    config = Config(CLOWDER_CONTROLLER.name, CLOWDER_CONTROLLER.project_choices)
    config.current_clowder_config.parallel = True
    config.save()
    print()
    config.current_clowder_config.print_configuration()


@valid_clowder_yaml_required
@print_clowder_name
def config_set_projects(args) -> None:
    """Clowder config set projects command entry point"""

    print(' - Set projects config value')
    config = Config(CLOWDER_CONTROLLER.name, CLOWDER_CONTROLLER.project_choices)
    config.current_clowder_config.projects = tuple(args.projects)
    config.save()
    print()
    config.current_clowder_config.print_configuration()


@valid_clowder_yaml_required
@print_clowder_name
def config_set_protocol(args) -> None:
    """Clowder config set protocol command entry point"""

    print(' - Set protocol config value')
    config = Config(CLOWDER_CONTROLLER.name, CLOWDER_CONTROLLER.project_choices)
    config.current_clowder_config.protocol = args.protocol
    config.save()
    print()
    config.current_clowder_config.print_configuration()


@valid_clowder_yaml_required
@print_clowder_name
def config_set_rebase(args) -> None: # noqa
    """Clowder config set rebase command entry point"""

    print(' - Set rebase config value')
    config = Config(CLOWDER_CONTROLLER.name, CLOWDER_CONTROLLER.project_choices)
    config.current_clowder_config.rebase = True
    config.save()
    print()
    config.current_clowder_config.print_configuration()
