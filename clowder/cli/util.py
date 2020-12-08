"""Clowder command line utils

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import Argument, CountArgument

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER


class JobsArgument(CountArgument):

    def __init__(self, positional: bool = False, *args, **kwargs):
        new_args = list(args)
        if positional:
            new_args = ['jobs'] + new_args
        else:
            new_args = ['--jobs', '-j'] + new_args
        new_kwargs = dict(
            kwargs,
            help='number of jobs to use running command in parallel'
        )
        super().__init__(
            *new_args,
            **new_kwargs
        )


class ProjectsArgument(Argument):

    def __init__(self, help_msg: str, requires_arg: bool = False, *args, **kwargs):
        new_kwargs = dict(
            kwargs,
            metavar='<project|group>',
            choices=CLOWDER_CONTROLLER.project_choices_with_default,
            help=fmt.project_options_help_message(help_msg)
        )
        new_args = ['projects'] + list(args)
        if requires_arg:
            new_kwargs = dict(
                new_kwargs,
                nargs='+'
            )
            super().__init__(*new_args, **new_kwargs)
        else:
            new_kwargs = dict(
                new_kwargs,
                default='default',
                nargs='*'
            )
            super().__init__(*new_args, **new_kwargs)
