"""Clowder command line repo controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import argparse

from pygoodle.cli import add_parser_arguments
from pygoodle.connectivity import network_connection_required

from clowder.clowder_controller import print_clowder_name
from clowder.environment import clowder_git_repo_required, clowder_repo_required, ENVIRONMENT
from clowder.git.clowder_repo import ClowderRepo, print_clowder_repo_status, print_clowder_repo_status_fetch


def add_repo_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa
    """Add clowder repo parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

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


def add_repo_add_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa
    """Add clowder repo add parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    parser = subparsers.add_parser('add', help='Add files in clowder repo')
    parser.set_defaults(func=add)

    add_parser_arguments(parser, [
        (['files'], dict(nargs='+', metavar='<file>', help='files to add'))
    ])


def add_repo_checkout_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa
    """Add clowder repo checkout parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    parser = subparsers.add_parser('checkout', help='Checkout ref in clowder repo')
    parser.set_defaults(func=checkout)

    add_parser_arguments(parser, [
        (['ref'], dict(nargs=1, metavar='<ref>', help='git ref to checkout'))
    ])


def add_repo_clean_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa
    """Add clowder repo clean parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    parser = subparsers.add_parser('clean', help='Discard changes in clowder repo')
    parser.set_defaults(func=clean)


def add_repo_commit_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa
    """Add clowder repo commit parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    parser = subparsers.add_parser('commit', help='Commit current changes in clowder repo yaml files')
    parser.set_defaults(func=commit)

    add_parser_arguments(parser, [
        (['message'], dict(nargs=1, metavar='<message>', help='commit message'))
    ])


def add_repo_pull_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa
    """Add clowder repo pull parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    parser = subparsers.add_parser('pull', help='Pull upstream changes in clowder repo')
    parser.set_defaults(func=pull)


def add_repo_push_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa
    """Add clowder repo push parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    parser = subparsers.add_parser('push', help='Push changes in clowder repo')
    parser.set_defaults(func=push)


def add_repo_run_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa
    """Add clowder repo run parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    parser = subparsers.add_parser('run', help='Run command in clowder repo')
    parser.set_defaults(func=run)

    add_parser_arguments(parser, [
        (['command'], dict(nargs=1, metavar='<command>', help='command to run in clowder repo directory'))
    ])


def add_repo_status_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa
    """Add clowder repo status parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    parser = subparsers.add_parser('status', help='Print clowder repo git status')
    parser.set_defaults(func=status)


@print_clowder_name
@clowder_git_repo_required
@print_clowder_repo_status
def add(args) -> None:
    """Clowder repo add command private implementation"""

    ClowderRepo(ENVIRONMENT.clowder_git_repo_dir).add(args.files)


@print_clowder_name
@clowder_git_repo_required
@print_clowder_repo_status_fetch
def checkout(args) -> None:
    """Clowder repo checkout command private implementation"""

    ClowderRepo(ENVIRONMENT.clowder_git_repo_dir).checkout(args.ref[0])


@print_clowder_name
@clowder_git_repo_required
@print_clowder_repo_status
def clean(_) -> None:
    """Clowder repo clean command private implementation"""

    ClowderRepo(ENVIRONMENT.clowder_git_repo_dir).clean()


@print_clowder_name
@clowder_git_repo_required
@print_clowder_repo_status
def commit(args) -> None:
    """Clowder repo commit command private implementation"""

    ClowderRepo(ENVIRONMENT.clowder_git_repo_dir).commit(args.message[0])


@print_clowder_name
@clowder_git_repo_required
@network_connection_required
@print_clowder_repo_status_fetch
def pull(_) -> None:
    """Clowder repo pull command private implementation"""

    ClowderRepo(ENVIRONMENT.clowder_git_repo_dir).pull()


@print_clowder_name
@clowder_git_repo_required
@network_connection_required
@print_clowder_repo_status_fetch
def push(_) -> None:
    """Clowder repo push command private implementation"""

    ClowderRepo(ENVIRONMENT.clowder_git_repo_dir).push()


@print_clowder_name
@clowder_repo_required
@print_clowder_repo_status
def run(args) -> None:
    """Clowder repo run command private implementation"""

    ClowderRepo(ENVIRONMENT.clowder_repo_dir).run_command(args.command[0])


@print_clowder_name
@clowder_repo_required
@print_clowder_repo_status
def status(_) -> None:
    """Clowder repo status command entry point"""

    if ENVIRONMENT.clowder_git_repo_dir is not None:
        ClowderRepo(ENVIRONMENT.clowder_repo_dir).git_status()
