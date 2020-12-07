"""Clowder command line utils

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import Argument

from clowder.clowder_controller import CLOWDER_CONTROLLER


class ProjectsArgument(Argument):

    def __init__(self, help_msg: str, *args, **kwargs):
        super().__init__(
            'projects',
            metavar='<project|group>',
            default='default',
            nargs='*',
            choices=CLOWDER_CONTROLLER.project_choices_with_default,
            help=help_msg,
            *args, **kwargs
        )
