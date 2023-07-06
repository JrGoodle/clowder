"""command line app

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from typing import Any, Dict, Tuple

from ..format import Format


class Argument:

    def __init__(self, *args, **kwargs):
        self.args: Tuple[Any] = args

        # update metavar to default if missing or remove if None
        metavar = 'metavar'
        if metavar not in kwargs:
            name = self._get_name(args)
            kwargs[metavar] = f'<{name}>'
        elif metavar in kwargs and kwargs[metavar] is None:
            del kwargs[metavar]

        self.options: Dict[str, Any] = kwargs

    @staticmethod
    def _get_name(args: Tuple[Any]) -> str:
        names = [a for a in args if a.startswith('--')]
        if names:
            return Format.remove_prefix(names[0], '--')

        names = [a for a in args if a.startswith('-')]
        if names:
            return Format.remove_prefix(names[0], '-')

        names = [a for a in args if not a.startswith('-')]
        if names:
            return names[0]

        raise Exception('Failed to infer argument name')
