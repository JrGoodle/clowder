# -*- coding: utf-8 -*-
"""Clowder test cats command line controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os

from cement.ext.ext_argparse import ArgparseController, expose

from clowder_test.execute import execute_test_command
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
    def branch(self) -> None:
        """clowder cats branch tests"""

        self._execute_command('./branch.sh', self.path)

    @expose(
        help='Run cats checkout tests'
    )
    def checkout(self) -> None:
        """clowder cats checkout tests"""

        self._execute_command('./checkout.sh', self.path)

    @expose(
        help='Run cats clean tests'
    )
    def clean(self) -> None:
        """clowder cats clean tests"""

        self._execute_command('./clean.sh', self.path)

    @expose(
        help='Run cats config tests'
    )
    def config(self) -> None:
        """clowder cats config tests"""

        self._execute_command('./config.sh', self.path)

    @expose(
        help='Run cats diff tests'
    )
    def diff(self) -> None:
        """clowder cats diff tests"""

        self._execute_command('./diff.sh', self.path)

    @expose(
        help='Run cats forall tests'
    )
    def forall(self) -> None:
        """clowder cats forall tests"""

        self._execute_command('./forall.sh', self.path)

    @expose(
        help='Run cats groups tests'
    )
    def groups(self) -> None:
        """clowder cats groups tests"""

        self._execute_command('./groups.sh', self.path)

    @expose(
        help='Run cats help tests'
    )
    def help(self) -> None:
        """clowder cats help tests"""

        self._execute_command('./help.sh', self.path)

    @expose(
        help='Run cats herd branch tests'
    )
    def herd_branch(self) -> None:
        """clowder cats herd branch tests"""

        self._execute_command('./herd_branch.sh', self.path)

    @expose(
        help='Run cats herd submodules tests'
    )
    def herd_submodules(self) -> None:
        """clowder cats herd submodules tests"""

        self._execute_command('./herd_submodules.sh', self.path)

    @expose(
        help='Run cats herd tag tests'
    )
    def herd_tag(self) -> None:
        """clowder cats herd tag tests"""

        self._execute_command('./herd_tag.sh', self.path)

    @expose(
        help='Run cats herd tests'
    )
    def herd(self) -> None:
        """clowder cats herd tests"""

        self._execute_command('./herd.sh', self.path)

    @expose(
        help='Run cats init tests'
    )
    def init(self) -> None:
        """clowder cats init tests"""

        self._execute_command('./init.sh', self.path)

    @expose(
        help='Run cats link tests'
    )
    def link(self) -> None:
        """clowder cats link tests"""

        self._execute_command('./link.sh', self.path)

    @expose(
        help='Run cats lfs tests'
    )
    def lfs(self) -> None:
        """clowder cats lfs tests"""

        self._execute_command('./lfs.sh', self.path)

    @expose(
        help='Run cats prune tests'
    )
    def prune(self) -> None:
        """clowder cats prune tests"""

        self._execute_command('./prune.sh', self.path)

    @expose(
        help='Run cats repo tests'
    )
    def repo(self) -> None:
        """clowder cats repo tests"""

        self._execute_command('./repo.sh', self.path)

    @expose(
        help='Run cats reset tests'
    )
    def reset(self) -> None:
        """clowder cats reset tests"""

        self._execute_command('./reset.sh', self.path)

    @expose(
        help='Run cats save tests'
    )
    def save(self) -> None:
        """clowder cats save tests"""

        self._execute_command('./save.sh', self.path)

    @expose(
        help='Run cats start tests'
    )
    def start(self) -> None:
        """clowder cats start tests"""

        self._execute_command('./start.sh', self.path)

    @expose(
        help='Run cats stash tests'
    )
    def stash(self) -> None:
        """clowder cats stash tests"""

        self._execute_command('./stash.sh', self.path)

    @expose(
        help='Run cats status tests'
    )
    def status(self) -> None:
        """clowder cats status tests"""

        self._execute_command('./status.sh', self.path)

    @expose(
        help='Run cats subdirectory tests'
    )
    def subdirectory(self) -> None:
        """clowder cats subdirectory tests"""

        self._execute_command('./subdirectory.sh', self.path)

    @expose(
        help='Run cats yaml tests'
    )
    def yaml(self) -> None:
        """clowder cats yaml tests"""

        self._execute_command('./yaml.sh', self.path)

    @expose(
        help='Run cats yaml validation tests'
    )
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
