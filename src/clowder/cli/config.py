# -*- coding: utf-8 -*-
"""Clowder command line config controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse
from typing import Optional

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.util.decorators import (
    print_clowder_name,
    valid_clowder_yaml_required
)
from clowder.config import Config

from .util import add_parser_arguments


config_parser: Optional[argparse.ArgumentParser] = None
config_set_parser: Optional[argparse.ArgumentParser] = None


def add_config_parser(subparsers: argparse._SubParsersAction) -> None: # noqa
    """Add clowder config parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    global config_parser
    config_parser = subparsers.add_parser('config', help='Manage clowder config (EXPERIMENTAL)')
    config_parser.set_defaults(func=config_help)
    config_subparsers = config_parser.add_subparsers()

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

    # clowder config clear jobs
    jobs_parser = config_clear_subparsers.add_parser('jobs', help='Clear use jobs commands')
    jobs_parser.set_defaults(func=config_clear_jobs)

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


def add_config_set_parser(subparsers: argparse._SubParsersAction) -> None: # noqa
    """Add clowder config set parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    # clowder config set
    global config_set_parser
    config_set_parser = subparsers.add_parser('set', help='Set clowder config options')
    config_set_parser.set_defaults(func=config_help_set)
    config_set_subparsers = config_set_parser.add_subparsers()

    # clowder config set rebase
    rebase_parser = config_set_subparsers.add_parser('rebase', help='Set use rebase with herd command')
    rebase_parser.set_defaults(func=config_set_rebase)

    # clowder config set jobs
    jobs_parser = config_set_subparsers.add_parser('jobs', help='Set use jobs commands')
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
def config_clear_all(args) -> None: # noqa
    """Clowder config clear all command entry point"""

    print(' - Clear all config values')
    config = _config()
    config.current_clowder_config.clear()
    config.save()
    print()
    config.current_clowder_config.print_configuration()


@valid_clowder_yaml_required
@print_clowder_name
def config_clear_jobs(args) -> None: # noqa
    """Clowder config clear jobs command entry point"""

    print(' - Clear jobs config value')
    config = _config()
    config.current_clowder_config.jobs = None
    config.save()
    print()
    config.current_clowder_config.print_configuration()


@valid_clowder_yaml_required
@print_clowder_name
def config_clear_projects(args) -> None: # noqa
    """Clowder config clear projects command entry point"""

    print(' - Clear projects config value')
    config = _config()
    config.current_clowder_config.projects = None
    config.save()
    print()
    config.current_clowder_config.print_configuration()


@valid_clowder_yaml_required
@print_clowder_name
def config_clear_protocol(args) -> None: # noqa
    """Clowder config clear protocol command entry point"""

    print(' - Clear protocol config value')
    config = _config()
    config.current_clowder_config.protocol = None
    config.save()
    print()
    config.current_clowder_config.print_configuration()


@valid_clowder_yaml_required
@print_clowder_name
def config_clear_rebase(args) -> None: # noqa
    """Clowder config clear rebase command entry point"""

    print(' - Clear rebase config value')
    config = _config()
    config.current_clowder_config.rebase = None
    config.save()
    print()
    config.current_clowder_config.print_configuration()


@valid_clowder_yaml_required
@print_clowder_name
def config_get_all(args) -> None: # noqa
    """Clowder config get all command entry point"""

    config = _config(print_newline=False)
    config.current_clowder_config.print_configuration()


def config_help(args): # noqa
    """Clowder config help handler"""

    config_parser.print_help()


def config_help_set(args): # noqa
    """Clowder config set help handler"""

    config_set_parser.print_help()


@valid_clowder_yaml_required
@print_clowder_name
def config_set_jobs(args) -> None: # noqa
    """Clowder config set jobs command entry point"""

    print(' - Set jobs config value')
    config = _config()
    config.current_clowder_config.jobs = True
    config.save()
    print()
    config.current_clowder_config.print_configuration()


@valid_clowder_yaml_required
@print_clowder_name
def config_set_projects(args) -> None:
    """Clowder config set projects command entry point"""

    print(' - Set projects config value')
    config = _config()
    config.current_clowder_config.projects = tuple(args.projects)
    config.save()
    print()
    config.current_clowder_config.print_configuration()


@valid_clowder_yaml_required
@print_clowder_name
def config_set_protocol(args) -> None:
    """Clowder config set protocol command entry point"""

    print(' - Set protocol config value')
    config = _config()
    config.current_clowder_config.protocol = args.protocol[0]
    config.save()
    print()
    config.current_clowder_config.print_configuration()


@valid_clowder_yaml_required
@print_clowder_name
def config_set_rebase(args) -> None: # noqa
    """Clowder config set rebase command entry point"""

    print(' - Set rebase config value')
    config = _config()
    config.current_clowder_config.rebase = True
    config.save()
    print()
    config.current_clowder_config.print_configuration()


def _config(print_newline: bool = True) -> Config:
    """Get clowder Config instance

    :param bool print_newline: Whether to print a newline if an exception is thrown
    :return: Clowder Config instance
    :rtype: Config
    :raise Exception:
    """

    try:
        return Config(CLOWDER_CONTROLLER.name, CLOWDER_CONTROLLER.project_choices, raise_exceptions=True)
    except: # noqa
        if print_newline:
            print()
        raise
