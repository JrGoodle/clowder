"""command line app

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from .argument import Argument


class SingleArgument(Argument):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, nargs=1, **kwargs)
