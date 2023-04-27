"""Clowder command line utils

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import Argument, CountArgument

import clowder.util.formatting as fmt
from clowder.controller import CLOWDER_CONTROLLER


class JobsArgument(CountArgument):

    def __init__(self, positional: bool = False, *args, **kwargs):
        if positional:
            command_args = ['jobs']
        else:
            command_args = ['--jobs', '-j']
        super().__init__(*command_args, *args, help='number of jobs to use running command in parallel', **kwargs)


class ProjectsArgument(Argument):

    def __init__(self, help_msg: str, requires_arg: bool = False, *args, **kwargs):
        args = ['projects'] + list(args)
        kwargs = dict(
            kwargs,
            metavar='<project|group>',
            choices=CLOWDER_CONTROLLER.project_choices_with_default,
            help=fmt.project_options_help_message(help_msg)
        )
        if requires_arg:
            super().__init__(*args, nargs='+', **kwargs)
        else:
            super().__init__(*args, default='default', nargs='*', **kwargs)
