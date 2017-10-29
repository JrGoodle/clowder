# -*- coding: utf-8 -*-
"""Representation of clowder.yaml fork

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import os

from termcolor import colored

from clowder.git.project_repo import ProjectRepo


class Fork(object):
    """clowder.yaml fork class"""

    def __init__(self, fork, root_directory, path, source):
        self.root_directory = root_directory
        self.path = path
        self.name = fork['name']
        self.remote_name = fork['remote']
        self.url = source.get_url_prefix() + self.name + ".git"

    def full_path(self):
        """Return full path to project

        :return: Project's full file path
        :rtype: str
        """

        return os.path.join(self.root_directory, self.path)

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
