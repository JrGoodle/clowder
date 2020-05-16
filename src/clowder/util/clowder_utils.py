# -*- coding: utf-8 -*-
"""Clowder command line utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os
from typing import List, Optional

import clowder.util.formatting as fmt
from clowder import CLOWDER_REPO_VERSIONS_DIR
from clowder.error.clowder_exit import ClowderExit
from clowder.model.project import Project
from clowder.util.file_system import force_symlink


def existing_branch_projects(projects: List[Project], branch: str, is_remote: bool) -> bool:
    """Checks if given branch exists in any project

    :param list[Project] projects: Projects to check
    :param str branch: Branch to check for
    :param bool is_remote: Check for remote branch
    :return: True, if at least one branch exists
    :rtype: bool
    """

    return any([p.existing_branch(branch, is_remote=is_remote) for p in projects])


def filter_projects(projects: List[Project], project_names: List[str]) -> List[Project]:
    """Filter projects based on given project or group names

    :param list[Project] projects: Projects to filter
    :param list[str] project_names: Project names to match against
    :return: List of projects in groups matching given names
    :rtype: list[Project]
    """

    filtered_projects = []
    for name in project_names:
        filtered_projects += [p for p in projects if name in p.groups]
    return list(set(filtered_projects))


def get_saved_version_names() -> Optional[List[str]]:
    """Return list of all saved versions

    :return: List of all saved version names
    :rtype: Optional[list[str]]
    """

    if CLOWDER_REPO_VERSIONS_DIR is None:
        return None

    return [v[:-13] for v in os.listdir(CLOWDER_REPO_VERSIONS_DIR) if v.endswith('.clowder.yaml')]


def link_clowder_yaml(clowder_dir: str, version: Optional[str] = None) -> None:
    """Create symlink pointing to clowder.yaml file

    :param str clowder_dir: Directory to create symlink in
    :param Optional[str] version: Version name of clowder.yaml to link
    :raise ClowderExit:
    """

    if version is None:
        yaml_file = os.path.join(clowder_dir, '.clowder', 'clowder.yaml')
        path_output = fmt.path_string('.clowder/clowder.yaml')
    else:
        relative_path = os.path.join('.clowder', 'versions', f'{version}.clowder.yaml')
        path_output = fmt.path_string(relative_path)
        yaml_file = os.path.join(clowder_dir, relative_path)

    if not os.path.isfile(yaml_file):
        print(f"\n{path_output} doesn't seem to exist\n")
        raise ClowderExit(1)

    print(f' - Symlink {path_output}')
    force_symlink(yaml_file, os.path.join(clowder_dir, 'clowder.yaml'))


def options_help_message(options: List[str], message: str) -> str:
    """Help message for groups option

    :param list[str] options: List of options
    :param str message: Help message
    :return: Formatted options help message
    :rtype: str
    """

    if options == [''] or options is None or options == [] or not all(isinstance(n, str) for n in options):
        return message

    help_message = '''
                   {0}:
                   {1}
                   '''

    return help_message.format(message, ', '.join(options))


def print_parallel_projects_output(projects: List[Project]) -> None:
    """Print output for parallel project command

    :param list[Project] projects: Projects to print output for
    """

    for project in projects:
        print(project.status())
        _print_fork_output(project)


def validate_projects(projects: List[Project]) -> None:
    """Validate status of all projects

    :param list[Project] projects: Projects to validate
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
