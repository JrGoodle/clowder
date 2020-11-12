"""Clowder console utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from rich import print
import rich.console

from typing import Any


class Console:
    """clowder console class"""

    def __init__(self):
        self.print_output: bool = True
        self._rich_console: rich.console.Console = rich.console.Console()

    def print(self, output: Any = '') -> None:
        if self.print_output:
            print(output)

    def print_exception(self) -> None:
        # https://stackoverflow.com/a/57859075
        self._rich_console.print_exception()


CONSOLE: Console = Console()
