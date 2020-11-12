"""Clowder console utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from rich import print

from typing import Any


class Console:
    """clowder console class"""

    def __init__(self):
        self.print_output: bool = True

    def print(self, output: Any = '') -> None:
        if self.print_output:
            print(output)


CONSOLE: Console = Console()
