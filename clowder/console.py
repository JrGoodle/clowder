"""Clowder console utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from io import StringIO

from rich import print
import rich.console

from typing import Any


class Console:
    """clowder console class"""

    def __init__(self):
        self.print_output: bool = True
        self._rich_console: rich.console.Console = rich.console.Console()
        self._rich_string_io_console: rich.console.Console = rich.console.Console(file=StringIO())

    def log(self, output: Any = '') -> None:
        self._rich_console.log(output)

    def print(self, output: Any = '') -> None:
        if self.print_output:
            print(output)

    def print_exception(self) -> None:
        self._rich_console.print_exception()

    def pretty_log_message(self, output: Any) -> str:
        self._rich_string_io_console.print(output)
        output = self._rich_string_io_console.file.getvalue()
        return output

    def pretty_traceback(self) -> str:
        self._rich_string_io_console.print_exception()
        output = self._rich_string_io_console.file.getvalue()
        return output


CONSOLE: Console = Console()
