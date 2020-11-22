"""Clowder command line save controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import argparse

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER, print_clowder_name, valid_clowder_yaml_required
from clowder.util.console import CONSOLE
from clowder.environment import clowder_repo_required, ENVIRONMENT
from clowder.util.error import DefaultVersionError, ExistingVersionError
from clowder.git.clowder_repo import ClowderRepo
from clowder.util.file_system import make_dir
from clowder.util.yaml import save_yaml_file

from .util import add_parser_arguments


def add_save_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa

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

    :raise DefaultVersionError:
    :raise ExistingVersionError:
    """

    if args.version.lower() == 'default':
        raise DefaultVersionError(f"Version name '{args.version}' is not allowed")

    if ENVIRONMENT.clowder_repo_dir is not None:
        ClowderRepo(ENVIRONMENT.clowder_repo_dir).print_status()
    CLOWDER_CONTROLLER.validate_projects_exist()
    CLOWDER_CONTROLLER.validate_project_statuses(CLOWDER_CONTROLLER.projects)

    # TODO: Better validate version name (no spaces, no ~, etc.)
    # Replace path separators with dashes to avoid creating directories
    version_name = args.version.lower().replace('/', '-')

    versions_dir = ENVIRONMENT.clowder_repo_versions_dir
    if not versions_dir.exists():
        make_dir(versions_dir)

    yml_file = versions_dir / f"{version_name}.clowder.yml"
    yaml_file = versions_dir / f"{version_name}.clowder.yaml"
    version_exists_message = f"Version '{fmt.version(version_name)}' already exists"
    if yml_file.exists():
        raise ExistingVersionError(f"{fmt.path(yml_file)}\n{version_exists_message}")
    elif yaml_file.exists():
        raise ExistingVersionError(f"{fmt.path(yaml_file)}\n{version_exists_message}")

    CONSOLE.stdout(f" - Save version '{fmt.version(version_name)}'\n{fmt.path(yml_file)}")
    save_yaml_file(CLOWDER_CONTROLLER.get_yaml(resolved=True), yml_file)
