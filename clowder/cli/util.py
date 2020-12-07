"""Clowder command line utils

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import Argument

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER


class ProjectsArgument(Argument):

    def __init__(self, help_msg: str, requires_arg: bool = False, *args, **kwargs):
        help_msg = fmt.project_options_help_message(help_msg)
        kwargs['metavar'] = '<project|group>'
        kwargs['choices'] = CLOWDER_CONTROLLER.project_choices_with_default,
        kwargs['help'] = help_msg
        projects = 'projects'
        if requires_arg:
            super().__init__(projects, nargs='+', *args, **kwargs)
        else:
            super().__init__(projects, default='default', nargs='*', *args, **kwargs)
