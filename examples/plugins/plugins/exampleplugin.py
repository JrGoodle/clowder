# -*- coding: utf-8 -*-
"""Example clowder plugin command

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function
from cement.ext.ext_argparse import ArgparseController, expose

from clowder.cli.globals import CLOWDER_CONTROLLER
from clowder.clowder_repo import (
    CLOWDER_REPO,
    print_clowder_repo_status
)
import clowder.util.formatting as fmt


# Disable errors shown by pylint for too few public methods
# pylint: disable=R0903


class ExamplePluginController(ArgparseController):
    """Example plugin command controller class"""

    class Meta:
        """Example plugin command Meta configuration"""

        label = 'exampleplugin'
        description = 'example plugin controller description'
        stacked_on = 'base'
        stacked_type = 'embedded'

    @expose(
        help="example plugin command description",
        arguments=[
            (['--foo'], dict(action='store', default='something', help='the infamous foo option'))
        ]
    )
    def mycommand(self):
        """Example plugin command entry point"""

        self._mycommand()

    @print_clowder_repo_status
    def _mycommand(self):
        """Example plugin command private implementation"""

        print("foo: " + self.app.pargs.foo + '\n')

        print("Clowder information")
        for group in CLOWDER_CONTROLLER.groups:
            print('\n' + fmt.group_name(group.name))
            print("Group name: " + group.name)
            print("Group depth default: " + str(group.depth))
            print("Group recursive default: " + str(group.recursive))
            print("Group timestamp author default: " + str(group.timestamp_author))
            print("Group ref default: " + group.ref)
            print("Group remote name default: " + group.remote_name)
            for project in group.projects:
                print("\nProject name: " + project.name)
                print("Project path: " + project.path)
                print("Project ref: " + project.ref)
                print("Project remote: " + project.remote)
                print("Project depth: " + str(project.depth))
                print("Project recursive: " + str(project.recursive))
                print("Source name: " + project.source.name)
                print("Source url: " + project.source.url)
                if project.fork:
                    print("Fork name: " + project.fork.name)
                    print("Fork path: " + project.fork.path)
                    print("Fork remote name: " + project.fork.remote_name)


def load(app):
    """Example plugin command load function"""

    app.handler.register(ExamplePluginController)
