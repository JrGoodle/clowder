# -*- coding: utf-8 -*-
"""Representation of clowder.yaml fork

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import os

from termcolor import colored

from clowder.git.project_repo import ProjectRepo


class Fork(object):
    """clowder.yaml Project model class

    :ivar str name: Project name
    :ivar str path: Project relative path
    :ivar Fork fork: Project's associated Fork
    """

    def __init__(self, fork, root_directory, path, source):
        """Project __init__

        :param dict fork: Parsed YAML python object for fork
        :param str root_directory: Root directory of clowder projects
        :param str path: Fork relative path
        :param Source source: Source instance
        """

        self._root_directory = root_directory
        self.path = path
        self.name = fork['name']
        self.remote_name = fork['remote']
        self.url = source.get_url_prefix() + self.name + ".git"

    def full_path(self):
        """Return full path to project

        :return: Project's full file path
        :rtype: str
        """

        return os.path.join(self._root_directory, self.path)

    def get_yaml(self):
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: dict
        """

        return {'name': self.name, 'remote': self.remote_name}

    def status(self):
        """Return formatted fork status

        :return: Formatted fork status
        :rtype: str
        """

        if not ProjectRepo.existing_git_repository(self.path):
            return colored(self.path, 'green')

        project_output = ProjectRepo.format_project_string(self.path, self.path)
        current_ref_output = ProjectRepo.format_project_ref_string(self.full_path())
        return project_output + ' ' + current_ref_output
