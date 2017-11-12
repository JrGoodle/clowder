# -*- coding: utf-8 -*-
"""Clowder test command line app

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import os

import colorama
from cement.core.foundation import CementApp

from clowder_test import ROOT_DIR
from clowder_test.cli.base_controller import BaseController
from clowder_test.cli.cats_controller import CatsController
from clowder_test.cli.cocos2d_controller import Cocos2dController
from clowder_test.cli.llvm_controller import LLVMController
from clowder_test.cli.swift_controller import SwiftController
from clowder_test.execute import execute_command


def post_argument_parsing_hook(app):
    execute_command('./setup_local_test_directory.sh', os.path.join(ROOT_DIR, 'test', 'scripts'))


class ClowderApp(CementApp):
    """Clowder command CLI app"""

    class Meta:
        """Clowder command CLI Meta configuration"""

        label = 'clowder'
        extensions = ['argcomplete']
        base_controller = 'base'
        hooks = [
            ('post_argument_parsing', post_argument_parsing_hook)
        ]
        handlers = [
            BaseController,
            CatsController,
            Cocos2dController,
            LLVMController,
            SwiftController
        ]


def main():
    """Clowder command CLI main function"""

    print()
    with ClowderApp() as app:
        app.run()


if __name__ == '__main__':
    colorama.init()
    main()
