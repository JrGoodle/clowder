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
    """Command class for parsing commandline options"""

    def __init__(self):
        self.root_directory = os.getcwd()
        self.clowder = None
        self.clowder_repo = None
        self.versions = None
        self.invalid_yaml = False
        self._version = '2.4.0'
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
        self.args = parser.parse_args()
        self._display_trailing_newline = False

        # Check for unrecognized command
        if self.args.clowder_command is None or not hasattr(self, self.args.clowder_command):
            exit_unrecognized_command(parser)

        # use dispatch pattern to invoke method with same name
        getattr(self, self.args.clowder_command)()
        print()

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def branch(self):
        """clowder branch command"""

        if self.args.all:
            self.clowder.branch(group_names=self.args.groups, project_names=self.args.projects,
                                skip=self.args.skip, local=True, remote=True)
            return

        if self.args.remote:
            self.clowder.branch(group_names=self.args.groups, project_names=self.args.projects,
                                skip=self.args.skip, remote=True)
            return

        self.clowder.branch(group_names=self.args.groups, project_names=self.args.projects,
                            skip=self.args.skip, local=True)

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def clean(self):
        """clowder clean command"""

        if self.args.all:
            self.clowder.clean_all(group_names=self.args.groups, project_names=self.args.projects,
                                   skip=self.args.skip)
            return

        clean_args = ''
        if self.args.d:
            clean_args += 'd'
        if self.args.f:
            clean_args += 'f'
        if self.args.X:
            clean_args += 'X'
        if self.args.x:
            clean_args += 'x'
        self.clowder.clean(group_names=self.args.groups, project_names=self.args.projects,
                           skip=self.args.skip, args=clean_args, recursive=self.args.recursive)

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def diff(self):
        """clowder diff command"""

        self.clowder.diff(group_names=self.args.groups, project_names=self.args.projects)

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def forall(self):
        """clowder forall command"""

        self.clowder.forall(self.args.command[0], self.args.ignore_errors,
                            group_names=self.args.groups, project_names=self.args.projects,
                            skip=self.args.skip, parallel=self.args.parallel)

    @network_connection_required
    @valid_clowder_yaml_required
    @print_clowder_repo_status_fetch
    def herd(self):
        """clowder herd command"""

        branch = None if self.args.branch is None else self.args.branch[0]
        tag = None if self.args.tag is None else self.args.tag[0]
        depth = None if self.args.depth is None else self.args.depth[0]

        args = {'group_names': self.args.groups, 'project_names': self.args.projects, 'skip': self.args.skip,
                'branch': branch, 'tag': tag, 'depth': depth, 'rebase': self.args.rebase}
        if self.args.parallel:
            self.clowder.herd_parallel(**args)
            return
        self.clowder.herd(**args)

    @network_connection_required
    def init(self):
        """clowder init command"""

        if self.clowder_repo:
            cprint('Clowder already initialized in this directory\n', 'red')
            sys.exit(1)

        url_output = colored(self.args.url, 'green')
        print('Create clowder repo from ' + url_output + '\n')
        clowder_repo = ClowderRepo(self.root_directory)
        if self.args.branch is None:
            branch = 'master'
        else:
            branch = str(self.args.branch[0])
        clowder_repo.init(self.args.url, branch)

    @clowder_required
    @print_clowder_repo_status
    def link(self):
        """clowder link command"""

        if self.args.version is None:
            version = None
        else:
            version = self.args.version[0]
        self.clowder_repo.link(version)

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def prune(self):
        """clowder prune command"""

        if self.args.all:
            self._prune_all()
            return

        if self.args.remote:
            self._prune_remote()
            return

        self.clowder.prune(self.args.groups, self.args.branch, project_names=self.args.projects,
                           skip=self.args.skip, force=self.args.force, local=True)

    @clowder_required
    def repo(self):
        """clowder repo command"""

        repo_command = 'repo_' + self.args.repo_command
        getattr(self, repo_command)()

    @clowder_required
    @print_clowder_repo_status
    def repo_add(self):
        """clowder repo add command"""

        self.clowder_repo.add(self.args.files)

    @clowder_required
    @print_clowder_repo_status_fetch
    def repo_checkout(self):
        """clowder repo checkout command"""

        self.clowder_repo.checkout(self.args.ref[0])

    @clowder_required
    @print_clowder_repo_status
    def repo_clean(self):
        """clowder repo clean command"""

        self.clowder_repo.clean()

    @clowder_required
    @print_clowder_repo_status
    def repo_commit(self):
        """clowder repo commit command"""

        self.clowder_repo.commit(self.args.message[0])

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

        self.clowder_repo.run_command(self.args.command[0])

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
        if self. args.timestamp:
            timestamp_project = self.args.timestamp[0]
        self.clowder.reset(group_names=self.args.groups, project_names=self.args.projects,
                           skip=self.args.skip, timestamp_project=timestamp_project, parallel=self.args.parallel)

    @valid_clowder_yaml_required
    def save(self):
        """clowder save command"""

        if self.args.version.lower() == 'default':
            print(fmt.save_default_error(self.args.version))
            sys.exit(1)

        self.clowder_repo.print_status()
        self.clowder.save_version(self.args.version)

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def start(self):
        """clowder start command"""

        if self.args.tracking:
            self._start_tracking()
            return

        if self.args.projects is None:
            self.clowder.start_groups(self.args.groups, self.args.skip, self.args.branch)
        else:
            self.clowder.start_projects(self.args.projects, self.args.skip, self.args.branch)

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def stash(self):
        """clowder stash command"""

        self.clowder.stash(group_names=self.args.groups, project_names=self.args.projects, skip=self.args.skip)

    @valid_clowder_yaml_required
    def status(self):
        """clowder status command"""

        self.clowder_repo.print_status(fetch=self.args.fetch)

        if self.args.fetch:
            self._fetch_clowder_projects()

        padding = len(max(self.clowder.get_all_project_paths(), key=len))
        self.clowder.status(self.clowder.get_all_group_names(), padding)

    @network_connection_required
    @valid_clowder_yaml_required
    @print_clowder_repo_status_fetch
    def sync(self):
        """clowder sync command"""

        all_fork_projects = self.clowder.get_all_fork_project_names()
        if all_fork_projects == '':
            cprint(' - No forks to sync\n', 'red')
            sys.exit()
        self.clowder.sync(all_fork_projects, rebase=self.args.rebase, parallel=self.args.parallel)

    def version(self):
        """clowder version command"""

        print('clowder version ' + self._version + '\n')
        sys.exit()

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def yaml(self):
        """clowder yaml command"""

        self.clowder.print_yaml(self.args.resolved)

    @network_connection_required
    def _fetch_clowder_projects(self):
        """fetch all projects"""

        print(' - Fetch upstream changes for projects\n')
        self.clowder.fetch(self.clowder.get_all_group_names())

    @network_connection_required
    def _prune_all(self):
        """clowder prune all command"""

        self.clowder.prune(self.args.groups, self.args.branch, project_names=self.args.projects,
                           skip=self.args.skip, force=self.args.force, local=True, remote=True)

    @network_connection_required
    def _prune_remote(self):
        """clowder prune remote command"""

        self.clowder.prune(self.args.groups, self.args.branch, project_names=self.args.projects,
                           skip=self.args.skip, remote=True)

    @network_connection_required
    def _start_tracking(self):
        """clowder start tracking command"""

        if self.args.projects is None:
            self.clowder.start_groups(self.args.groups, self.args.skip, self.args.branch, tracking=True)
        else:
            self.clowder.start_projects(self.args.projects, self.args.skip, self.args.branch, tracking=True)

    def _exit_handler_formatter(self):
        """Exit handler to display trailing newline"""

        if self._display_trailing_newline:
            print()


def exit_unrecognized_command(parser):
    """Print unrecognized command message and exit"""

    parser.print_help()
    print()
    sys.exit(1)
