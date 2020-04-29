# -*- coding: utf-8 -*-
"""Clowder test swift command line controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os

from cement.ext.ext_argparse import ArgparseController, expose

from clowder_test.execute import execute_test_command
from clowder_test import ROOT_DIR


class SwiftController(ArgparseController):
    """Clowder test command swift controller"""

    path = os.path.join(ROOT_DIR, 'test', 'scripts', 'swift')

    class Meta:
        """Clowder test swift Meta configuration"""

        label = 'swift'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Run swift tests'

    @expose(
        help='Run all swift tests'
    )
    def all(self) -> None:
        """clowder swift tests"""

        self._execute_command('./test_example_swift.sh', os.path.join(ROOT_DIR, 'test', 'scripts'))

    @expose(
        help='Run swift config versions tests'
    )
    def config_versions(self) -> None:
        """clowder swift config versions tests"""

        self._execute_command('./config_versions.sh', self.path)

    @expose(
        help='Run swift configure remotes tests'
    )
    def configure_remotes(self) -> None:
        """clowder swift configure remotes tests"""

        self._execute_command('./configure_remotes.sh', self.path)

    @expose(
        help='Run swift reset tests'
    )
    def reset(self) -> None:
        """clowder swift reset tests"""

        self._execute_command('./reset.sh', self.path)

    def _execute_command(self, command: str, path: str) -> None:
        """Private execute command

        :param str command: Command to run
        :param str path: Path to set as ``cwd``
        """

        execute_test_command(command, path,
                             parallel=self.app.pargs.parallel,
                             write=self.app.pargs.write,
                             coverage=self.app.pargs.coverage,
                             debug=self.app.debug,
                             quiet=self.app.pargs.silent)
