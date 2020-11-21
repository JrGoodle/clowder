"""Clowder console utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import sys
from io import StringIO
from typing import Any

from rich.console import Console as RichConsole


class Console:
    """clowder console class"""

    def __init__(self):
        self.print_output: bool = True
        self._stdout: RichConsole = RichConsole(force_terminal=True,
                                                # color_system='256',
                                                width=160)
        self._stderr: RichConsole = RichConsole(file=sys.stderr,
                                                force_terminal=True,
                                                # color_system='256',
                                                width=160)
        self._stringio: RichConsole = RichConsole(file=StringIO(),
                                                  width=160)
        # for console in [self._stdout, self._stderr, self._stringio]:
        #     CONSOLE.stderr(console)
        #     print(console.encoding)
        #     print(console.color_system)
        #     print(console.width)
        #     print(console.is_terminal)
        #     print(console.is_dumb_terminal)

    def stderr(self, output: Any = '') -> None:
        if self.print_output:
            self._stderr.log(output, log_locals=True)

    def stdout(self, output: Any = '') -> None:
        if self.print_output:
            self._stdout.print(output)

    def print_exception(self) -> None:
        if self.print_output:
            self._stderr.print_exception()

    @property
    def width(self) -> int:
        width = self._stdout.width
        return width

    def _pretty_log_message(self, output: Any) -> str:
        self._stringio.print(output)
        output = self._stringio.file.getvalue()
        return output

    @property
    def _pretty_traceback(self) -> str:
        self._stringio.print_exception()
        output = self._stringio.file.getvalue()
        return output


CONSOLE: Console = Console()
