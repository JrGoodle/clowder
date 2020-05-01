# -*- coding: utf-8 -*-
"""Clowder command line utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os
from typing import List, Optional

import clowder.util.formatting as fmt
from clowder import ROOT_DIR
from clowder.error.clowder_exit import ClowderExit
from clowder.model.group import Group
from clowder.model.project import Project
from clowder.util.file_system import force_symlink


def existing_branch_groups(groups: List[Group], branch: str, is_remote: bool) -> bool:
    """Checks if given branch exists in any project

    :param list[Group] groups: Groups to check
    :param str branch: Branch to check for
    :param bool is_remote: Check for remote branch
    :return: True, if at least one branch exists
    :rtype: bool
    """

    return any([p.existing_branch(branch, is_remote=is_remote) for g in groups for p in g.projects])


def existing_branch_projects(projects: List[Project], branch: str, is_remote: bool) -> bool:
    """Checks if given branch exists in any project

    :param list[Project] projects: Projects to check
    :param str branch: Branch to check for
    :param bool is_remote: Check for remote branch
    :return: True, if at least one branch exists
    :rtype: bool
    """

    return any([p.existing_branch(branch, is_remote=is_remote) for p in projects])


def filter_groups(groups: List[Group], names: List[str]) -> List[Group]:
    """Filter groups based on given group names

    :param list[Group] groups: Groups to filter
    :param list[str] names: Group names to match against
    :return: List of groups in groups matching given names
    :rtype: list[Group]
    """

    return [g for g in groups if g.name in names]


def filter_projects(groups: List[Group], group_names: List[str] = None,
                    project_names: List[str] = None) -> List[Project]:
    """Filter projects based on given project or group names

    :param list[Group] groups: Groups to filter
    :param list[str] group_names: Group names to match against
    :param list[str] project_names: Project names to match against
    :return: List of projects in groups matching given names
    :rtype: list[Project]
    """

    if project_names is not None:
        return [p for g in groups for p in g.projects if p.name in project_names]

    if group_names is not None:
        return [p for g in groups if g.name in group_names for p in g.projects]

    return []


def get_saved_version_names() -> Optional[List[str]]:
    """Return list of all saved versions

    :return: List of all saved version names
    :rtype: Optional[list[str]]
    """

    versions_dir = os.path.join(os.getcwd(), '.clowder', 'versions')
    if not os.path.exists(versions_dir):
        return None
    return [v for v in os.listdir(versions_dir) if not v.startswith('.') if v.lower() != 'default']


def link_clowder_yaml(version: Optional[str] = None) -> None:
    """Create symlink pointing to clowder.yaml file

    :param Optional[str] version: Version name of clowder.yaml to link
    :raise ClowderExit:
    """

    if version is None:
        yaml_file = os.path.join(ROOT_DIR, '.clowder', 'clowder.yaml')
        path_output = fmt.get_path('.clowder/clowder.yaml')
    else:
        relative_path = os.path.join('.clowder', 'versions', version, 'clowder.yaml')
        path_output = fmt.get_path(relative_path)
        yaml_file = os.path.join(ROOT_DIR, relative_path)

    if not os.path.isfile(yaml_file):
        print(f"\n{path_output} doesn't seem to exist\n")
        raise ClowderExit(1)

    yaml_symlink = os.path.join(ROOT_DIR, 'clowder.yaml')
    print(f' - Symlink {path_output}')
    force_symlink(yaml_file, yaml_symlink)


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


def print_parallel_groups_output(groups: List[Group], skip: List[str]) -> None:
    """Print output for parallel group command

    :param list[Group] groups: Groups to print output for
    :param list[str] skip: Project names to skip
    """

    for group in groups:
        print(fmt.group_name(group.name))
        print_parallel_projects_output(group.projects, skip)


def print_parallel_projects_output(projects: List[Project], skip: List[str]) -> None:
    """Print output for parallel project command

    :param list[Project] projects: Projects to print output for
    :param list[str] skip: Project names to skip
    """

    for project in projects:
        if project.name in skip:
            continue
        print(project.status())
        _print_fork_output(project)


def run_group_command(group: Group, skip: List[str], command: str, *args, **kwargs) -> None:
    """Run group command and print output

    :param Group group: Group to run command for
    :param list[str] skip: Project names to skip
    :param str command: Name of method to invoke
    :param args: List of arguments to pass to method invocation
    :param kwargs: Dict of arguments to pass to method invocation
    """

    print(fmt.group_name(group.name))
    for project in group.projects:
        print(project.status())
        if project.name in skip:
            print(fmt.skip_project_message())
            continue
        getattr(project, command)(*args, **kwargs)


def run_project_command(project: Project, skip: List[str], command: str, *args, **kwargs) -> None:
    """Run project command and print output

    :param Praject project: Project to run command for
    :param list[str] skip: Project names to skip
    :param str command: Name of method to invoke
    :param args: List of arguments to pass to method invocation
    :param kwargs: Dict of arguments to pass to method invocation
    """

    print(project.status())
    if project.name in skip:
        print(fmt.skip_project_message())
        return
    getattr(project, command)(*args, **kwargs)


def validate_groups(groups: List[Group]) -> None:
    """Validate status of all projects for specified groups

    :param list[Group] groups: Groups to validate
    :raise ClowderExit:
    """

    for group in groups:
        group.print_validation()

    if not all([g.is_valid() for g in groups]):
        print()
        raise ClowderExit(1)


def validate_projects(projects: List[Project]) -> None:
    """Validate status of all projects

    :param list[Project] projects: Projects to validate
    :raise ClowderExit:
    """

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
