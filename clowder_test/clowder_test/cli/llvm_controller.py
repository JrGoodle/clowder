# -*- coding: utf-8 -*-
"""Clowder test llvm command line controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os

from cement.ext.ext_argparse import ArgparseController, expose

from clowder_test.execute import (
    execute_command,
    clowder_test_exit
)


class LLVMController(ArgparseController):
    """Clowder test command llvm controller"""

    path = os.path.join(os.getcwd(), 'test', 'scripts', 'llvm')

    class Meta:
        """Clowder test llvm Meta configuration"""

        label = 'llvm'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Run llvm tests'

    @expose(
        help='Run all llvm tests'
    )
    def all(self):
        """clowder llvm tests"""

        path = os.path.join(os.getcwd(), 'test', 'scripts')
        return_code = self._execute_command('./test_example_llvm.sh', path)
        clowder_test_exit(return_code)

    @expose(
        help='Run llvm branch tests'
    )
    def branch(self):
        """clowder llvm branch tests"""

        return_code = self._execute_command('./branch.sh', self.path)
        clowder_test_exit(return_code)

    @expose(
        help='Run llvm forks tests'
    )
    def forks(self):
        """clowder llvm forks tests"""

        return_code = self._execute_command('./forks.sh', self.path)
        clowder_test_exit(return_code)

    @expose(
        help='Run llvm herd tests'
    )
    def herd(self):
        """clowder llvm herd tests"""

        return_code = self._execute_command('./herd.sh', self.path)
        clowder_test_exit(return_code)

    @expose(
        help='Run llvm reset tests'
    )
    def reset(self):
        """clowder llvm reset tests"""

        return_code = self._execute_command('./reset.sh', self.path)
        clowder_test_exit(return_code)

    @expose(
        help='Run llvm sync tests'
    )
    def sync(self):
        """clowder llvm sync tests"""

        return_code = self._execute_command('./sync.sh', self.path)
        clowder_test_exit(return_code)

    def _execute_command(self, command, path):
        """Private execute command"""

        access = 'write' if self.app.pargs.write else 'read'
        test_env = {'ACCESS_LEVEL': access}
        if self.app.pargs.parallel:
            test_env["PARALLEL"] = '--parallel'
        if self.app.pargs.coverage:
            test_env['COMMAND'] = 'coverage run -m clowder.clowder_app'
        else:
            test_env['COMMAND'] = 'clowder'
        return execute_command(command, path, env=test_env)
