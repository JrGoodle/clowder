# -*- coding: utf-8 -*-
"""Clowder test command line app

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from subprocess import CalledProcessError

import colorama
from cement import App

from clowder_test import ROOT_DIR
from clowder_test.cli.base_controller import BaseController
from clowder_test.cli.cats_controller import CatsController
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
            CatsController
        ]


def main():
    """Clowder command CLI main function"""

    print()
    try:
        with ClowderTestApp() as app:
            app.run()
    except CalledProcessError as err:
        print('CLOWDER_TEST: CalledProcessError')
        print(f"CLOWDER_TEST: {err}")
        print()
        exit(err.returncode)
    except Exception as err:
        print('CLOWDER_TEST: Exception')
        print(f"CLOWDER_TEST: {err}")
        print()
        exit(1)


if __name__ == '__main__':
    colorama.init()
    main()
