# -*- coding: utf-8 -*-
"""Clowder command line save controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import errno
import os

from cement.ext.ext_argparse import ArgparseController, expose

import clowder.util.formatting as fmt
from clowder import ROOT_DIR
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.clowder_repo import CLOWDER_REPO
from clowder.error.clowder_exit import ClowderExit
from clowder.util.decorators import valid_clowder_yaml_required
from clowder.util.clowder_utils import validate_projects
from clowder.util.yaml import save_yaml


class SaveController(ArgparseController):
    """Clowder save command controller"""

    class Meta:
        """Clowder save Meta configuration"""

        label = 'save'
        stacked_on = 'base'
        stacked_type = 'embedded'
        description = 'Create version of clowder.yaml for current repos'

    @expose(
        help='Create version of clowder.yaml for current repos',
        arguments=[
            (['version'], dict(help='version to save', metavar='VERSION'))
        ]
    )
    def save(self) -> None:
        """Clowder save command entry point"""

        self._save()

    @valid_clowder_yaml_required
    def _save(self) -> None:
        """Clowder save command private implementation

        :raise ClowderExit:
        """

        if self.app.pargs.version.lower() == 'default':
            print(fmt.error_save_default(self.app.pargs.version))
            raise ClowderExit(1)

        CLOWDER_REPO.print_status()
        CLOWDER_CONTROLLER.validate_projects_exist()
        # TODO: Get all projects
        validate_projects(CLOWDER_CONTROLLER.projects)

        # Replace path separators with dashes to avoid creating directories
        version_name = self.app.pargs.version.replace('/', '-')

        versions_dir = os.path.join(ROOT_DIR, '.clowder', 'versions')
        _make_dir(versions_dir)

        yaml_file = os.path.join(versions_dir, f'{version_name}.yaml')
        if os.path.exists(yaml_file):
            print(fmt.error_save_version_exists(version_name, yaml_file) + '\n')
            raise ClowderExit(1)

        print(fmt.save_version_message(version_name, yaml_file))
        save_yaml(CLOWDER_CONTROLLER.get_yaml(), yaml_file)


def _make_dir(directory: str) -> None:
    """Make directory if it doesn't exist

    :param str directory: Directory path to create
    :raise OSError:
    """

    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError as err:
            if err.errno != errno.EEXIST:
                raise
