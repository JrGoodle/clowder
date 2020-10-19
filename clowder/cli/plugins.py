# -*- coding: utf-8 -*-
"""Clowder command line plugins controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse
import os
import importlib.util

from clowder.environment import ENVIRONMENT
from clowder.util.decorators import clowder_repo_required, valid_clowder_yaml_required

from .util import add_parser_arguments


def add_plugins_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa
    """Add clowder plugins parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    plugins_dir = ENVIRONMENT.clowder_repo_plugins_dir
    if plugins_dir is None:
        return
    dir_exists = plugins_dir.exists()
    is_dir = plugins_dir.is_dir()
    if not dir_exists or not is_dir:
        return

    files = os.listdir(plugins_dir)
    files = [ENVIRONMENT.clowder_repo_plugins_dir / f for f in files]
    plugins = [f for f in files if f.is_dir()]
    # TODO: Check for .py file
    if not plugins:
        return

    for plugin in plugins:
        # TODO: Add way to define help
        parser = subparsers.add_parser(plugin.name, help=f"Run {plugin.name} command")
        # parser.formatter_class = argparse.RawTextHelpFormatter
        add_parser_arguments(parser, [])
        parser.set_defaults(func=run)


@clowder_repo_required
@valid_clowder_yaml_required
def run(args) -> None:
    """Clowder plugins command private implementation"""

    plugins_dir = ENVIRONMENT.clowder_repo_plugins_dir

    plugin_name = args.subcommand
    module = f"{plugin_name}.{plugin_name}"
    module_file = plugins_dir / plugin_name / f"{plugin_name}.py"

    spec = importlib.util.spec_from_file_location(module, module_file)
    plugin = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(plugin)  # noqa
    plugin.main()  # noqa
