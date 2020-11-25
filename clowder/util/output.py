"""abode output utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import clowder.util.formatting as fmt
from clowder.util.console import CONSOLE


def separator(message: str, character: str) -> None:
    sep = character * len(message)
    CONSOLE.stdout(fmt.bold(sep))


def h1(message: str, newline: bool = True) -> None:
    if newline:
        CONSOLE.stdout()
    CONSOLE.stdout(fmt.bold(message))
    separator(message, '=')


def h2(message: str, newline: bool = True) -> None:
    if newline:
        CONSOLE.stdout()
    CONSOLE.stdout(fmt.bold(message))
    separator(message, '-')


def h3(message: str, newline: bool = True) -> None:
    if newline:
        CONSOLE.stdout()
    CONSOLE.stdout(fmt.bold(fmt.underline(f'# {message}')))


def h4(message: str, newline: bool = True) -> None:
    if newline:
        CONSOLE.stdout()
    CONSOLE.stdout(fmt.bold(fmt.underline(f'## {message}')))


def h5(message: str, newline: bool = True) -> None:
    if newline:
        CONSOLE.stdout()
    CONSOLE.stdout(fmt.bold(fmt.underline(f'### {message}')))
