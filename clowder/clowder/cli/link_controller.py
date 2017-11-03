import os

from cement.ext.ext_argparse import expose

from clowder.cli.abstract_base_controller import AbstractBaseController
from clowder.cli.util import (
    get_saved_version_names,
    options_help_message
)


class LinkController(AbstractBaseController):
    class Meta:
        label = 'link'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Symlink clowder.yaml version'
        versions = get_saved_version_names()
        arguments = [
            (['--version', '-v'], dict(choices=versions, nargs=1, default=None, metavar='VERSION',
                                       help=options_help_message(versions, 'version to symlink')))
            ]

    @expose(help="second-controller default command", hide=True)
    def default(self):
        print("Inside SecondController.default()")
