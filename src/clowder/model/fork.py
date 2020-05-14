# -*- coding: utf-8 -*-
"""Representation of clowder.yaml fork

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os
from typing import List

from termcolor import colored

from clowder import ROOT_DIR
from clowder.git.project_repo import ProjectRepo
from clowder.git.util import (
    existing_git_repository,
    format_git_branch,
    format_git_tag,
    git_url
)
from clowder.model import Defaults
from clowder.model import Source
from clowder.model import Project


class Fork(object):
    """clowder.yaml Project model class

    :ivar str name: Project name
    :ivar str path: Project relative path
    :ivar str remote: Fork remote name
    :ivar str ref: Fork git ref
    """

    def __init__(self, fork: dict, project: Project, sources: List[Source], defaults: Defaults):
        """Project __init__

        :param dict fork: Parsed YAML python object for fork
        :param Project project: Parent project
        :param list[Source] sources: List of Source instances
        :param Defaults defaults: Defaults instance
        """

        self.path = project.path
        self.name = fork['name']
        self.remote = fork.get('remote', defaults.remote)
        self._recursive = project.recursive

        self._branch = fork.get("branch", None)
        self._tag = fork.get("tag", None)
        self._commit = fork.get("commit", None)

        if self._branch is not None:
            self.ref = format_git_branch(self._branch)
        elif self._tag is not None:
            self.ref = format_git_tag(self._tag)
        elif self._commit is not None:
            self.ref = self._commit
        else:
            self._branch = defaults.branch
            self._tag = defaults.tag
            self._commit = defaults.commit
            self.ref = defaults.ref

        self._source = None
        source_name = fork.get('source', project.source.name)
        for s in sources:
            if s.name == source_name:
                self._source = s

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
                'ref': self.ref}

    def status(self) -> str:
        """Return formatted fork status

        :return: Formatted fork status
        :rtype: str
        """

        if not existing_git_repository(self.path):
            return colored(self.path, 'green')

        repo = ProjectRepo(self.full_path(), self.remote, self.ref)
        project_output = repo.format_project_string(self.path)
        current_ref_output = repo.format_project_ref_string()
        return project_output + ' ' + current_ref_output

    def url(self) -> str:
        """Return project url"""

        return git_url(self._source.protocol, self._source.url, self.name)
