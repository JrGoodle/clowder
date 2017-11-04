# -*- coding: utf-8 -*-
"""Clowder test cocos2d command line controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os

from cement.ext.ext_argparse import ArgparseController, expose

from clowder_test.execute import (
    execute_command,
    clowder_test_exit
)


class Cocos2dController(ArgparseController):
    """Clowder test command cocos2d controller"""

    path = os.path.join(os.getcwd(), 'test', 'scripts', 'cocos2d')

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

        path = os.path.join(os.getcwd(), 'test', 'scripts')
        return_code = self._execute_command('./test_example_cocos2d.sh', path)
        clowder_test_exit(return_code)

    @expose(
        help='Run clean cocos2d tests'
    )
    def clean(self):
        """clowder cocos2d clean tests"""

        return_code = self._execute_command('./clean.sh', self.path)
        clowder_test_exit(return_code)

    @expose(
        help='Run herd cocos2d tests'
    )
    def herd(self):
        """clowder cocos2d herd tests"""

        return_code = self._execute_command('./herd.sh', self.path)
        clowder_test_exit(return_code)

    @expose(
        help='Run skip cocos2d tests'
    )
    def skip(self):
        """clowder cocos2d skip tests"""

        return_code = self._execute_command('./skip.sh', self.path)
        clowder_test_exit(return_code)

    def _execute_command(self, command, path):
        """Private execute command"""

        access = 'write' if self.app.pargs.write else 'read'
        test_env = {'ACCESS_LEVEL': access}
        if self.app.pargs.parallel:
            test_env["PARALLEL"] = '--parallel'
        return execute_command(command, path, env=test_env)
