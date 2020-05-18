# -*- coding: utf-8 -*-
"""Clowder command line repo controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse

import clowder.clowder_repo as clowder_repo
from clowder.util.clowder_utils import add_parser_arguments
from clowder.util.connectivity import network_connection_required
from clowder.util.decorators import (
    clowder_required,
    print_clowder_repo_status,
    print_clowder_repo_status_fetch
)


def add_repo_parser(subparsers: argparse._SubParsersAction) -> None: # noqa
    """Clowder repo command controller"""

    parser = subparsers.add_parser('repo', help='Manage clowder repo')
    repo_subparsers = parser.add_subparsers()

    add_repo_add_parser(repo_subparsers)
    add_repo_checkout_parser(repo_subparsers)
    add_repo_clean_parser(repo_subparsers)
    add_repo_commit_parser(repo_subparsers)
    add_repo_pull_parser(repo_subparsers)
    add_repo_push_parser(repo_subparsers)
    add_repo_run_parser(repo_subparsers)
    add_repo_status_parser(repo_subparsers)


def add_repo_add_parser(subparsers: argparse._SubParsersAction): # noqa
    """Clowder repo add command controller"""

    arguments = [
        (['files'], dict(nargs='+', metavar='FILE', help='files to add'))
    ]

    parser = subparsers.add_parser('add', help='Add files in clowder repo')
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=add)


def add_repo_checkout_parser(subparsers: argparse._SubParsersAction): # noqa
    """Clowder repo checkout command controller"""

    arguments = [
        (['ref'], dict(nargs=1, metavar='REF', help='git ref to checkout'))
    ]

    parser = subparsers.add_parser('checkout', help='Checkout ref in clowder repo')
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=checkout)


def add_repo_clean_parser(subparsers: argparse._SubParsersAction): # noqa
    """Clowder repo clean command controller"""

    parser = subparsers.add_parser('clean', help='Discard changes in clowder repo')
    parser.set_defaults(func=clean)


def add_repo_commit_parser(subparsers: argparse._SubParsersAction): # noqa
    """Clowder repo commit command controller"""

    arguments = [
        (['message'], dict(nargs=1, metavar='MESSAGE', help='commit message'))
    ]

    parser = subparsers.add_parser('commit', help='Commit current changes in clowder repo yaml files')
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=commit)


def add_repo_pull_parser(subparsers: argparse._SubParsersAction): # noqa
    """Clowder repo pull command controller"""

    parser = subparsers.add_parser('pull', help='Pull upstream changes in clowder repo')
    parser.set_defaults(func=pull)


def add_repo_push_parser(subparsers: argparse._SubParsersAction): # noqa
    """Clowder repo push command controller"""

    parser = subparsers.add_parser('push', help='Push changes in clowder repo')
    parser.set_defaults(func=push)


def add_repo_run_parser(subparsers: argparse._SubParsersAction): # noqa
    """Clowder repo run command controller"""

    arguments = [
        (['command'], dict(nargs=1, metavar='COMMAND', help='command to run in clowder repo directory'))
    ]

    parser = subparsers.add_parser('run', help='Run command in clowder repo')
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=run)


def add_repo_status_parser(subparsers: argparse._SubParsersAction): # noqa
    """Clowder repo status command controller"""

    parser = subparsers.add_parser('status', help='Print clowder repo git status')
    parser.set_defaults(func=status)


def add(args) -> None:
    """Clowder repo add command entry point"""

    _add(args)


@clowder_required
@print_clowder_repo_status
def _add(args) -> None:
    """Clowder repo add command private implementation"""

    clowder_repo.add(args.files)


def checkout(args) -> None:
    """Clowder repo checkout command entry point"""

    _checkout(args)


@clowder_required
@print_clowder_repo_status_fetch
def _checkout(args) -> None:
    """Clowder repo checkout command private implementation"""

    clowder_repo.checkout(args.ref[0])


def clean(args) -> None: # noqa
    """Clowder repo clean command entry point"""

    _clean()


@clowder_required
@print_clowder_repo_status
def _clean() -> None:
    """Clowder repo clean command private implementation"""

    clowder_repo.clean()


def commit(args) -> None:
    """Clowder repo commit command entry point"""

    _commit(args)


@clowder_required
@print_clowder_repo_status
def _commit(args) -> None:
    """Clowder repo commit command private implementation"""

    clowder_repo.commit(args.message[0])


def pull(args) -> None: # noqa
    """Clowder repo pull command entry point"""

    _pull()


@network_connection_required
@clowder_required
@print_clowder_repo_status_fetch
def _pull() -> None:
    """Clowder repo pull command private implementation"""

    clowder_repo.pull()


def push(args) -> None: # noqa
    """Clowder repo push command entry point"""

    _push()


@network_connection_required
@clowder_required
@print_clowder_repo_status_fetch
def _push() -> None:
    """Clowder repo push command private implementation"""

    clowder_repo.push()


def run(args) -> None:
    """Clowder repo run command entry point"""

    _run(args)


@clowder_required
@print_clowder_repo_status
def _run(args) -> None:
    """Clowder repo run command private implementation"""

    clowder_repo.run_command(args.command[0])


def status(args) -> None: # noqa
    """Clowder repo status command entry point"""

    _status()


@clowder_required
@print_clowder_repo_status
def _status() -> None:
    """Clowder repo status command private implementation"""

    clowder_repo.git_status()
