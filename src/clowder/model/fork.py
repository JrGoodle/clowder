# -*- coding: utf-8 -*-
"""Representation of clowder.yaml fork

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os
from typing import List

from termcolor import colored

import clowder.util.formatting as fmt
from clowder import ROOT_DIR
from clowder.error.clowder_yaml_error import ClowderYAMLError, ClowderYAMLYErrorType
from clowder.git.project_repo import ProjectRepo
from clowder.git.util import (
    existing_git_repository,
    git_url
)
from clowder.model.defaults import Defaults
from clowder.model.source import Source


class Fork(object):
    """clowder.yaml Project model class

    :ivar str name: Project name
    :ivar str path: Project relative path
    :ivar str remote: Git remote name
    """

    def __init__(self, fork: dict, path: str, project_name: str, project_source: Source,
                 sources: List[Source], project_ref: str, recursive: bool, defaults: Defaults):
        """Project __init__

        :param dict fork: Parsed YAML python object for fork
        :param str path: Fork relative path
        :param str project_name: Parent project name
        :param Source project_source: Source instance from project
        :param list[Source] sources: List of Source instances
        :param str project_ref: Git ref from project
        :param bool recursive: Whether to handle submodules
        :param Defaults defaults: Defaults instance
        """

        self.path = path
        self.name = fork['name']
        self.remote = fork.get('remote', defaults.remote)
        self._ref = fork.get('ref', project_ref)
        self._recursive = recursive

        self._source = None
        source_name = fork.get('source', project_source.name)
        for s in sources:
            if s.name == source_name:
                self._source = s
        if self._source is None:
            # FIXME: This should be in validation
            raise ClowderYAMLError(fmt.source_not_found_error(source_name, project_name, fork=self.name),
                                   ClowderYAMLYErrorType.SOURCE_NOT_FOUND)

    def full_path(self) -> str:
        """Return full path to project

        :return: Project's full file path
        :rtype: str
        """

        return os.path.join(ROOT_DIR, self.path)

    def get_yaml(self) -> dict:
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: dict
        """

        # TODO: Should this be added for forks as well as projects?
        # if resolved:
        #     ref = self.ref
        # else:
        #     repo = ProjectRepo(self.full_path(), self.remote, self.ref)
        #     ref = repo.sha()

        return {'name': self.name,
                'remote': self.remote,
                'source': self._source.name,
                'ref': self._ref}

    def status(self) -> str:
        """Return formatted fork status

        :return: Formatted fork status
        :rtype: str
        """

        if not existing_git_repository(self.path):
            return colored(self.path, 'green')

        repo = ProjectRepo(self.full_path(), self.remote, self._ref)
        project_output = repo.format_project_string(self.path)
        current_ref_output = repo.format_project_ref_string()
        return project_output + ' ' + current_ref_output

    def url(self) -> str:
        """Return project url"""

        return git_url(self._source.protocol, self._source.url, self.name)
