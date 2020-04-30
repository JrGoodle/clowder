# -*- coding: utf-8 -*-
"""Clowder test cats command line controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os

from cement.ext.ext_argparse import ArgparseController, expose

from clowder_test.execute import create_cats_cache, execute_test_command
from clowder_test import ROOT_DIR


class CatsController(ArgparseController):
    """Clowder test command cats controller"""

    path = os.path.join(ROOT_DIR, 'test', 'scripts', 'cats')

    class Meta:
        """Clowder test cats Meta configuration"""

        label = 'cats'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Run cats tests'

    @expose(
        help='Run all cats tests'
    )
    def all(self) -> None:
        """clowder cats tests"""

        self._execute_command('./test_example_cats.sh', os.path.join(ROOT_DIR, 'test', 'scripts'))

    @expose(
        help='Run cats branch tests'
    )
    @create_cats_cache
    def branch(self) -> None:
        """clowder cats branch tests"""

        self._execute_command('./branch.sh', self.path)

    @expose(
        help='Run cats checkout tests'
    )
    @create_cats_cache
    def checkout(self) -> None:
        """clowder cats checkout tests"""

        self._execute_command('./checkout.sh', self.path)

    @expose(
        help='Run cats clean tests'
    )
    @create_cats_cache
    def clean(self) -> None:
        """clowder cats clean tests"""

        self._execute_command('./clean.sh', self.path)

    @expose(
        help='Run cats diff tests'
    )
    @create_cats_cache
    def diff(self) -> None:
        """clowder cats diff tests"""

        self._execute_command('./diff.sh', self.path)

    @expose(
        help='Run cats forall tests'
    )
    @create_cats_cache
    def forall(self) -> None:
        """clowder cats forall tests"""

        self._execute_command('./forall.sh', self.path)

    @expose(
        help='Run cats help tests'
    )
    @create_cats_cache
    def help(self) -> None:
        """clowder cats help tests"""

        self._execute_command('./help.sh', self.path)

    @expose(
        help='Run cats herd branch tests'
    )
    @create_cats_cache
    def herd_branch(self) -> None:
        """clowder cats herd branch tests"""

        self._execute_command('./herd_branch.sh', self.path)

    @expose(
        help='Run cats herd submodules tests'
    )
    @create_cats_cache
    def herd_submodules(self) -> None:
        """clowder cats herd submodules tests"""

        self._execute_command('./herd_submodules.sh', self.path)

    @expose(
        help='Run cats herd tag tests'
    )
    @create_cats_cache
    def herd_tag(self) -> None:
        """clowder cats herd tag tests"""

        self._execute_command('./herd_tag.sh', self.path)

    @expose(
        help='Run cats herd tests'
    )
    @create_cats_cache
    def herd(self) -> None:
        """clowder cats herd tests"""

        self._execute_command('./herd.sh', self.path)

    @expose(
        help='Run cats init tests'
    )
    @create_cats_cache
    def init(self) -> None:
        """clowder cats init tests"""

        self._execute_command('./init.sh', self.path)

    @expose(
        help='Run cats link tests'
    )
    @create_cats_cache
    def link(self) -> None:
        """clowder cats link tests"""

        self._execute_command('./link.sh', self.path)

    @expose(
        help='Run cats prune tests'
    )
    @create_cats_cache
    def prune(self) -> None:
        """clowder cats prune tests"""

        self._execute_command('./prune.sh', self.path)

    @expose(
        help='Run cats repo tests'
    )
    @create_cats_cache
    def repo(self) -> None:
        """clowder cats repo tests"""

        self._execute_command('./repo.sh', self.path)

    @expose(
        help='Run cats reset tests'
    )
    @create_cats_cache
    def reset(self) -> None:
        """clowder cats reset tests"""

        self._execute_command('./reset.sh', self.path)

    @expose(
        help='Run cats save tests'
    )
    @create_cats_cache
    def save(self) -> None:
        """clowder cats save tests"""

        self._execute_command('./save.sh', self.path)

    @expose(
        help='Run cats skip tests'
    )
    @create_cats_cache
    def skip(self) -> None:
        """clowder cats skip tests"""

        self._execute_command('./skip.sh', self.path)

    @expose(
        help='Run cats start tests'
    )
    @create_cats_cache
    def start(self) -> None:
        """clowder cats start tests"""

        self._execute_command('./start.sh', self.path)

    @expose(
        help='Run cats stash tests'
    )
    @create_cats_cache
    def stash(self) -> None:
        """clowder cats stash tests"""

        self._execute_command('./stash.sh', self.path)

    @expose(
        help='Run cats status tests'
    )
    @create_cats_cache
    def status(self) -> None:
        """clowder cats status tests"""

        self._execute_command('./status.sh', self.path)

    @expose(
        help='Run cats yaml tests'
    )
    @create_cats_cache
    def yaml(self) -> None:
        """clowder cats yaml tests"""

        self._execute_command('./yaml.sh', self.path)

    @expose(
        help='Run cats yaml validation tests'
    )
    @create_cats_cache
    def yaml_validation(self) -> None:
        """clowder cats yaml validation tests"""

        self._execute_command('./yaml_validation.sh', self.path)

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
