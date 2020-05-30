# -*- coding: utf-8 -*-
"""Clowder test command line app

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import colorama
from cement import App

from clowder_test import ROOT_DIR
from clowder_test.cli.base_controller import BaseController
from clowder_test.cli.cats_controller import CatsController
from clowder_test.cli.misc_controller import MiscController
from clowder_test.cli.swift_controller import SwiftController
from clowder_test.execute import execute_command


def post_argument_parsing_hook(app): # noqa
    execute_command('./setup_local_test_directory.sh', ROOT_DIR / 'test' / 'scripts')


class ClowderTestApp(App):
    """Clowder command CLI app"""

    class Meta:
        """Clowder command CLI Meta configuration"""

        label = 'clowder'
        base_controller = 'base'
        hooks = [
            ('post_argument_parsing', post_argument_parsing_hook)
        ]
        handlers = [
            BaseController,
            CatsController,
            MiscController,
            SwiftController
        ]


def main():
    """Clowder command CLI main function"""

    print()
    with ClowderTestApp() as app:
        app.run()


if __name__ == '__main__':
    colorama.init()
    main()
