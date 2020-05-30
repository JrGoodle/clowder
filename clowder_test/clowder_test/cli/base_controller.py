# -*- coding: utf-8 -*-
"""Clowder test command line base controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import ArgparseController, expose

from clowder_test.execute import execute_test_command
from clowder_test import ROOT_DIR


VERSION = '0.1.0'


class BaseController(ArgparseController):
    """Clowder app base controller"""

    path = ROOT_DIR / 'test' / 'scripts'

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
    def all(self) -> None:
        """clowder test all command"""

        scripts = [
            './test_example_cats.sh',
            './test_example_swift.sh',
            './test_example_misc.sh'
        ]
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
        help='Run config yaml validation tests'
    )
    def config_yaml_validation(self) -> None:
        """clowder config yaml validation tests"""

        execute_test_command('./test_config_yaml_validation.sh', self.path,
                             parallel=True,
                             write=self.app.pargs.write,
                             coverage=self.app.pargs.coverage,
                             debug=self.app.debug,
                             quiet=self.app.pargs.silent)

    @expose(
        help='Run offline tests'
    )
    def offline(self) -> None:
        """clowder offline tests"""

        execute_test_command('./offline.sh', self.path / 'cats',
                             parallel=self.app.pargs.parallel,
                             write=self.app.pargs.write,
                             coverage=self.app.pargs.coverage,
                             debug=self.app.debug,
                             quiet=self.app.pargs.silent)

    @expose(
        help='Run parallel tests'
    )
    def parallel(self) -> None:
        """clowder parallel tests"""

        execute_test_command('./test_parallel.sh', self.path,
                             parallel=True,
                             write=self.app.pargs.write,
                             coverage=self.app.pargs.coverage,
                             debug=self.app.debug,
                             quiet=self.app.pargs.silent)

    # @expose(
    #     help='Run unit tests'
    # )
    # def unittests(self) -> None:
    #     """clowder unit tests"""
    #
    #     execute_test_command('./unittests.sh', self.path,
    #                          parallel=self.app.pargs.parallel,
    #                          write=self.app.pargs.write,
    #                          coverage=self.app.pargs.coverage,
    #                          test_env=test_env,
    #                          debug=self.app.debug,
    #                          quiet=self.app.pargs.silent)

    @expose(
        help='Run tests requiring remote write permissions'
    )
    def write(self) -> None:
        """clowder write tests"""

        cats_scripts = ['./write_herd.sh', './write_prune.sh', './write_repo.sh', './write_start.sh']
        for script in cats_scripts:
            execute_test_command(script, self.path / 'cats',
                                 parallel=self.app.pargs.parallel,
                                 write=True,
                                 coverage=self.app.pargs.coverage,
                                 debug=self.app.debug,
                                 quiet=self.app.pargs.silent)

        misc_scripts = ['./write_forks.sh']
        for script in misc_scripts:
            execute_test_command(script, self.path / 'misc',
                                 parallel=self.app.pargs.parallel,
                                 write=True,
                                 coverage=self.app.pargs.coverage,
                                 debug=self.app.debug,
                                 quiet=self.app.pargs.silent)

        # execute_test_command('./write_configure_remotes.sh', os.path.join(self.path, 'swift'),
        #                      parallel=self.app.pargs.parallel,
        #                      write=True,
        #                      coverage=self.app.pargs.coverage,
        #                      debug=self.app.debug,
        #                      quiet=self.app.pargs.silent,
        #                      ssh=True)
