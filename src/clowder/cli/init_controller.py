# -*- coding: utf-8 -*-
"""Clowder command line init controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os

from cement.ext.ext_argparse import ArgparseController, expose
from termcolor import colored, cprint

import clowder.clowder_repo as clowder_repo
from clowder import CURRENT_DIR
from clowder.error.clowder_exit import ClowderExit
from clowder.git.util import existing_git_repository
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
    def init(self) -> None:
        """Clowder init command entry point"""

        self._init()

    @network_connection_required
    def _init(self) -> None:
        """Clowder init command private implementation

        :raise ClowderExit:
        """

        clowder_repo_dir = os.path.join(CURRENT_DIR, '.clowder')
        if existing_git_repository(clowder_repo_dir):
            cprint('Clowder already initialized in this directory\n', 'red')
            raise ClowderExit(1)

        url_output = colored(self.app.pargs.url, 'green')
        print(f"Create clowder repo from {url_output}\n")
        if self.app.pargs.branch is None:
            branch = 'master'
        else:
            branch = str(self.app.pargs.branch[0])
        clowder_repo.init(self.app.pargs.url, branch)
