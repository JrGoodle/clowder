# -*- coding: utf-8 -*-
"""Clowder command line init controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import os

from cement.ext.ext_argparse import ArgparseController, expose
from termcolor import colored, cprint

from clowder.clowder_repo import CLOWDER_REPO
from clowder.error.clowder_exit import ClowderExit
from clowder.util.connectivity import network_connection_required


class InitController(ArgparseController):
    """Clowder init command controller"""

    class Meta:
        """Clowder init Meta configuration"""

        label = 'init'
        stacked_on = 'base'
        stacked_type = 'embedded'
        description = 'Clone repository to clowder directory and create clowder.yaml symlink'

    @expose(
        help='Clone repository to clowder directory and create clowder.yaml symlink',
        arguments=[
            (['url'], dict(metavar='URL', help='url of repo containing clowder.yaml')),
            (['--branch', '-b'], dict(nargs=1, metavar='BRANCH', help='branch of repo containing clowder.yaml'))
        ]
    )
    def init(self):
        """Clowder init command entry point"""

        self._init()

    @network_connection_required
    def _init(self):
        """Clowder init command private implementation

        :raise ClowderExit:
        """

        if os.path.isdir(CLOWDER_REPO.clowder_path):
            cprint('Clowder already initialized in this directory\n', 'red')
            raise ClowderExit(1)

        url_output = colored(self.app.pargs.url, 'green')
        print('Create clowder repo from ' + url_output + '\n')
        if self.app.pargs.branch is None:
            branch = 'master'
        else:
            branch = str(self.app.pargs.branch[0])
        CLOWDER_REPO.init(self.app.pargs.url, branch)
