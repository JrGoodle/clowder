"""command line app

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import argparse
import pkg_resources
import sys
from subprocess import CalledProcessError
from typing import Any, List, Optional, Type, Union

import argcomplete
import pygoodle.reflection as reflect
from trio import MultiError

from ..console import CONSOLE
from .argument import Argument
from .argument_group import ArgumentGroup
from .mutually_exclusive_argument_group import MutuallyExclusiveArgumentGroup
from .subcommand import Subcommand

Parser = Union[argparse.ArgumentParser, argparse._MutuallyExclusiveGroup, argparse._ArgumentGroup]  # noqa


class App:

    class Meta:
        name: str = 'command'
        entry_point: str = 'command'
        args: List[Argument] = []
        mutually_exclusive_args: List[MutuallyExclusiveArgumentGroup] = []
        argument_groups: List[ArgumentGroup] = []
        subcommands: List[Subcommand] = []

    def __init__(self):
        from rich.traceback import install
        install()
        import colorama
        colorama.init()

        self.name: str = 'command'
        self.entry_point: str = 'command'
        self.args: List[Argument] = []
        self.mutually_exclusive_args: List[MutuallyExclusiveArgumentGroup] = []
        self.argument_groups: List[ArgumentGroup] = []
        self.subcommands: List[Type[Subcommand]] = []
        self._update_meta()

        self.parser: argparse.ArgumentParser = self._create_parser()
        argcomplete.autocomplete(self.parser)
        self.parsed_args: Any = self.parser.parse_args()
        self.process_args()

    def main(self) -> None:
        """command CLI main function"""

        try:
            self.parsed_args.func(self.parsed_args)
        except CalledProcessError as err:
            CONSOLE.stderr('** CalledProcessError **')
            CONSOLE.stderr(err)
            exit(err.returncode)
        except MultiError as err:
            CONSOLE.stderr('** MultiError **')
            CONSOLE.stderr(err.exceptions)
            exit(1)
        except OSError as err:
            CONSOLE.stderr('** OSError **')
            CONSOLE.stderr(err)
            exit(err.errno)
        except SystemExit as err:
            if err.code == 0:
                exit()
            CONSOLE.stderr('** SystemExit **')
            CONSOLE.print_exception()
            exit(err.code)
        except KeyboardInterrupt:
            CONSOLE.stderr('** KeyboardInterrupt **')
            exit(1)
        except BaseException:  # noqa
            CONSOLE.stderr('** Unhandled exception **')
            CONSOLE.print_exception()
            exit(1)

    def process_args(self) -> None:
        pass

    @staticmethod
    def _add_parser_arguments(parser: Parser, arguments: List[Argument]) -> None:
        """Add arguments to parser

        :param Parser parser: Parser to add arguments to
        :param Arguments arguments: Arguments to add to parser
        """

        for argument in arguments:
            parser.add_argument(*argument.args, **argument.options)

    def _add_subcommand(self, subcommand: Subcommand, subparsers: Optional[argparse._SubParsersAction] = None) -> None:  # noqa
        """Add arguments to parser

        :param Subcommand subcommand: Subcommand object
        :param Optional subparsers: Parser to add subcommand to
        """

        subparsers = self.subparsers if subparsers is None else subparsers
        parser = subparsers.add_parser(subcommand.name, help=subcommand.help)
        subcommand.add_parser(parser)
        parser.formatter_class = argparse.RawTextHelpFormatter
        parser.set_defaults(func=subcommand.run)

        self._add_parser_arguments(parser, subcommand.args)

        for group in subcommand.mutually_exclusive_args:
            parser_group = parser.add_mutually_exclusive_group(**group.options)
            self._add_parser_arguments(parser_group, group.args)

        for group in subcommand.argument_groups:
            parser_group = parser.add_argument_group(title=group.title, **group.options)
            self._add_parser_arguments(parser_group, group.args)

        if subcommand.subcommands:
            command_subparsers = parser.add_subparsers(dest=f'{subcommand.name} subcommand', help=subcommand.help)
            for command in subcommand.subcommands:
                self._add_subcommand(command(), command_subparsers)

    def _create_parser(self) -> argparse.ArgumentParser:
        """Configure CLI parsers

        :return: Configured argument parser for command
        :rtype: argparse.ArgumentParser
        """

        def command_help(_):
            command_parser.print_help(file=sys.stderr)

        try:
            command_parser = argparse.ArgumentParser(prog=self.entry_point)
            if hasattr(self, 'run'):
                action = getattr(self, 'run')
            else:
                action = command_help
            command_parser.set_defaults(func=action)
            try:
                version_message = f"{self.entry_point} version {pkg_resources.require(self.name)[0].version}"
                self._add_parser_arguments(command_parser, [
                    Argument('-v', '--version', action='version', version=version_message, metavar=None)
                ])
            except:
                pass

            if self.args:
                self._add_parser_arguments(command_parser, self.args)

            for group in self.mutually_exclusive_args:
                parser_group = command_parser.add_mutually_exclusive_group(**group.options)
                self._add_parser_arguments(parser_group, group.args)

            for group in self.argument_groups:
                parser_group = command_parser.add_argument_group(title=group.title, **group.options)
                self._add_parser_arguments(parser_group, group.args)

            if self.subcommands:
                self.subparsers = command_parser.add_subparsers(dest=f'{self.entry_point} subcommand')
                for subcommand in self.subcommands:
                    self._add_subcommand(subcommand())

            return command_parser
        except Exception:
            CONSOLE.stderr('Failed to create parser')
            raise

    def _update_attr(self, name: str, meta: Meta) -> None:
        reflect.update_attr(self, name, meta)

    def _update_meta(self) -> None:
        classes = reflect.method_resolution_order(self, reverse=True)
        for cls in classes:
            meta = reflect.class_member(cls, 'Meta')
            if meta is not None:
                self._update_attr('name', meta)
                self._update_attr('entry_point', meta)
                self._update_attr('args', meta)
                self._update_attr('mutually_exclusive_args', meta)
                self._update_attr('argument_groups', meta)
                self._update_attr('subcommands', meta)
