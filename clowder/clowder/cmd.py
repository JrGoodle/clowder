# -*- coding: utf-8 -*-
"""Clowder command line entrypoint class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import argparse
import atexit
import os
import sys

import argcomplete
import colorama
from termcolor import cprint, colored

import clowder.commands as commands
import clowder.util.formatting as fmt
from clowder.clowder_controller import ClowderController
from clowder.clowder_repo import ClowderRepo
from clowder.error.clowder_error import ClowderError
from clowder.util.decorators import (
    clowder_required,
    print_clowder_repo_status,
    print_clowder_repo_status_fetch,
    network_connection_required,
    valid_clowder_yaml_required
)
from clowder.util.subparsers import configure_argparse


def main():
    """Main entrypoint for clowder command"""
    colorama.init()
    Command()


if __name__ == '__main__':
    raise SystemExit(main())


class Command(object):
    """Command class for parsing command line options

    :ivar str root_directory: Root directory of clowder projects
    :ivar ClowderController clowder: ClowderController instance
    :ivar ClowderRepo clowder_repo: ClowderRepo instance
    :ivar list[str] versions: List of all clowder.yaml versions
    :ivar bool invalid_yaml: Flag indicating whether current clowder.yaml is valid or invalid
    :ivar Exception error: Error associated with invalid yaml
    """

    def __init__(self):
        self.root_directory = os.getcwd()
        self.clowder = None
        self.clowder_repo = None
        self.versions = None
        self.invalid_yaml = False
        self._version = '2.5.0'
        clowder_path = os.path.join(self.root_directory, '.clowder')

        # Load current clowder.yaml config if it exists
        if os.path.isdir(clowder_path):
            clowder_symlink = os.path.join(self.root_directory, 'clowder.yaml')
            self.clowder_repo = ClowderRepo(self.root_directory)
            if not os.path.islink(clowder_symlink):
                cprint('\n.clowder', 'green')
                self.clowder_repo.link()
            try:
                self.clowder = ClowderController(self.root_directory)
                self.versions = self.clowder.get_saved_version_names()
            except (ClowderError, KeyError) as err:
                self.invalid_yaml = True
                self.error = err
            except (KeyboardInterrupt, SystemExit):
                sys.exit(1)

        # clowder argparse setup
        command_description = 'Utility for managing multiple git repositories'
        parser = argparse.ArgumentParser(description=command_description,
                                         formatter_class=argparse.RawDescriptionHelpFormatter)
        configure_argparse(parser, self.clowder, self.versions)

        # Argcomplete and arguments parsing
        argcomplete.autocomplete(parser)

        # Register exit handler to display trailing newline
        self._display_trailing_newline = True
        atexit.register(self._exit_handler_formatter)
        if not self.invalid_yaml:
            print()
        self._args = parser.parse_args()
        self._display_trailing_newline = False

        # Check for unrecognized command
        if self._args.clowder_command is None or not hasattr(self, self._args.clowder_command):
            exit_unrecognized_command(parser)

        # use dispatch pattern to invoke method with same name
        getattr(self, self._args.clowder_command)()
        print()

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def branch(self):
        """clowder branch command"""

        if self._args.all:
            commands.branch(self.clowder, group_names=self._args.groups, project_names=self._args.projects,
                            skip=self._args.skip, local=True, remote=True)
            return

        if self._args.remote:
            commands.branch(self.clowder, group_names=self._args.groups, project_names=self._args.projects,
                            skip=self._args.skip, remote=True)
            return

        commands.branch(self.clowder, group_names=self._args.groups, project_names=self._args.projects,
                        skip=self._args.skip, local=True)

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def checkout(self):
        """clowder checkout command"""

        commands.checkout(self.clowder, self._args.branch, group_names=self._args.groups,
                          project_names=self._args.projects)

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def clean(self):
        """clowder clean command"""

        if self._args.all:
            commands.clean_all(self.clowder, group_names=self._args.groups,
                               project_names=self._args.projects, skip=self._args.skip)
            return

        clean_args = ''
        if self._args.d:
            clean_args += 'd'
        if self._args.f:
            clean_args += 'f'
        if self._args.X:
            clean_args += 'X'
        if self._args.x:
            clean_args += 'x'
        commands.clean(self.clowder, group_names=self._args.groups, project_names=self._args.projects,
                       skip=self._args.skip, args=clean_args, recursive=self._args.recursive)

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def diff(self):
        """clowder diff command"""

        commands.diff(self.clowder, group_names=self._args.groups, project_names=self._args.projects)

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def forall(self):
        """clowder forall command"""

        commands.forall(self.clowder, self._args.command[0], self._args.ignore_errors,
                        group_names=self._args.groups, project_names=self._args.projects,
                        skip=self._args.skip, parallel=self._args.parallel)

    @network_connection_required
    @valid_clowder_yaml_required
    @print_clowder_repo_status_fetch
    def herd(self):
        """clowder herd command"""

        branch = None if self._args.branch is None else self._args.branch[0]
        tag = None if self._args.tag is None else self._args.tag[0]
        depth = None if self._args.depth is None else self._args.depth[0]

        kwargs = {'group_names': self._args.groups, 'project_names': self._args.projects, 'skip': self._args.skip,
                  'branch': branch, 'tag': tag, 'depth': depth, 'rebase': self._args.rebase}
        if self._args.parallel:
            commands.herd_parallel(self.clowder, **kwargs)
            return
        commands.herd(self.clowder, **kwargs)

    @network_connection_required
    def init(self):
        """clowder init command"""

        if self.clowder_repo:
            cprint('Clowder already initialized in this directory\n', 'red')
            sys.exit(1)

        url_output = colored(self._args.url, 'green')
        print('Create clowder repo from ' + url_output + '\n')
        clowder_repo = ClowderRepo(self.root_directory)
        if self._args.branch is None:
            branch = 'master'
        else:
            branch = str(self._args.branch[0])
        clowder_repo.init(self._args.url, branch)

    @clowder_required
    @print_clowder_repo_status
    def link(self):
        """clowder link command"""

        if self._args.version is None:
            version = None
        else:
            version = self._args.version[0]
        self.clowder_repo.link(version)

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def prune(self):
        """clowder prune command"""

        if self._args.all:
            self._prune_all()
            return

        if self._args.remote:
            self._prune_remote()
            return

        commands.prune(self.clowder, self._args.groups, self._args.branch,
                       project_names=self._args.projects,
                       skip=self._args.skip, force=self._args.force, local=True)

    @clowder_required
    def repo(self):
        """clowder repo command"""

        repo_command = 'repo_' + self._args.repo_command
        getattr(self, repo_command)()

    @clowder_required
    @print_clowder_repo_status
    def repo_add(self):
        """clowder repo add command"""

        self.clowder_repo.add(self._args.files)

    @clowder_required
    @print_clowder_repo_status_fetch
    def repo_checkout(self):
        """clowder repo checkout command"""

        self.clowder_repo.checkout(self._args.ref[0])

    @clowder_required
    @print_clowder_repo_status
    def repo_clean(self):
        """clowder repo clean command"""

        self.clowder_repo.clean()

    @clowder_required
    @print_clowder_repo_status
    def repo_commit(self):
        """clowder repo commit command"""

        self.clowder_repo.commit(self._args.message[0])

    @network_connection_required
    @clowder_required
    @print_clowder_repo_status_fetch
    def repo_pull(self):
        """clowder repo pull command"""

        self.clowder_repo.pull()

    @network_connection_required
    @clowder_required
    @print_clowder_repo_status_fetch
    def repo_push(self):
        """clowder repo push command"""

        self.clowder_repo.push()

    @clowder_required
    @print_clowder_repo_status
    def repo_run(self):
        """clowder repo run command"""

        self.clowder_repo.run_command(self._args.command[0])

    @clowder_required
    @print_clowder_repo_status
    def repo_status(self):
        """clowder repo status command"""

        self.clowder_repo.git_status()

    @network_connection_required
    @valid_clowder_yaml_required
    @print_clowder_repo_status_fetch
    def reset(self):
        """clowder reset command"""

        timestamp_project = None
        if self. _args.timestamp:
            timestamp_project = self._args.timestamp[0]
        commands.reset(self.clowder, group_names=self._args.groups, project_names=self._args.projects,
                       skip=self._args.skip, timestamp_project=timestamp_project, parallel=self._args.parallel)

    @valid_clowder_yaml_required
    def save(self):
        """clowder save command"""

        if self._args.version.lower() == 'default':
            print(fmt.save_default_error(self._args.version))
            sys.exit(1)

        self.clowder_repo.print_status()
        commands.save(self.clowder, self._args.version)

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def start(self):
        """clowder start command"""

        if self._args.tracking:
            self._start_tracking()
            return

        if self._args.projects is None:
            commands.start_groups(self.clowder, self._args.groups, self._args.skip, self._args.branch)
        else:
            commands.start_projects(self.clowder, self._args.projects, self._args.skip, self._args.branch)

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def stash(self):
        """clowder stash command"""

        commands.stash(self.clowder, group_names=self._args.groups,
                       project_names=self._args.projects, skip=self._args.skip)

    @valid_clowder_yaml_required
    def status(self):
        """clowder status command"""

        commands.status(self.clowder_repo, self.clowder, self._args.fetch)

    @network_connection_required
    @valid_clowder_yaml_required
    @print_clowder_repo_status_fetch
    def sync(self):
        """clowder sync command"""

        all_fork_projects = self.clowder.get_all_fork_project_names()
        if all_fork_projects == '':
            cprint(' - No forks to sync\n', 'red')
            sys.exit()
        commands.sync(self.clowder, all_fork_projects, rebase=self._args.rebase, parallel=self._args.parallel)

    def version(self):
        """clowder version command"""

        print('clowder version ' + self._version + '\n')
        sys.exit()

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def yaml(self):
        """clowder yaml command"""

        commands.yaml(self.clowder, self._args.resolved)

    @network_connection_required
    def _prune_all(self):
        """clowder prune all command"""

        commands.prune(self.clowder, self._args.groups, self._args.branch,
                       project_names=self._args.projects, skip=self._args.skip,
                       force=self._args.force, local=True, remote=True)

    @network_connection_required
    def _prune_remote(self):
        """clowder prune remote command"""

        commands.prune(self.clowder, self._args.groups, self._args.branch,
                       project_names=self._args.projects,
                       skip=self._args.skip, remote=True)

    @network_connection_required
    def _start_tracking(self):
        """clowder start tracking command"""

        if self._args.projects is None:
            commands.start_groups(self.clowder, self._args.groups, self._args.skip, self._args.branch, tracking=True)
            return

        commands.start_projects(self.clowder, self._args.projects, self._args.skip, self._args.branch, tracking=True)

    def _exit_handler_formatter(self):
        """Exit handler to display trailing newline"""

        if self._display_trailing_newline:
            print()


def exit_unrecognized_command(parser):
    """Print unrecognized command message and exit

    :param ArgumentParser parser: ArgParse parser
    """

    parser.print_help()
    print()
    sys.exit(1)
