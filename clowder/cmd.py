#! /usr/bin/env python3
"""Main entrypoint for clowder command"""
import argparse
import atexit
import os
import signal
import sys
import argcomplete
import colorama
from termcolor import cprint, colored
from clowder.clowder_repo import ClowderRepo
from clowder.clowder_controller import ClowderController
from clowder.utility.clowder_subparsers import configure_argparse
from clowder.utility.clowder_utilities import is_offline
from clowder.utility.print_utilities import print_offline_error

if __name__ == '__main__':
    raise SystemExit(main())

# Disable errors shown by pylint for no specified exception types
# pylint: disable=W0702
# Disable errors shown by pylint for too many public methods
# pylint: disable=R0904
# Disable errors shown by pylint for too many branches
# pylint: disable=R0912

class Command(object):
    """Command class for parsing commandline options"""

    def __init__(self):
        self.root_directory = os.getcwd()
        self.clowder = None
        self.clowder_repo = None
        self.versions = None
        self._invalid_yaml = False
        # Load current clowder.yml config if it exists
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
            except:
                self._invalid_yaml = True

        # clowder argparse setup
        command_description = 'Utility for managing multiple git repositories'
        parser = argparse.ArgumentParser(description=command_description,
                                         formatter_class=argparse.RawDescriptionHelpFormatter)
        configure_argparse(parser, self.clowder, self.versions)
        # Argcomplete and arguments parsing
        argcomplete.autocomplete(parser)
        if not self._invalid_yaml:
            print()
        # Register exit handler to display trailing newline
        self._display_trailing_newline = True
        atexit.register(self._exit_handler_formatter)
        self.args = parser.parse_args()
        self._display_trailing_newline = False

        if self.args.clowder_version:
            print('clowder version 2.3.0')
            sys.exit()
        if self.args.clowder_command is None or not hasattr(self, self.args.clowder_command):
            exit_unrecognized_command(parser)
        # use dispatch pattern to invoke method with same name
        getattr(self, self.args.clowder_command)()
        print()

    def branch(self):
        """clowder branch command"""
        if self._invalid_yaml:
            sys.exit(1)
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
        if self._invalid_yaml:
            sys.exit(1)
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
        if self._invalid_yaml:
            sys.exit(1)
        if self.clowder_repo is None:
            exit_clowder_not_found()
        self.clowder_repo.print_status()
        if self.clowder is None:
            sys.exit(1)
        self.clowder.diff(group_names=self.args.groups,
                          project_names=self.args.projects)

    def forall(self):
        """clowder forall command"""
        if self._invalid_yaml:
            sys.exit(1)
        if self.clowder_repo is None:
            exit_clowder_not_found()
        self.clowder_repo.print_status()
        if self.clowder is None:
            sys.exit(1)
        self.clowder.forall(self.args.command[0],
                            self.args.ignore_errors,
                            group_names=self.args.groups,
                            project_names=self.args.projects)

    def herd(self):
        """clowder herd command"""
        if self._invalid_yaml:
            sys.exit(1)
        if self.clowder_repo is None:
            exit_clowder_not_found()
        self.clowder_repo.print_status(fetch=True)
        if is_offline():
            print_offline_error()
        if self.clowder is None:
            sys.exit(1)

        if self.args.branch is None:
            branch = None
        else:
            branch = self.args.branch[0]

        if self.args.depth is None:
            depth = None
        else:
            depth = self.args.depth[0]

        self.clowder.herd(group_names=self.args.groups,
                          project_names=self.args.projects,
                          branch=branch,
                          depth=depth)

    def init(self):
        """clowder init command"""
        if self.clowder_repo is not None:
            cprint('Clowder already initialized in this directory\n', 'red')
            sys.exit(1)
        if is_offline():
            print_offline_error()
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
        if self._invalid_yaml:
            sys.exit(1)
        if self.clowder_repo is None:
            exit_clowder_not_found()
        self.clowder_repo.print_status()
        if self.clowder is None:
            sys.exit(1)
        if self.args.projects is None:
            if self.args.all:
                if is_offline():
                    print_offline_error()
                self.clowder.prune_groups(self.args.groups,
                                          self.args.branch,
                                          force=self.args.force,
                                          local=True,
                                          remote=True)
            elif self.args.remote:
                if is_offline():
                    print_offline_error()
                self.clowder.prune_groups(self.args.groups,
                                          self.args.branch,
                                          remote=True)
            else:
                self.clowder.prune_groups(self.args.groups,
                                          self.args.branch,
                                          force=self.args.force,
                                          local=True)
        else:
            if self.args.all:
                if is_offline():
                    print_offline_error()
                self.clowder.prune_projects(self.args.projects,
                                            self.args.branch,
                                            force=self.args.force,
                                            local=True,
                                            remote=True)
            elif self.args.remote:
                if is_offline():
                    print_offline_error()
                self.clowder.prune_projects(self.args.projects,
                                            self.args.branch,
                                            remote=True)
            else:
                self.clowder.prune_projects(self.args.projects,
                                            self.args.branch,
                                            force=self.args.force,
                                            local=True)

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
            print_offline_error()
        self.clowder_repo.print_status(fetch=True)
        self.clowder_repo.pull()

    def repo_push(self):
        """clowder repo push command"""
        if self.clowder_repo is None:
            exit_clowder_not_found()
        if is_offline():
            print_offline_error()
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
        self.clowder_repo.status()

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
        if self._invalid_yaml:
            sys.exit(1)
        if self.clowder_repo is None:
            exit_clowder_not_found()
        self.clowder_repo.print_status()
        if self.clowder is None:
            sys.exit(1)
        if self.args.tracking:
            if is_offline():
                print_offline_error()
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
        if self._invalid_yaml:
            sys.exit(1)
        if self.clowder_repo is None:
            exit_clowder_not_found()
        self.clowder_repo.print_status()
        if self.clowder is None:
            sys.exit(1)
        self.clowder.stash(group_names=self.args.groups,
                           project_names=self.args.projects)

    def status(self):
        """clowder status command"""
        if self.clowder_repo is None:
            exit_clowder_not_found()
        self.clowder_repo.print_status(fetch=self.args.fetch)
        if self.clowder is None:
            sys.exit(1)
        if self.args.fetch:
            if is_offline():
                print_offline_error()
            print(' - Fetch upstream changes for projects\n')
            self.clowder.fetch(self.clowder.get_all_group_names())
        all_project_paths = self.clowder.get_all_project_paths()
        padding = len(max(all_project_paths, key=len))
        self.clowder.status(self.clowder.get_all_group_names(), padding)

    def sync(self):
        """clowder sync command"""
        if self.clowder_repo is None:
            exit_clowder_not_found()
        self.clowder_repo.print_status(fetch=True)
        if self.clowder is None:
            sys.exit(1)
        if is_offline():
            print_offline_error()
        all_fork_projects = self.clowder.get_all_fork_project_names()
        if all_fork_projects is '':
            cprint(' - No forks to sync\n', 'red')
            sys.exit()
        self.clowder.sync(all_fork_projects)

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


def exit_unrecognized_command(parser):
    """Print unrecognized command message and exit"""
    parser.print_help()
    print()
    sys.exit(1)

def exit_clowder_not_found():
    """Print clowder not found message and exit"""
    cprint(' - No clowder found in the current directory\n', 'red')
    sys.exit(1)

def main():
    """Main entrypoint for clowder command"""
    signal.signal(signal.SIGINT, signal_handler)
    colorama.init()
    Command()

# Disable errors shown by pylint for unused arguments
# pylint: disable=W0613
def signal_handler(sig, frame):
    """Signal handler for Ctrl+C trap"""
    print()
    sys.exit(0)
