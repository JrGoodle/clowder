# -*- coding: utf-8 -*-
"""Clowder command line link controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import ArgparseController, expose

from clowder.cli import CLOWDER_REPO
from clowder.cli.util import (
    get_saved_version_names,
    options_help_message
)
from clowder.util.decorators import (
    clowder_required,
    print_clowder_repo_status
)


class LinkController(ArgparseController):
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
    @clowder_required
    @print_clowder_repo_status
    def default(self):
        if self.app.pargs.version is None:
            version = None
        else:
            version = self.app.pargs.version[0]
        CLOWDER_REPO.link(version)
