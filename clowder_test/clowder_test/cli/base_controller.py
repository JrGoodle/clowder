# -*- coding: utf-8 -*-
"""Clowder test command line base controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os

from cement.ext.ext_argparse import ArgparseController, expose

from clowder_test.execute import execute_test_command

from clowder_test import ROOT_DIR


VERSION = '0.1.0'


class BaseController(ArgparseController):
    """Clowder app base controller"""

    path = os.path.join(ROOT_DIR, 'test', 'scripts')

    class Meta:
        """Clowder app base Meta configuration"""

        label = 'base'
        description = 'Clowder test runner'
        arguments = [
            (['--coverage', '-c'], dict(action='store_true', help='run tests with code coverage')),
            (['--parallel', '-p'], dict(action='store_true', help='run tests with parallel commands')),
            (['--write', '-w'], dict(action='store_true', help='run tests requiring test repo write access')),
            (['-v', '--version'], dict(action='version', version=VERSION)),
            (['--silent'], dict(action='store_true', help='suppress all output of subcommands'))
        ]

    @expose(
        help='Run all tests'
    )
    def all(self):
        """clowder test all command"""

        scripts = ['./test_example_cats.sh', './test_example_cocos2d.sh',
                   './test_example_llvm.sh', './test_example_swift.sh']
        for script in scripts:
            execute_test_command(script, self.path,
                                 parallel=self.app.pargs.parallel,
                                 write=self.app.pargs.write,
                                 coverage=self.app.pargs.coverage,
                                 debug=self.app.debug,
                                 quiet=self.app.pargs.silent)

        self.offline()
        self.parallel()

    @expose(
        help='Run offline tests'
    )
    def offline(self):
        """clowder offline tests"""

        execute_test_command('./offline.sh', os.path.join(self.path, 'cats'),
                             parallel=self.app.pargs.parallel,
                             write=self.app.pargs.write,
                             coverage=self.app.pargs.coverage,
                             debug=self.app.debug,
                             quiet=self.app.pargs.silent)

    @expose(
        help='Run parallel tests'
    )
    def parallel(self):
        """clowder parallel tests"""

        execute_test_command('./test_parallel.sh', self.path,
                             parallel=True,
                             write=self.app.pargs.write,
                             coverage=self.app.pargs.coverage,
                             debug=self.app.debug,
                             quiet=self.app.pargs.silent)

    @expose(
        help='Run tests requiring ssh credentials'
    )
    def ssh(self):
        """clowder ssh tests"""

        execute_test_command('./ssh_protocol.sh', os.path.join(self.path, 'cocos2d'),
                             parallel=self.app.pargs.parallel,
                             write=True,
                             coverage=self.app.pargs.coverage,
                             debug=self.app.debug,
                             quiet=self.app.pargs.silent,
                             ssh=True)

        execute_test_command('./ssh_configure_remotes.sh', os.path.join(self.path, 'swift'),
                             parallel=self.app.pargs.parallel,
                             write=True,
                             coverage=self.app.pargs.coverage,
                             debug=self.app.debug,
                             quiet=self.app.pargs.silent,
                             ssh=True)

    @expose(
        help='Run unit tests',
        arguments=[
            (['version'], dict(choices=['python2', 'python3'], metavar='PYTHON_VERSION',
                               help='Python vesion to run unit tests for'))
        ]
    )
    def unittests(self):
        """clowder unit tests"""

        if self.app.pargs.version == 'python2':
            test_env = {"PYTHON_VERSION": 'python'}
        else:
            test_env = {"PYTHON_VERSION": 'python3'}

        execute_test_command('./unittests.sh', self.path,
                             parallel=self.app.pargs.parallel,
                             write=self.app.pargs.write,
                             coverage=self.app.pargs.coverage,
                             test_env=test_env,
                             debug=self.app.debug,
                             quiet=self.app.pargs.silent)

    @expose(
        help='Run tests requiring remote write permissions'
    )
    def write(self):
        """clowder write tests"""

        cats_scripts = ['./write_herd.sh', './write_prune.sh', './write_repo.sh', './write_start.sh']
        for script in cats_scripts:
            execute_test_command(script, os.path.join(self.path, 'cats'),
                                 parallel=self.app.pargs.parallel,
                                 write=True,
                                 coverage=self.app.pargs.coverage,
                                 debug=self.app.debug,
                                 quiet=self.app.pargs.silent)

        llvm_scripts = ['./write_forks.sh', './write_sync.sh']
        for script in llvm_scripts:
            execute_test_command(script, os.path.join(self.path, 'llvm'),
                                 parallel=self.app.pargs.parallel,
                                 write=True,
                                 coverage=self.app.pargs.coverage,
                                 debug=self.app.debug,
                                 quiet=self.app.pargs.silent)
