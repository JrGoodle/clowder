# -*- coding: utf-8 -*-
"""Clowder test misc command line controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from pathlib import Path

from cement.ext.ext_argparse import ArgparseController, expose

from clowder_test.execute import execute_test_command
from clowder_test import ROOT_DIR


class MiscController(ArgparseController):
    """Clowder test command misc controller"""

    path = ROOT_DIR / 'test' / 'scripts' / 'misc'

    class Meta:
        """Clowder test misc Meta configuration"""

        label = 'misc'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Run misc tests'

    @expose(
        help='Run all misc tests'
    )
    def all(self) -> None:
        """clowder misc tests"""

        self._execute_command('./test_example_misc.sh', ROOT_DIR / 'test' / 'scripts')

    @expose(
        help='Run misc forks tests'
    )
    def forks(self) -> None:
        """clowder misc forks tests"""

        self._execute_command('./forks.sh', self.path)

    @expose(
        help='Run misc sources tests'
    )
    def sources(self) -> None:
        """clowder misc sources tests"""

        self._execute_command('./sources.sh', self.path)

    def _execute_command(self, command: str, path: Path) -> None:
        """Private execute command

        :param str command: Command to run
        :param Path path: Path to set as ``cwd``
        """

        execute_test_command(command, path,
                             parallel=self.app.pargs.parallel,
                             write=self.app.pargs.write,
                             coverage=self.app.pargs.coverage,
                             debug=self.app.debug,
                             quiet=self.app.pargs.silent)
