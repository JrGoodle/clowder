# -*- coding: utf-8 -*-
"""Clowder command line save controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse
import os

import clowder.clowder_repo as clowder_repo
import clowder.util.formatting as fmt
from clowder import CLOWDER_REPO_DIR
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.error import ClowderExit
from clowder.util.clowder_utils import (
    add_parser_arguments,
    validate_projects
)
from clowder.util.decorators import valid_clowder_yaml_required
from clowder.util.file_system import make_dir
from clowder.util.yaml import save_yaml


def add_save_parser(subparsers: argparse._SubParsersAction) -> None: # noqa

    arguments = [
        (['version'], dict(help='version to save', metavar='VERSION'))
    ]

    parser = subparsers.add_parser('save', help='Create version of clowder.yaml for current repos')
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=save)


def save(args) -> None:
    """Clowder save command entry point"""

    _save(args)


@valid_clowder_yaml_required
def _save(args) -> None:
    """Clowder save command private implementation

    :raise ClowderExit:
    """

    if args.version.lower() == 'default':
        print(fmt.error_save_default(args.version))
        raise ClowderExit(1)

    clowder_repo.print_status()
    CLOWDER_CONTROLLER.validate_projects_exist()
    # TODO: Get all projects
    validate_projects(CLOWDER_CONTROLLER.projects)

    # Replace path separators with dashes to avoid creating directories
    version_name = args.version.replace('/', '-')

    versions_dir = os.path.join(CLOWDER_REPO_DIR, 'versions')
    make_dir(versions_dir)

    yaml_file = os.path.join(versions_dir, f"{version_name}.clowder.yaml")
    if os.path.exists(yaml_file):
        print(f"{fmt.error_save_version_exists(version_name, yaml_file)}\n")
        raise ClowderExit(1)

    print(fmt.save_version_message(version_name, yaml_file))
    save_yaml(CLOWDER_CONTROLLER.get_yaml(), yaml_file)
