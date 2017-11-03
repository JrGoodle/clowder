# -*- coding: utf-8 -*-
"""Clowder command line save controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os
import sys

from cement.ext.ext_argparse import expose

import clowder.util.formatting as fmt
from clowder.cli.abstract_base_controller import AbstractBaseController
from clowder.util.decorators import valid_clowder_yaml_required
from clowder.commands.util import (
    validate_groups,
    validate_projects_exist
)
from clowder.yaml.saving import save_yaml


class SaveController(AbstractBaseController):
    class Meta:
        label = 'save'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Create version of clowder.yaml for current repos'
        arguments = [
            (['version'], dict(help='version to save', metavar='VERSION'))
            ]

    @expose(help="second-controller default command", hide=True)
    @valid_clowder_yaml_required
    def default(self):
        if self.app.pargs.version.lower() == 'default':
            print(fmt.save_default_error(self.app.pargs.version))
            sys.exit(1)

        self.clowder_repo.print_status()
        validate_projects_exist(self.clowder)
        validate_groups(self.clowder.groups)

        version_name = self.app.pargs.version.replace('/', '-')  # Replace path separators with dashes
        version_dir = os.path.join(self.clowder.root_directory, '.clowder', 'versions', version_name)
        _make_dir(version_dir)

        yaml_file = os.path.join(version_dir, 'clowder.yaml')
        if os.path.exists(yaml_file):
            print(fmt.save_version_exists_error(version_name, yaml_file) + '\n')
            sys.exit(1)

        print(fmt.save_version(version_name, yaml_file))
        save_yaml(self.clowder.get_yaml(), yaml_file)


def _make_dir(directory):
    """Make directory if it doesn't exist

    :param str directory: Directory path to create
    :raise OSError:
    """

    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError as err:
            if err.errno != os.errno.EEXIST:
                raise
