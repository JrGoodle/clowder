# -*- coding: utf-8 -*-
"""Clowder command line base controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import ArgparseController, expose


VERSION = '2.5.0'


class BaseController(ArgparseController):
    """
    This is the application base controller, but we don't want to use our
    abstract base class here.

    """
    class Meta:
        label = 'base'
        arguments = [
            (['-v', '--version'], dict(action='version', version=VERSION)),
        ]

