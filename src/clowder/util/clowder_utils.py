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

from .file_system import force_symlink

Parser = Union[argparse.ArgumentParser, argparse._MutuallyExclusiveGroup, argparse._ArgumentGroup] # noqa
Arguments = List[Tuple[list, dict]]


def add_parser_arguments(parser: Parser, arguments: Arguments) -> None:
    """Add arguments to parser

    :param Parser parser: Parser to add arguments to
    :param Arguments arguments: Arguments to add to parser
    """

    for argument in arguments:
        parser.add_argument(*argument[0], **argument[1])


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
    """

    if CLOWDER_REPO_VERSIONS_DIR is None:
        return None

    return tuple(sorted([v[:-13] for v in os.listdir(str(CLOWDER_REPO_VERSIONS_DIR)) if v.endswith('.clowder.yaml')]))


def link_clowder_yaml(clowder_dir: Path, version: Optional[str] = None) -> None:
    """Create symlink pointing to clowder.yaml file

    :param Path clowder_dir: Directory to create symlink in
    :param Optional[str] version: Version name of clowder.yaml to link
    :raise ClowderExit:
    """

    if version is None:
        yaml_file = clowder_dir / '.clowder' / 'clowder.yaml'
        path_output = fmt.path_string(Path('.clowder/clowder.yaml'))
    else:
        relative_path = Path('.clowder', 'versions', f'{version}.clowder.yaml')
        path_output = fmt.path_string(relative_path)
        yaml_file = clowder_dir.joinpath(relative_path)

    if not yaml_file.is_file():
        print(f"\n{path_output} doesn't seem to exist\n")
        raise ClowderExit(1)

    print(f' - Symlink {path_output}')
    force_symlink(yaml_file, clowder_dir / 'clowder.yaml')


def print_parallel_projects_output(projects: Tuple[Project, ...]) -> None:
    """Print output for parallel project command

    :param Tuple[Project, ...] projects: Projects to print output for
    """

    for project in projects:
        print(project.status())
        _print_fork_output(project)


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
