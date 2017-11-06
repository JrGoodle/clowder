# -*- coding: utf-8 -*-
"""Clowder test llvm command line controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os

from cement.ext.ext_argparse import ArgparseController, expose

from clowder_test.execute import execute_test_command

from clowder_test import ROOT_DIR


class LLVMController(ArgparseController):
    """Clowder test command llvm controller"""

    path = os.path.join(ROOT_DIR, 'test', 'scripts', 'llvm')

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

        self._execute_command('./test_example_llvm.sh', os.path.join(ROOT_DIR, 'test', 'scripts'))

    @expose(
        help='Run llvm branch tests'
    )
    def branch(self):
        """clowder llvm branch tests"""

        self._execute_command('./branch.sh', self.path)

    @expose(
        help='Run llvm forks tests'
    )
    def forks(self):
        """clowder llvm forks tests"""

        self._execute_command('./forks.sh', self.path)

    @expose(
        help='Run llvm herd tests'
    )
    def herd(self):
        """clowder llvm herd tests"""

        self._execute_command('./herd.sh', self.path)

    @expose(
        help='Run llvm reset tests'
    )
    def reset(self):
        """clowder llvm reset tests"""

        self._execute_command('./reset.sh', self.path)

    @expose(
        help='Run llvm sync tests'
    )
    def sync(self):
        """clowder llvm sync tests"""

        self._execute_command('./sync.sh', self.path)

    def _execute_command(self, command, path):
        """Private execute command"""

        execute_test_command(command, path,
                             parallel=self.app.pargs.parallel,
                             write=self.app.pargs.write,
                             coverage=self.app.pargs.coverage)
