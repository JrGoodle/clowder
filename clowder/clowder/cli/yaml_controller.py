# -*- coding: utf-8 -*-
"""Clowder command line yaml controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import sys

from cement.ext.ext_argparse import ArgparseController, expose

import clowder.util.formatting as fmt
from clowder.clowder_repo import (
    print_clowder_repo_status,
    valid_clowder_yaml_required
)
from clowder.cli.globals import CLOWDER_CONTROLLER
from clowder.yaml.printing import print_yaml


class YAMLController(ArgparseController):
    class Meta:
        label = 'yaml'
        stacked_on = 'base'
        stacked_type = 'embedded'
        description = 'Print clowder.yaml information'

    @expose(
        help='this is the help message for clowder yaml',
        arguments=[
            (['--resolved', '-r'], dict(action='store_true', help='print resolved clowder.yaml'))
        ]
    )
    def yaml(self):
        self._yaml()

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def _yaml(self):
        if self.app.pargs.resolved:
            print(fmt.yaml_string(CLOWDER_CONTROLLER.get_yaml_resolved()))
        else:
            print_yaml(CLOWDER_CONTROLLER.root_directory)
        sys.exit()  # exit early to prevent printing extra newline
