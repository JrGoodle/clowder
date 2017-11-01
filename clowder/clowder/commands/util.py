# -*- coding: utf-8 -*-
"""Clowder command utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import sys

import clowder.util.formatting as fmt


def existing_branch_groups(groups, branch, is_remote):
    """Checks if given branch exists in any project

    :param list(Group) groups: Groups to check
    :param str branch: Branch to check for
    :param bool is_remote: Check for remote branch
    :return: True, if at least one branch exists
    :rtype: bool
    """

    return any([p.existing_branch(branch, is_remote=is_remote) for g in groups for p in g.projects])


def existing_branch_projects(projects, branch, is_remote):
    """Checks if given branch exists in any project

    :param list(Project) projects: Projects to check
    :param str branch: Branch to check for
    :param bool is_remote: Check for remote branch
    :return: True, if at least one branch exists
    :rtype: bool
    """

    return any([p.existing_branch(branch, is_remote=is_remote) for p in projects])


def filter_groups(groups, group_names):
    """Filter groups based on given group names

    :param list(Group) groups: Groups to filter
    :param list(str) group_names: Group names to match against
    :return: List of groups in groups matching given names
    :rtype: list(Group)
    """

    return [g for g in groups if g.name in group_names]


def filter_projects_on_project_names(groups, project_names):
    """Filter projects based on given project names

    :param list(Group) groups: Groups to filter
    :param list(str) project_names: Project names to match against
    :return: List of projects in groups matching given names
    :rtype: list(Project)
    """

    return [p for g in groups for p in g.projects if p.name in project_names]


def filter_projects_on_group_names(groups, group_names):
    """Filter projects based on given group names

    :param list(Group) groups: Groups to filter
    :param list(str) group_names: Group names to match against
    :return: List of projects in groups matching given names
    :rtype: list(Project)
    """

    return [p for g in groups if g.name in group_names for p in g.projects]


def print_parallel_groups_output(groups, skip):
    """Print output for parallel group command

    :param list(Group) groups: Groups to print output for
    :param list(str) skip: Project names to skip
    """

    for group in groups:
        print(fmt.group_name(group.name))
        print_parallel_projects_output(group.projects, skip)


def print_parallel_projects_output(projects, skip):
    """Print output for parallel project command

    :param list(Project) projects: Projects to print output for
    :param list(str) skip: Project names to skip
    """

    for project in projects:
        if project.name in skip:
            continue
        print(project.status())
        _print_fork_output(project)


def run_group_command(group, skip, command, *args, **kwargs):
    """Run group command and print output

    :param Group group: Group to run command for
    :param list(str) skip: Project names to skip
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


def run_project_command(project, skip, command, *args, **kwargs):
    """Run project command and print output

    :param Praject project: Project to run command for
    :param list(str) skip: Project names to skip
    :param str command: Name of method to invoke
    :param args: List of arguments to pass to method invocation
    :param kwargs: Dict of arguments to pass to method invocation
    """

    print(project.status())
    if project.name in skip:
        print(fmt.skip_project_message())
        return
    getattr(project, command)(*args, **kwargs)


def validate_groups(groups):
    """Validate status of all projects for specified groups

    :param list(Group) groups: Groups to validate
    """

    for group in groups:
        group.print_validation()

    if not all([g.is_valid() for g in groups]):
        print()
        sys.exit(1)


def validate_projects(projects):
    """Validate status of all projects

    :param list(Project) projects: Projects to validate
    """

    if not all([p.is_valid() for p in projects]):
        print()
        sys.exit(1)


def validate_projects_exist(clowder):
    """Validate existence status of all projects for specified groups

    :param ClowderController clowder: ClowderController instance
    """

    projects_exist = True
    for group in clowder.groups:
        group.print_existence_message()
        if not group.existing_projects():
            projects_exist = False

    if not projects_exist:
        herd_output = fmt.clowder_command('clowder herd')
        print('\n - First run ' + herd_output + ' to clone missing projects\n')
        sys.exit(1)


def _print_fork_output(project):
    """Print fork output if a fork exists

    :param Project project: Project to print fork status for
    """

    if project.fork:
        print('  ' + fmt.fork_string(project.name))
        print('  ' + fmt.fork_string(project.fork.name))
