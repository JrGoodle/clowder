# -*- coding: utf-8 -*-
"""Clowder command line link controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import ArgparseController, expose

from clowder import CLOWDER_DIR
from clowder.util.decorators import (
    clowder_required,
    print_clowder_repo_status
)
from clowder.util.clowder_utils import (
    get_saved_version_names,
    link_clowder_yaml,
    options_help_message
)


class LinkController(ArgparseController):
    """Clowder link command controller"""

    class Meta:
        """Clowder link Meta configuration"""

        label = 'link'
        stacked_on = 'base'
        stacked_type = 'embedded'
        description = 'Symlink clowder.yaml version'

    versions = get_saved_version_names()

    @expose(
        help='Symlink clowder.yaml version',
        arguments=[
            (['version'], dict(metavar='VERSION', choices=versions, nargs=1, default=None,
                               help=options_help_message(versions, 'version to symlink')))
        ]
    )
    def link(self) -> None:
        """Clowder link command entry point"""

        self._link()

    @clowder_required
    @print_clowder_repo_status
    def _link(self) -> None:
        """Clowder link command private implementation"""

        if self.app.pargs.version is None:
            version = None
        else:
            version = self.app.pargs.version
        link_clowder_yaml(CLOWDER_DIR, version)
