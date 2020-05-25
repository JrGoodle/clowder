# -*- coding: utf-8 -*-
"""Clowder command line utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse
import os
from pathlib import Path
from typing import List, Optional, Tuple, Union

import clowder.util.formatting as fmt
from clowder import CLOWDER_REPO_VERSIONS_DIR
from clowder.error import ClowderExit
from clowder.model import Project

from .file_system import (
    force_symlink,
    remove_file
)

Parser = Union[argparse.ArgumentParser, argparse._MutuallyExclusiveGroup, argparse._ArgumentGroup] # noqa
Arguments = List[Tuple[list, dict]]


def add_parser_arguments(parser: Parser, arguments: Arguments) -> None:
    """Add arguments to parser

    :param Parser parser: Parser to add arguments to
    :param Arguments arguments: Arguments to add to parser
    """

    for argument in arguments:
        parser.add_argument(*argument[0], **argument[1])


# TODO: Update to return list of all duplicates found
def check_for_duplicates(list_of_elements: List[str]) -> Optional[str]:
    """Check if given list contains any duplicates

    :param List[str] list_of_elements: List of strings to check for duplicates
    :return: First duplicate encountered, or None if no duplicates found
    :rtype: Optional[str]
    """

    set_of_elements = set()
    for elem in list_of_elements:
        if elem in set_of_elements:
            return elem
        else:
            set_of_elements.add(elem)
    return None


def existing_branch_projects(projects: Tuple[Project, ...], branch: str, is_remote: bool) -> bool:
    """Checks if given branch exists in any project

    :param Tuple[Project, ...] projects: Projects to check
    :param str branch: Branch to check for
    :param bool is_remote: Check for remote branch
    :return: True, if at least one branch exists
    :rtype: bool
    """

    return any([p.existing_branch(branch, is_remote=is_remote) for p in projects])


def filter_projects(projects: Tuple[Project, ...], project_names: Tuple[str, ...]) -> Tuple[Project, ...]:
    """Filter projects based on given project or group names

    :param Tuple[Project, ...] projects: Projects to filter
    :param Tuple[str, ...] project_names: Project names to match against
    :return: Projects in groups matching given names
    :rtype: Tuple[Project, ...]
    """

    filtered_projects = []
    for name in project_names:
        filtered_projects += [p for p in projects if name in p.groups]
    return tuple(sorted(set(filtered_projects), key=lambda project: project.name))


def get_saved_version_names() -> Optional[Tuple[str, ...]]:
    """Return list of all saved versions

    :return: All saved version names
    :rtype: Optional[Tuple[str, ...]]
    :raise ClowderExit:
    """

    if CLOWDER_REPO_VERSIONS_DIR is None:
        return None

    versions = [Path(Path(v).stem).stem for v in os.listdir(str(CLOWDER_REPO_VERSIONS_DIR))
                if v.endswith('.clowder.yml') or v.endswith('.clowder.yaml')]

    duplicate = check_for_duplicates(versions)
    if duplicate is not None:
        print(fmt.error_duplicate_version(duplicate))
        raise ClowderExit(1)

    return tuple(sorted(versions))


def link_clowder_yaml_default(clowder_dir: Path) -> None:
    """Create symlink pointing to clowder yaml file

    :param Path clowder_dir: Directory to create symlink in
    :raise ClowderExit:
    """

    yml_relative_path = Path('.clowder', 'clowder.yml')
    yml_absolute_path = clowder_dir / yml_relative_path
    yaml_relative_path = Path('.clowder', 'clowder.yaml')
    yaml_absolute_path = clowder_dir / yaml_relative_path

    if yml_absolute_path.is_file():
        relative_source_file = yml_relative_path
    elif yaml_absolute_path.is_file():
        relative_source_file = yaml_relative_path
    else:
        print(f"{fmt.ERROR} .clowder/clowder.yml doesn't seem to exist\n")
        raise ClowderExit(1)

    source_file = clowder_dir / relative_source_file
    target_file = clowder_dir / source_file.name

    print(f" - Symlink {fmt.path_string(Path(target_file.name))} -> {fmt.path_string(relative_source_file)}")

    force_symlink(source_file, clowder_dir / target_file)

    existing_file = None
    if target_file.suffix == '.yaml':
        file = clowder_dir / 'clowder.yml'
        if file.exists():
            existing_file = file
    elif target_file.suffix == '.yml':
        file = clowder_dir / 'clowder.yaml'
        if file.exists():
            existing_file = file

    if existing_file is not None:
        print(f" - Remove previously existing file {fmt.path_string(existing_file)}")
        try:
            remove_file(existing_file)
        except OSError as err:
            print(f"{fmt.ERROR} Failed to remove file {existing_file}")
            print(err)
            ClowderExit(1)


def link_clowder_yaml_version(clowder_dir: Path, version: str) -> None:
    """Create symlink pointing to clowder yaml file

    :param Path clowder_dir: Directory to create symlink in
    :param str version: Version name of clowder yaml file to link
    :raise ClowderExit:
    """

    yml_relative_path = Path('.clowder', 'versions', f'{version}.clowder.yml')
    yml_absolute_path = clowder_dir / yml_relative_path
    yaml_relative_path = Path('.clowder', 'versions', f'{version}.clowder.yaml')
    yaml_absolute_path = clowder_dir / yaml_relative_path

    if yml_absolute_path.is_file():
        relative_source_file = yml_relative_path
    elif yaml_absolute_path.is_file():
        relative_source_file = yaml_relative_path
    else:
        print(f"{fmt.ERROR} .clowder/versions/{version}.clowder.yml doesn't seem to exist\n")
        raise ClowderExit(1)

    source_file = clowder_dir / relative_source_file
    target_file = clowder_dir / remove_prefix(source_file.name, f"{version}.")

    print(f" - Symlink {fmt.path_string(Path(target_file.name))} -> {fmt.path_string(relative_source_file)}")

    force_symlink(source_file, target_file)

    existing_file = None
    if target_file.suffix == '.yaml':
        file = clowder_dir / 'clowder.yml'
        if file.exists():
            existing_file = file
    elif target_file.suffix == '.yml':
        file = clowder_dir / 'clowder.yaml'
        if file.exists():
            existing_file = file

    if existing_file is not None:
        print(f" - Remove previously existing file {fmt.path_string(existing_file)}")
        try:
            remove_file(existing_file)
        except OSError as err:
            print(f"{fmt.ERROR} Failed to remove file {existing_file}")
            print(err)
            ClowderExit(1)


def print_parallel_projects_output(projects: Tuple[Project, ...]) -> None:
    """Print output for parallel project command

    :param Tuple[Project, ...] projects: Projects to print output for
    """

    for project in projects:
        print(project.status())
        _print_fork_output(project)


def remove_prefix(text: str, prefix: str) -> str:
    """Remove prefix from string

    :param str text: Text to remove prefix from
    :param str prefix: Prefix to remoe
    :return: Text with prefix removed if present
    :rtype: str
    """

    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def validate_project_statuses(projects: Tuple[Project, ...]) -> None:
    """Validate status of all projects

    :param Tuple[Project, ...] projects: Projects to validate
    :raise ClowderExit:
    """

    for p in projects:
        p.print_validation()
    if not all([p.is_valid() for p in projects]):
        print()
        raise ClowderExit(1)


def _print_fork_output(project: Project) -> None:
    """Print fork output if a fork exists

    :param Project project: Project to print fork status for
    """

    if project.fork:
        print('  ' + fmt.fork_string(project.name))
        print('  ' + fmt.fork_string(project.fork.name))
