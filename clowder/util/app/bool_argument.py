"""command line app

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from .argument import Argument


class BoolArgument(Argument):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, action='store_true', metavar=None, **kwargs)
