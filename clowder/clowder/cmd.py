"""Main entrypoint for clowder command"""

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
from clowder.util.connectivity import is_offline
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
        self._invalid_yaml = False
        self._version = '2.4.0'
        # Load current clowder.yaml config if it exists
        clowder_path = os.path.join(self.root_directory, '.clowder')
        if os.path.isdir(clowder_path):
            clowder_symlink = os.path.join(self.root_directory, 'clowder.yaml')
            self.clowder_repo = ClowderRepo(self.root_directory)
            if not os.path.islink(clowder_symlink):
                print()
                clowder_output = colored('.clowder', 'green')
                print(clowder_output)
                self.clowder_repo.link()
            try:
                self.clowder = ClowderController(self.root_directory)
                self.versions = self.clowder.get_saved_version_names()
            except (ClowderError, KeyError) as err:
                self._invalid_yaml = True
                self._error = err
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
        if not self._invalid_yaml:
            print()
        self.args = parser.parse_args()
        self._display_trailing_newline = False

        if self.args.clowder_command is None or not hasattr(self, self.args.clowder_command):
            exit_unrecognized_command(parser)
        # use dispatch pattern to invoke method with same name
        getattr(self, self.args.clowder_command)()
        print()

    def branch(self):
        """clowder branch command"""
        self._validate_clowder_yaml()
        if self.clowder_repo is None:
            exit_clowder_not_found()
        self.clowder_repo.print_status()
        if self.clowder is None:
            sys.exit(1)
        if self.args.all:
            self.clowder.branch(group_names=self.args.groups,
                                project_names=self.args.projects,
                                local=True,
                                remote=True)
        elif self.args.remote:
            self.clowder.branch(group_names=self.args.groups,
                                project_names=self.args.projects,
                                remote=True)
        else:
            self.clowder.branch(group_names=self.args.groups,
                                project_names=self.args.projects,
                                local=True)

    def clean(self):
        """clowder clean command"""
        self._validate_clowder_yaml()
        if self.clowder_repo is None:
            exit_clowder_not_found()
        self.clowder_repo.print_status()
        if self.clowder is None:
            sys.exit(1)
        if self.args.all:
            self.clowder.clean_all(group_names=self.args.groups,
                                   project_names=self.args.projects)
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
        self.clowder.clean(group_names=self.args.groups,
                           project_names=self.args.projects,
                           args=clean_args,
                           recursive=self.args.recursive)

    def diff(self):
        """clowder diff command"""
        self._validate_clowder_yaml()
        if self.clowder_repo is None:
            exit_clowder_not_found()
        self.clowder_repo.print_status()
        if self.clowder is None:
            sys.exit(1)
        self.clowder.diff(group_names=self.args.groups,
                          project_names=self.args.projects)

    def forall(self):
        """clowder forall command"""
        self._validate_clowder_yaml()
        if self.clowder_repo is None:
            exit_clowder_not_found()
        self.clowder_repo.print_status()
        if self.clowder is None:
            sys.exit(1)
        self.clowder.forall(self.args.command[0],
                            self.args.ignore_errors,
                            group_names=self.args.groups,
                            project_names=self.args.projects,
                            parallel=self.args.parallel)

    def herd(self):
        """clowder herd command"""
        self._validate_clowder_yaml()
        if self.clowder_repo is None:
            exit_clowder_not_found()
        self.clowder_repo.print_status(fetch=True)
        if is_offline():
            print(fmt.offline_error())
            sys.exit(1)
        if self.clowder is None:
            sys.exit(1)

        if self.args.branch is None:
            branch = None
        else:
            branch = self.args.branch[0]

        if self.args.tag is None:
            tag = None
        else:
            tag = self.args.tag[0]

        if self.args.depth is None:
            depth = None
        else:
            depth = self.args.depth[0]

        args = {'group_names': self.args.groups, 'project_names': self.args.projects,
                'branch': branch, 'tag': tag, 'depth': depth, 'rebase': self.args.rebase}
        if self.args.parallel:
            self.clowder.herd_parallel(**args)
            return
        self.clowder.herd(**args)

    def init(self):
        """clowder init command"""
        if self.clowder_repo:
            cprint('Clowder already initialized in this directory\n', 'red')
            sys.exit(1)
        if is_offline():
            print(fmt.offline_error())
            sys.exit(1)
        url_output = colored(self.args.url, 'green')
        print('Create clowder repo from ' + url_output + '\n')
        clowder_repo = ClowderRepo(self.root_directory)
        if self.args.branch is None:
            branch = 'master'
        else:
            branch = str(self.args.branch[0])
        clowder_repo.init(self.args.url, branch)

    def link(self):
        """clowder link command"""
        if self.clowder_repo is None:
            exit_clowder_not_found()
        self.clowder_repo.print_status()
        if self.args.version is None:
            version = None
        else:
            version = self.args.version[0]

        self.clowder_repo.link(version)

    def prune(self):
        """clowder prune command"""
        self._validate_clowder_yaml()
        if self.clowder_repo is None:
            exit_clowder_not_found()
        self.clowder_repo.print_status()
        if self.clowder is None:
            sys.exit(1)
        if self.args.projects is None:
            self._prune_groups()
        else:
            self._prune_projects()

    def repo(self):
        """clowder repo command"""
        if self.clowder_repo is None:
            exit_clowder_not_found()
        repo_command = 'repo_' + self.args.repo_command
        getattr(self, repo_command)()

    def repo_add(self):
        """clowder repo add command"""
        if self.clowder_repo is None:
            exit_clowder_not_found()
        self.clowder_repo.print_status()
        self.clowder_repo.add(self.args.files)

    def repo_checkout(self):
        """clowder repo checkout command"""
        if self.clowder_repo is None:
            exit_clowder_not_found()
        self.clowder_repo.print_status(fetch=True)
        self.clowder_repo.checkout(self.args.ref[0])

    def repo_clean(self):
        """clowder repo clean command"""
        if self.clowder_repo is None:
            exit_clowder_not_found()
        self.clowder_repo.print_status()
        self.clowder_repo.clean()

    def repo_commit(self):
        """clowder repo commit command"""
        if self.clowder_repo is None:
            exit_clowder_not_found()
        self.clowder_repo.print_status()
        self.clowder_repo.commit(self.args.message[0])

    def repo_pull(self):
        """clowder repo pull command"""
        if self.clowder_repo is None:
            exit_clowder_not_found()
        if is_offline():
            print(fmt.offline_error())
            sys.exit(1)
        self.clowder_repo.print_status(fetch=True)
        self.clowder_repo.pull()

    def repo_push(self):
        """clowder repo push command"""
        if self.clowder_repo is None:
            exit_clowder_not_found()
        if is_offline():
            print(fmt.offline_error())
            sys.exit(1)
        self.clowder_repo.print_status(fetch=True)
        self.clowder_repo.push()

    def repo_run(self):
        """clowder repo run command"""
        if self.clowder_repo is None:
            exit_clowder_not_found()
        self.clowder_repo.print_status()
        self.clowder_repo.run_command(self.args.command[0])

    def repo_status(self):
        """clowder repo status command"""
        if self.clowder_repo is None:
            exit_clowder_not_found()
        self.clowder_repo.print_status()
        self.clowder_repo.git_status()

    def reset(self):
        """clowder reset command"""
        self._validate_clowder_yaml()
        if self.clowder_repo is None:
            exit_clowder_not_found()
        self.clowder_repo.print_status(fetch=True)
        if is_offline():
            print(fmt.offline_error())
            sys.exit(1)
        if self.clowder is None:
            sys.exit(1)
        timestamp_project = None
        if self. args.timestamp:
            timestamp_project = self.args.timestamp[0]
        self.clowder.reset(group_names=self.args.groups,
                           project_names=self.args.projects,
                           timestamp_project=timestamp_project,
                           parallel=self.args.parallel)

    def save(self):
        """clowder save command"""
        if self.clowder_repo is None:
            exit_clowder_not_found()
        if self.clowder is None:
            sys.exit(1)
        self.clowder_repo.print_status()
        self.clowder.save_version(self.args.version)

    def start(self):
        """clowder start command"""
        self._validate_clowder_yaml()
        if self.clowder_repo is None:
            exit_clowder_not_found()
        self.clowder_repo.print_status()
        if self.clowder is None:
            sys.exit(1)
        if self.args.tracking:
            if is_offline():
                print(fmt.offline_error())
                sys.exit(1)
        if self.args.projects is None:
            self.clowder.start_groups(self.args.groups,
                                      self.args.branch,
                                      self.args.tracking)
        else:
            self.clowder.start_projects(self.args.projects,
                                        self.args.branch,
                                        self.args.tracking)

    def stash(self):
        """clowder stash command"""
        self._validate_clowder_yaml()
        if self.clowder_repo is None:
            exit_clowder_not_found()
        self.clowder_repo.print_status()
        if self.clowder is None:
            sys.exit(1)
        self.clowder.stash(group_names=self.args.groups,
                           project_names=self.args.projects)

    def status(self):
        """clowder status command"""
        self._validate_clowder_yaml()
        if self.clowder_repo is None:
            exit_clowder_not_found()
        self.clowder_repo.print_status(fetch=self.args.fetch)
        if self.clowder is None:
            sys.exit(1)
        if self.args.fetch:
            if is_offline():
                print(fmt.offline_error())
                sys.exit(1)
            print(' - Fetch upstream changes for projects\n')
            self.clowder.fetch(self.clowder.get_all_group_names())
        all_project_paths = self.clowder.get_all_project_paths()
        padding = len(max(all_project_paths, key=len))
        self.clowder.status(self.clowder.get_all_group_names(), padding)

    def sync(self):
        """clowder sync command"""
        self._validate_clowder_yaml()
        if self.clowder_repo is None:
            exit_clowder_not_found()
        self.clowder_repo.print_status(fetch=True)
        if self.clowder is None:
            sys.exit(1)
        if is_offline():
            print(fmt.offline_error())
            sys.exit(1)
        all_fork_projects = self.clowder.get_all_fork_project_names()
        if all_fork_projects == '':
            cprint(' - No forks to sync\n', 'red')
            sys.exit()
        self.clowder.sync(all_fork_projects, rebase=self.args.rebase, parallel=self.args.parallel)

    def version(self):
        """clowder version command"""
        print('clowder version ' + self._version + '\n')
        sys.exit()

    def yaml(self):
        """clowder yaml command"""
        if self.clowder_repo is None:
            exit_clowder_not_found()
        self.clowder_repo.print_status()
        if self._invalid_yaml:
            sys.exit(1)
        self.clowder.print_yaml(self.args.resolved)

    def _exit_handler_formatter(self):
        """Exit handler to display trailing newline"""
        if self._display_trailing_newline:
            print()

    def _prune_groups(self):
        """Private method for pruning groups"""
        if self.args.all:
            if is_offline():
                print(fmt.offline_error())
                sys.exit(1)
            self.clowder.prune_groups(self.args.groups,
                                      self.args.branch,
                                      force=self.args.force,
                                      local=True,
                                      remote=True)
        elif self.args.remote:
            if is_offline():
                print(fmt.offline_error())
                sys.exit(1)
            self.clowder.prune_groups(self.args.groups,
                                      self.args.branch,
                                      remote=True)
        else:
            self.clowder.prune_groups(self.args.groups,
                                      self.args.branch,
                                      force=self.args.force,
                                      local=True)

    def _prune_projects(self):
        """Private method for pruning projects"""
        if self.args.all:
            if is_offline():
                print(fmt.offline_error())
                sys.exit(1)
            self.clowder.prune_projects(self.args.projects,
                                        self.args.branch,
                                        force=self.args.force,
                                        local=True,
                                        remote=True)
        elif self.args.remote:
            if is_offline():
                print(fmt.offline_error())
                sys.exit(1)
            self.clowder.prune_projects(self.args.projects,
                                        self.args.branch,
                                        remote=True)
        else:
            self.clowder.prune_projects(self.args.projects,
                                        self.args.branch,
                                        force=self.args.force,
                                        local=True)

    def _validate_clowder_yaml(self):
        """Print invalid yaml message and exit if invalid"""
        if self._invalid_yaml:
            print(fmt.invalid_yaml_error())
            print(fmt.error(self._error))
            sys.exit(1)


def exit_unrecognized_command(parser):
    """Print unrecognized command message and exit"""
    parser.print_help()
    print()
    sys.exit(1)


def exit_clowder_not_found():
    """Print clowder not found message and exit"""
    cprint(' - No clowder found in the current directory\n', 'red')
    sys.exit(1)
