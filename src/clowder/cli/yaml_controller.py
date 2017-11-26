# -*- coding: utf-8 -*-
"""Clowder command line yaml controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

from cement.ext.ext_argparse import ArgparseController, expose

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.clowder_repo import print_clowder_repo_status
from clowder.util.decorators import valid_clowder_yaml_required
from clowder.yaml.printing import print_yaml


class YAMLController(ArgparseController):
    """Clowder yaml command controller"""

    class Meta:
        """Clowder yaml Meta configuration"""

        label = 'yaml'
        stacked_on = 'base'
        stacked_type = 'embedded'
        description = 'Print clowder.yaml information'

    @expose(
        help='Print clowder.yaml information',
        arguments=[
            (['--resolved', '-r'], dict(action='store_true', help='print resolved clowder.yaml'))
        ]
    )
    def yaml(self):
        """Clowder yaml command entry point"""

        self._yaml()

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def _yaml(self):
        """Clowder yaml command private implementation"""

        if self.app.pargs.resolved:
            print(fmt.yaml_string(CLOWDER_CONTROLLER.get_yaml(resolved=True)))
        else:
            print_yaml()
