# -*- coding: utf-8 -*-
"""Clowder command line base controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import ArgparseController


VERSION = '3.0.0'


class BaseController(ArgparseController):
    """Clowder app base controller"""

    class Meta:
        """Clowder app base Meta configuration"""

        label = 'base'
        arguments = [
            (['-v', '--version'], dict(action='version', version=VERSION)),
        ]
