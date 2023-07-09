"""command line app

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from .single_argument import SingleArgument


class CountArgument(SingleArgument):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, metavar='<n>', default=None, type=int, **kwargs)
