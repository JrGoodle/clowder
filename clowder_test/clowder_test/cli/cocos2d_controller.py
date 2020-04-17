# -*- coding: utf-8 -*-
"""Clowder test cocos2d command line controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os

from cement.ext.ext_argparse import ArgparseController, expose

from clowder_test.execute import execute_test_command

from clowder_test import ROOT_DIR


class Cocos2dController(ArgparseController):
    """Clowder test command cocos2d controller"""

    path = os.path.join(ROOT_DIR, 'test', 'scripts', 'cocos2d')

    class Meta:
        """Clowder test cocos2d Meta configuration"""

        label = 'cocos2d'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Display current branches'

    @expose(
        help='Run all cocos2d tests'
    )
    def all(self):
        """clowder cocos2d tests"""

        self._execute_command('./test_example_cocos2d.sh', os.path.join(ROOT_DIR, 'test', 'scripts'))

    @expose(
        help='Run herd cocos2d tests'
    )
    def herd(self):
        """clowder cocos2d herd tests"""

        self._execute_command('./herd.sh', self.path)

    @expose(
        help='Run protocol cocos2d tests'
    )
    def protocol(self):
        """clowder cocos2d protocol tests"""

        self._execute_command('./protocol.sh', self.path)

    def _execute_command(self, command, path):
        """Private execute command"""

        execute_test_command(command, path,
                             parallel=self.app.pargs.parallel,
                             write=self.app.pargs.write,
                             coverage=self.app.pargs.coverage,
                             debug=self.app.debug,
                             quiet=self.app.pargs.silent)
