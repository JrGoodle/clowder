# -*- coding: utf-8 -*-
"""Representation of clowder.yaml fork

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import os

from termcolor import colored

from clowder import ROOT_DIR
from clowder.git.project_repo import ProjectRepo
from clowder.git.util import (
    existing_git_repository,
    format_project_ref_string,
    format_project_string,
    git_url
)


class Fork(object):
    """clowder.yaml Project model class

    :ivar str name: Project name
    :ivar str path: Project relative path
    :ivar str remote_name: Git remote name
    """

    def __init__(self, fork, path, source, protocol):
        """Project __init__

        :param dict fork: Parsed YAML python object for fork
        :param str path: Fork relative path
        :param Source source: Source instance
        :param str protocol: Git protocol ('ssh' or 'https')
        """

        self.path = path
        self.name = fork['name']
        self.remote_name = fork['remote']
        self._source = source
        self._protocol = protocol

    def full_path(self):
        """Return full path to project

        :return: Project's full file path
        :rtype: str
        """

        return os.path.join(ROOT_DIR, self.path)

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

        if not existing_git_repository(self.path):
            return colored(self.path, 'green')

        repo = ProjectRepo(self.full_path(), self.remote_name, 'refs/heads/master')
        project_output = format_project_string(repo, self.path)
        current_ref_output = format_project_ref_string(repo)
        return project_output + ' ' + current_ref_output

    def url(self, protocol):
        """Return project url

        :param str protocol: Git protocol ('ssh' or 'https')
        """

        if protocol:
            return git_url(protocol, self._source.url, self.name)

        return git_url(self._protocol, self._source.url, self.name)
