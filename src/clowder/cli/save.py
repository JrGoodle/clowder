# -*- coding: utf-8 -*-
"""Clowder command line save controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse

import clowder.clowder_repo as clowder_repo
import clowder.util.formatting as fmt
from clowder import CLOWDER_REPO_DIR
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.error import ClowderExit
from clowder.model.util import validate_project_statuses
from clowder.util.decorators import (
    print_clowder_name,
    valid_clowder_yaml_required
)
from clowder.util.file_system import make_dir
from clowder.util.yaml import save_yaml

from .util import add_parser_arguments


def add_save_parser(subparsers: argparse._SubParsersAction) -> None: # noqa

    arguments = [
        (['version'], dict(help='version to save', metavar='VERSION'))
    ]

    parser = subparsers.add_parser('save', help='Create clowder yaml version for current repos')
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=save)


@valid_clowder_yaml_required
@print_clowder_name
def save(args) -> None:
    """Clowder save command private implementation

    :raise ClowderExit:
    """

    if args.version.lower() == 'default':
        print(fmt.error_save_default(args.version))
        raise ClowderExit(1)

    clowder_repo.print_status()
    CLOWDER_CONTROLLER.validate_projects_exist()
    # TODO: Get all projects
    validate_project_statuses(CLOWDER_CONTROLLER.projects)

    # TODO: Better validate version name (no spaces, no ~, etc.)
    # Replace path separators with dashes to avoid creating directories
    version_name = args.version.replace('/', '-')

    versions_dir = CLOWDER_REPO_DIR / 'versions'
    make_dir(versions_dir)

    yml_file = versions_dir / f"{version_name}.clowder.yml"
    yaml_file = versions_dir / f"{version_name}.clowder.yaml"
    if yml_file.exists():
        print(f"{fmt.error_save_version_exists(version_name, yml_file)}\n")
        raise ClowderExit(1)
    elif yaml_file.exists():
        print(f"{fmt.error_save_version_exists(version_name, yaml_file)}\n")
        raise ClowderExit(1)

    print(fmt.save_version_message(version_name, yml_file))
    save_yaml(CLOWDER_CONTROLLER.get_yaml(), yml_file)
