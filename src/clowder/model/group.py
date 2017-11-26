# -*- coding: utf-8 -*-
"""Representation of clowder.yaml group

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import clowder.util.formatting as fmt
from clowder.git.util import existing_git_repository
from clowder.model.project import Project


class Group(object):
    """clowder.yaml Group model class

    :ivar str name: Group name
    :ivar int depth: Group depth default
    :ivar bool recursive: Group recursive default
    :ivar str timestamp_author: Group timestamp author default
    :ivar str ref: Group ref default
    :ivar str remote_name: Group remote name default
    :ivar Source source: Group source default
    :ivar list[Project] projects: List of group's projects
    """

    def __init__(self, group, defaults, sources):
        """Groups __init__

        :param dict group: Parsed YAML python object for group
        :param Defaults defaults: Defaults instance
        :param list[Source] sources: List of Source instances
        """

        self.name = group['name']
        self.depth = group.get('depth', defaults.depth)
        self.recursive = group.get('recursive', defaults.recursive)
        self.timestamp_author = group.get('timestamp_author', defaults.timestamp_author)
        self.ref = group.get('ref', defaults.ref)
        self.remote_name = group.get('remote', defaults.remote)
        source_name = group.get('source', defaults.source)

        for source in sources:
            if source.name == source_name:
                self.source = source

        self.projects = [Project(p, group, defaults, sources) for p in group['projects']]
        self.projects.sort(key=lambda p: p.path)

    def existing_branch(self, branch, is_remote):
        """Checks if given branch exists in any project

        :param str branch: Branch to check for
        :param bool is_remote: Check for remote branch
        :return: True, if at least one branch exists
        :rtype: bool
        """

        return any([p.existing_branch(branch, is_remote=is_remote) for p in self.projects])

    def existing_projects(self):
        """Validate existence status of all projects

        :return: True, if all projects exist
        :rtype: bool
        """

        return all([existing_git_repository(project.full_path()) for project in self.projects])

    def get_yaml(self, resolved=False):
        """Return python object representation of model objects

        .. py:function:: get_yaml(self, resolved=False)

        :param Optional[bool] resolved: Whether to return resolved yaml
        :return: YAML python object
        :rtype: dict
        """

        if not resolved:
            return {'name': self.name,
                    'projects': [p.get_yaml() for p in self.projects]}

        group = {'name': self.name,
                 'depth': self.depth,
                 'ref': self.ref,
                 'recursive': self.recursive,
                 'remote': self.remote_name,
                 'source': self.source.name,
                 'projects': [p.get_yaml(resolved=True) for p in self.projects]}

        if self.timestamp_author:
            group['timestamp_author'] = self.timestamp_author

        return group

    def is_dirty(self):
        """Check if group has at least one dirty project

        :return: True, if any project is dirty
        :rtype: bool
        """

        return any([project.is_dirty() for project in self.projects])

    def is_valid(self):
        """Validate status of all projects

        :return: True, if all projects are valid
        :rtype: bool
        """

        return all([project.is_valid() for project in self.projects])

    def print_existence_message(self):
        """Print existence validation message for projects in group"""

        if self.existing_projects():
            return

        print(fmt.group_name(self.name))
        for project in self.projects:
            if not existing_git_repository(project.full_path()):
                print(project.status())
                existing_git_repository(project.full_path())

    def print_validation(self):
        """Print validation message for projects in group"""

        if self.is_valid():
            return

        print(fmt.group_name(self.name))
        for project in self.projects:
            project.print_validation()
