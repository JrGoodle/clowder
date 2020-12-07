"""Clowder command line utils

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import Argument

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER


class JobsArgument(Argument):

    def __init__(self, *args, **kwargs):
        super().__init__(
            '--jobs', '-j',
            metavar='<n>',
            nargs=1,
            default=None,
            type=int,
            help='number of jobs to use running command in parallel',
            *args, **kwargs
        )


class ProjectsArgument(Argument):

    def __init__(self, help_msg: str, requires_arg: bool = False, *args, **kwargs):
        kwargs['metavar'] = '<project|group>'
        kwargs['choices'] = CLOWDER_CONTROLLER.project_choices_with_default,
        kwargs['help'] = fmt.project_options_help_message(help_msg)
        projects = 'projects'
        if requires_arg:
            super().__init__(projects, nargs='+', *args, **kwargs)
        else:
            super().__init__(projects, default='default', nargs='*', *args, **kwargs)
