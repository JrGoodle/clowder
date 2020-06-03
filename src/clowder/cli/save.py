# -*- coding: utf-8 -*-
"""Clowder command line save controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse

import clowder.clowder_repo as clowder_repo
import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.environment import ENVIRONMENT
from clowder.error import ClowderError, ClowderErrorType
from clowder.model.util import validate_project_statuses
from clowder.util.decorators import (
    clowder_repo_required,
    print_clowder_name,
    valid_clowder_yaml_required
)
from clowder.util.file_system import make_dir
from clowder.util.yaml import save_yaml_file

from .util import add_parser_arguments


def add_save_parser(subparsers: argparse._SubParsersAction) -> None: # noqa

    arguments = [
        (['version'], dict(help='version to save', metavar='<version>'))
    ]

    parser = subparsers.add_parser('save', help='Create clowder yaml version for current repos')
    parser.formatter_class = argparse.RawTextHelpFormatter
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=save)


@valid_clowder_yaml_required
@print_clowder_name
@clowder_repo_required
def save(args) -> None:
    """Clowder save command private implementation

    :raise ClowderError:
    """

    if args.version.lower() == 'default':
        raise ClowderError(ClowderErrorType.SAVE_DEFAULT_VERSION, fmt.error_save_default(args.version))

    clowder_repo.print_status()
    CLOWDER_CONTROLLER.validate_projects_exist()
    validate_project_statuses(CLOWDER_CONTROLLER.projects)

    # TODO: Better validate version name (no spaces, no ~, etc.)
    # Replace path separators with dashes to avoid creating directories
    version_name = args.version.lower().replace('/', '-')

    versions_dir = ENVIRONMENT.clowder_repo_dir / 'versions'
    make_dir(versions_dir)

    yml_file = versions_dir / f"{version_name}.clowder.yml"
    yaml_file = versions_dir / f"{version_name}.clowder.yaml"
    if yml_file.exists():
        raise ClowderError(ClowderErrorType.VERSION_ALREADY_EXISTS,
                           fmt.error_save_version_exists(version_name, yml_file))
    elif yaml_file.exists():
        raise ClowderError(ClowderErrorType.VERSION_ALREADY_EXISTS,
                           fmt.error_save_version_exists(version_name, yaml_file))

    print(fmt.save_version_message(version_name, yml_file))
    save_yaml_file(CLOWDER_CONTROLLER.get_yaml(), yml_file)
