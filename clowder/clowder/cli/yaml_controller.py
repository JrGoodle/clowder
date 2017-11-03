from __future__ import print_function

import sys

from cement.ext.ext_argparse import expose

import clowder.util.formatting as fmt
from clowder.cli.abstract_base_controller import AbstractBaseController
from clowder.util.decorators import (
    print_clowder_repo_status,
    valid_clowder_yaml_required
)
from clowder.yaml.printing import print_yaml


class YAMLController(AbstractBaseController):
    class Meta:
        label = 'yaml'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Print clowder.yaml information'
        arguments = [
            (['--resolved', '-r'], dict(action='store_true', help='print resolved clowder.yaml'))
            ]

    @expose(help="second-controller default command", hide=True)
    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def default(self):
        if self.app.pargs.resolved:
            print(fmt.yaml_string(self.clowder.get_yaml_resolved()))
        else:
            print_yaml(self.clowder.root_directory)
        sys.exit()  # exit early to prevent printing extra newline
