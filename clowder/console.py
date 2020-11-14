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
        self._stdout: rich.console.Console = rich.console.Console()
        self._stderr: rich.console.Console = rich.console.Console(file=sys.stderr)
        self._stringio: rich.console.Console = rich.console.Console(file=StringIO())
        self._error_messages: List[Any] = []

    def stderr(self, output: Any = '') -> None:
        if self.print_output:
            self._stderr.log(output)
        else:
            self._error_messages.append(output)

    def flush_errors(self, quiet: bool = False) -> None:
        if not quiet:
            for message in self._error_messages:
                self._stderr.log(message)
        self._error_messages = []

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


CONSOLE: Console = Console()
