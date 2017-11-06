# -*- coding: utf-8 -*-
"""Clowder test cats command line controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os

from cement.ext.ext_argparse import ArgparseController, expose

from clowder_test.execute import (
    execute_command,
    clowder_test_exit
)


class CatsController(ArgparseController):
    """Clowder test command cats controller"""

    path = os.path.join(os.getcwd(), 'test', 'scripts', 'cats')

    class Meta:
        """Clowder test cats Meta configuration"""

        label = 'cats'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Run cats tests'

    @expose(
        help='Run all cats tests'
    )
    def all(self):
        """clowder cats tests"""

        path = os.path.join(os.getcwd(), 'test', 'scripts')
        return_code = self._execute_command('./test_example_cats.sh', path)
        clowder_test_exit(return_code)

    @expose(
        help='Run cats branch tests'
    )
    def branch(self):
        """clowder cats branch tests"""

        return_code = self._execute_command('./branch.sh', self.path)
        clowder_test_exit(return_code)

    @expose(
        help='Run cats checkout tests'
    )
    def checkout(self):
        """clowder cats checkout tests"""

        return_code = self._execute_command('./checkout.sh', self.path)
        clowder_test_exit(return_code)

    @expose(
        help='Run cats clean tests'
    )
    def clean(self):
        """clowder cats clean tests"""

        return_code = self._execute_command('./clean.sh', self.path)
        clowder_test_exit(return_code)

    @expose(
        help='Run cats diff tests'
    )
    def diff(self):
        """clowder cats diff tests"""

        return_code = self._execute_command('./diff.sh', self.path)
        clowder_test_exit(return_code)

    @expose(
        help='Run cats forall tests'
    )
    def forall(self):
        """clowder cats forall tests"""

        return_code = self._execute_command('./forall.sh', self.path)
        clowder_test_exit(return_code)

    @expose(
        help='Run cats help tests'
    )
    def help(self):
        """clowder cats help tests"""

        return_code = self._execute_command('./help.sh', self.path)
        clowder_test_exit(return_code)

    @expose(
        help='Run cats herd branch tests'
    )
    def herd_branch(self):
        """clowder cats herd branch tests"""

        return_code = self._execute_command('./herd_branch.sh', self.path)
        clowder_test_exit(return_code)

    @expose(
        help='Run cats herd tag tests'
    )
    def herd_tag(self):
        """clowder cats herd tag tests"""

        return_code = self._execute_command('./herd_tag.sh', self.path)
        clowder_test_exit(return_code)

    @expose(
        help='Run cats herd tests'
    )
    def herd(self):
        """clowder cats herd tests"""

        return_code = self._execute_command('./herd.sh', self.path)
        clowder_test_exit(return_code)

    @expose(
        help='Run cats init tests'
    )
    def init(self):
        """clowder cats init tests"""

        return_code = self._execute_command('./init.sh', self.path)
        clowder_test_exit(return_code)

    @expose(
        help='Run cats link tests'
    )
    def link(self):
        """clowder cats link tests"""

        return_code = self._execute_command('./link.sh', self.path)
        clowder_test_exit(return_code)

    @expose(
        help='Run cats prune tests'
    )
    def prune(self):
        """clowder cats prune tests"""

        return_code = self._execute_command('./prune.sh', self.path)
        clowder_test_exit(return_code)

    @expose(
        help='Run cats repo tests'
    )
    def repo(self):
        """clowder cats repo tests"""

        return_code = self._execute_command('./repo.sh', self.path)
        clowder_test_exit(return_code)

    @expose(
        help='Run cats reset tests'
    )
    def reset(self):
        """clowder cats reset tests"""

        return_code = self._execute_command('./reset.sh', self.path)
        clowder_test_exit(return_code)

    @expose(
        help='Run cats save tests'
    )
    def save(self):
        """clowder cats save tests"""

        return_code = self._execute_command('./save.sh', self.path)
        clowder_test_exit(return_code)

    @expose(
        help='Run cats start tests'
    )
    def start(self):
        """clowder cats start tests"""

        return_code = self._execute_command('./start.sh', self.path)
        clowder_test_exit(return_code)

    @expose(
        help='Run cats stash tests'
    )
    def stash(self):
        """clowder cats stash tests"""

        return_code = self._execute_command('./stash.sh', self.path)
        clowder_test_exit(return_code)

    @expose(
        help='Run cats status tests'
    )
    def status(self):
        """clowder cats status tests"""

        return_code = self._execute_command('./status.sh', self.path)
        clowder_test_exit(return_code)

    @expose(
        help='Run cats yaml tests'
    )
    def yaml(self):
        """clowder cats yaml tests"""

        return_code = self._execute_command('./yaml.sh', self.path)
        clowder_test_exit(return_code)

    @expose(
        help='Run cats yaml import tests'
    )
    def yaml_import(self):
        """clowder cats yaml import tests"""

        return_code = self._execute_command('./yaml_import.sh', self.path)
        clowder_test_exit(return_code)

    @expose(
        help='Run cats yaml validation tests'
    )
    def yaml_validation(self):
        """clowder cats yaml validation tests"""

        return_code = self._execute_command('./yaml_validation.sh', self.path)
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
