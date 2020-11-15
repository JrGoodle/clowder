"""Clowder console utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import sys
from io import StringIO

import rich.console

from typing import Any, List, Optional


class Console:
    """clowder console class"""

    def __init__(self):
        self.print_output: bool = True
        self._stdout: rich.console.Console = rich.console.Console(force_terminal=True,
                                                                  color_system='256')
        self._stderr: rich.console.Console = rich.console.Console(file=sys.stderr,
                                                                  force_terminal=True,
                                                                  color_system='256')
        self._stringio: rich.console.Console = rich.console.Console(file=StringIO())
        # for console in [self._stdout, self._stderr, self._stringio]:
        #     CONSOLE.stderr(console)
        #     print(console.encoding)
        #     print(console.color_system)
        #     print(console.width)
        #     print(console.is_terminal)
        #     print(console.is_dumb_terminal)
        self._error_messages: List[Any] = []

    def flush_errors(self, quiet: bool = False) -> None:
        if not quiet:
            for message in self._error_messages:
                self._stderr.log(message)
        self._error_messages = []

    def stderr(self, output: Any = '') -> None:
        if self.print_output:
            self._stderr.log(output)
        else:
            self._error_messages.append(output)

    def stdout(self, output: Any = '') -> None:
        if self.print_output:
            self._stdout.print(output)

    def print_exception(self) -> None:
        self._stderr.print_exception()

    def pretty_log_message(self, output: Any) -> str:
        self._stringio.print(output)
        output = self._stringio.file.getvalue()
        return output

    @property
    def pretty_traceback(self, error: Optional[BaseException] = None) -> str:
        if error is not None:
            self._stringio.print(error)
        else:
            self._stringio.print_exception()
        output = self._stringio.file.getvalue()
        return output

    @property
    def width(self) -> int:
        width = self._stdout.width
        return width


CONSOLE: Console = Console()
