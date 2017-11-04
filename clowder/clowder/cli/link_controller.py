# -*- coding: utf-8 -*-
"""Clowder command line link controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import ArgparseController, expose

from clowder.cli.util import (
    get_saved_version_names,
    options_help_message
)
from clowder.clowder_repo import (
    CLOWDER_REPO,
    clowder_required,
    print_clowder_repo_status
)


class LinkController(ArgparseController):
    """Clowder link command controller"""

    class Meta:
        """Clowder link Meta configuration"""

        label = 'link'
        stacked_on = 'base'
        stacked_type = 'embedded'
        description = 'Symlink clowder.yaml version'

    @expose(
        help='this is the help message for clowder link',
        arguments=[
            (['--version', '-v'], dict(choices=get_saved_version_names(),
                                       nargs=1, default=None, metavar='VERSION',
                                       help=options_help_message(get_saved_version_names(), 'version to symlink')))
            ]
    )
    def link(self):
        """Clowder link command entry point"""

        self._link()

    @clowder_required
    @print_clowder_repo_status
    def _link(self):
        """Clowder link command private implementation"""

        if self.app.pargs.version is None:
            version = None
        else:
            version = self.app.pargs.version[0]
        CLOWDER_REPO.link(version)
