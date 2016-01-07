#! /usr/bin/env python3
"""Main entrypoint for clowder command"""

if __name__ == '__main__':
    raise SystemExit(main())

import argcomplete, argparse, colorama, os, signal, sys
from termcolor import cprint
from clowder.clowder_repo import ClowderRepo
from clowder.clowder_controller import ClowderController

# Disable errors shown by pylint for too many instance attributes
# pylint: disable=R0902
class Command(object):
    """Command class for parsing commandline options"""

    def __init__(self):
        self.root_directory = os.getcwd()
        self.clowder = None
        self.clowder_repo = None
        self.versions = None
        self.group_names = ''
        self.project_names = ''
        self.branches = ''
        # Load current clowder.yml config if it exists
        clowder_path = os.path.join(self.root_directory, '.clowder')
        if os.path.isdir(clowder_path):
            clowder_symlink = os.path.join(self.root_directory, 'clowder.yaml')
            self.clowder_repo = ClowderRepo(self.root_directory)
            if not os.path.islink(clowder_symlink):
                self.clowder_repo.symlink_yaml()
            self.clowder = ClowderController(self.root_directory)
            self.versions = self.clowder.get_saved_version_names()
            self.branches = self.clowder_repo.branches()
            if self.clowder.get_all_group_names() is not None:
                self.group_names = self.clowder.get_all_group_names()
            if self.clowder.get_all_project_names() is not None:
                self.project_names = self.clowder.get_all_project_names()
        # clowder argparse setup
        command_description = 'Utility for managing multiple git repositories'
        parser = argparse.ArgumentParser(description=command_description)
        parser.add_argument('--version', '-v', action='store_true',
                            dest='clowder_version', help='Print clowder version')
        subparsers = parser.add_subparsers(dest='command')
        self._configure_subparser_clean(subparsers)
        self._configure_subparser_forall(subparsers)
        self._configure_subparser_herd(subparsers)
        self._configure_subparser_init(subparsers)
        self._configure_subparser_repo(subparsers)
        self._configure_subparser_save(subparsers)
        self._configure_subparser_start(subparsers)
        self._configure_subparser_stash(subparsers)
        self._configure_subparser_status(subparsers)
        # Argcomplete and arguments parsing
        argcomplete.autocomplete(parser)
        self.args = parser.parse_args()

        if self.args.clowder_version:
            print('clowder version 0.9.0')
            sys.exit(0)
        print('')
        if self.args.command is None or not hasattr(self, self.args.command):
            exit_unrecognized_command(parser)
        # use dispatch pattern to invoke method with same name
        getattr(self, self.args.command)()
        print('')

    def clean(self):
        """clowder clean command"""
        if self.clowder_repo is not None:
            self.clowder_repo.print_status()
            print('')
            if self.args.projects is None:
                self.clowder.clean_groups(self.args.groups)
            else:
                self.clowder.clean_projects(self.args.projects)
        else:
            exit_clowder_not_found()

    def forall(self):
        """clowder forall command"""
        if self.clowder_repo is not None:
            self.clowder_repo.print_status()
            print('')
            if self.args.projects is None:
                self.clowder.forall_groups(self.args.cmd, self.args.groups)
            else:
                self.clowder.forall_projects(self.args.cmd, self.args.projects)
        else:
            exit_clowder_not_found()

    def herd(self):
        """clowder herd command"""
        if self.clowder_repo is not None:
            self.clowder_repo.print_status()
            self.clowder_repo.symlink_yaml(self.args.version)
            print('')
            clowder = ClowderController(self.root_directory)
            if self.args.projects is None:
                if self.args.groups is None:
                    clowder.herd_groups(clowder.get_all_group_names())
                else:
                    clowder.herd_groups(self.args.groups)
            else:
                clowder.herd_projects(self.args.projects)
        else:
            exit_clowder_not_found()

    def init(self):
        """clowder init command"""
        if self.clowder_repo is None:
            cprint('Init from %s\n' % self.args.url, 'yellow')
            clowder_repo = ClowderRepo(self.root_directory)
            clowder_repo.init(self.args.url)
        else:
            cprint('Clowder already bred in this directory', 'red')
            sys.exit()

    def repo(self):
        """clowder repo command"""
        if self.clowder_repo is not None:
            self.clowder_repo.print_status()
            print('')
            self.clowder_repo.run_command(self.args.cmd)
        else:
            exit_clowder_not_found()

    def save(self):
        """clowder save command"""
        if self.clowder_repo is not None:
            self.clowder.save_version(self.args.version)
        else:
            exit_clowder_not_found()

    def start(self):
        """clowder start command"""
        if self.clowder_repo is not None:
            self.clowder_repo.print_status()
            print('')
            if self.args.projects is None:
                if self.args.groups is None:
                    self.clowder.start_groups(self.clowder.get_all_group_names())
                else:
                    self.clowder.start_groups(self.args.groups)
            else:
                self.clowder.start_projects(self.args.projects)
        else:
            exit_clowder_not_found()

    def stash(self):
        """clowder stash command"""
        if self.clowder_repo is not None:
            self.clowder_repo.print_status()
            print('')
            if self.args.projects is None:
                self.clowder.stash_groups(self.args.groups)
            else:
                self.clowder.stash_projects(self.args.projects)
        else:
            exit_clowder_not_found()

    def status(self):
        """clowder status command"""
        if self.clowder_repo is not None:
            self.clowder_repo.print_status()
            print('')
            if self.args.verbose:
                self.clowder.status_verbose(self.args.groups)
            else:
                self.clowder.status(self.args.groups)
        else:
            exit_clowder_not_found()

# Disable errors shown by pylint for too many local variables
# pylint: disable=R0201
    def _configure_subparser_clean(self, subparsers):
        """Configure clowder clean subparser and arguments"""
        # clowder clean
        clean_help = 'Discard current changes in all projects'
        parser_clean = subparsers.add_parser('clean', help=clean_help)
        group_clean = parser_clean.add_mutually_exclusive_group()
        group_clean.add_argument('--groups', '-g', choices=self.group_names,
                                 default=self.group_names, nargs='+',
                                 help='Groups to clean')
        group_clean.add_argument('--projects', '-p', choices=self.project_names,
                                 nargs='+', help='Projects to clean')

    def _configure_subparser_forall(self, subparsers):
        """Configure clowder forall subparser and arguments"""
        # clowder forall
        forall_help = 'Run command in project directories'
        parser_forall = subparsers.add_parser('forall', help=forall_help)
        parser_forall.add_argument('cmd', help='Command to run in project directories')
        group_forall = parser_forall.add_mutually_exclusive_group()
        group_forall.add_argument('--groups', '-g', choices=self.group_names,
                                  default=self.group_names, nargs='+',
                                  help='Groups to run command for')
        group_forall.add_argument('--projects', '-p', choices=self.project_names,
                                  nargs='+', help='Projects to run command for')

    def _configure_subparser_herd(self, subparsers):
        """Configure clowder herd subparser and arguments"""
        # clowder herd
        herd_help = 'Clone and sync latest changes for projects'
        parser_herd = subparsers.add_parser('herd', help=herd_help)
        group_herd = parser_herd.add_mutually_exclusive_group()
        group_herd.add_argument('--version', '-v', choices=self.versions,
                                help='Version name to herd')
        group_herd.add_argument('--groups', '-g', choices=self.group_names,
                                default=self.group_names, nargs='+', help='Groups to herd')
        group_herd.add_argument('--projects', '-p', choices=self.project_names,
                                nargs='+', help='Projects to herd')

    def _configure_subparser_init(self, subparsers):
        """Configure clowder init subparser and arguments"""
        # clowder init
        init_help = 'Clone repository to clowder directory and create clowder.yaml symlink'
        parser_init = subparsers.add_parser('init', help=init_help)
        parser_init.add_argument('url', help='URL of repo containing clowder.yaml')

    def _configure_subparser_repo(self, subparsers):
        """Configure clowder repo subparser and arguments"""
        # clowder repo
        repo_help = 'Run command in project directories'
        parser_repo = subparsers.add_parser('repo', help=repo_help)
        parser_repo.add_argument('cmd', help='Command to run in project directories')

    def _configure_subparser_save(self, subparsers):
        """Configure clowder save subparser and arguments"""
        # clowder save
        save_help = 'Create version of clowder.yaml for current repos'
        parser_save = subparsers.add_parser('save', help=save_help)
        parser_save.add_argument('version', help='Version name to save')

    def _configure_subparser_start(self, subparsers):
        """Configure clowder start subparser and arguments"""
        # clowder start
        parser_start = subparsers.add_parser('start', help='Start a new feature')
        parser_start.add_argument('branch', help='Name of branch to create')
        parser_start.add_argument('--groups', '-g', choices=self.group_names,
                                  default=self.group_names, nargs='+',
                                  help='Groups to start feature for')
        parser_start.add_argument('--projects', '-p', choices=self.project_names,
                                  nargs='+', help='Projects to start feature for')

    def _configure_subparser_stash(self, subparsers):
        """Configure clowder stash subparser and arguments"""
        # clowder stash
        parser_stash = subparsers.add_parser('stash',
                                             help='Stash current changes')
        group_stash = parser_stash.add_mutually_exclusive_group()
        group_stash.add_argument('--groups', '-g', choices=self.group_names,
                                 default=self.group_names, nargs='+',
                                 help='Groups to stash')
        group_stash.add_argument('--projects', '-p', choices=self.project_names,
                                 nargs='+', help='Projects to stash')

    def _configure_subparser_status(self, subparsers):
        """Configure clowder status subparser and arguments"""
        # clowder status
        parser_status = subparsers.add_parser('status', help='Print project status')
        parser_status.add_argument('--verbose', '-v', action='store_true',
                                   help='Print detailed diff status')
        parser_status.add_argument('--groups', '-g', choices=self.group_names,
                                   default=self.group_names, nargs='+',
                                   help='Groups to print status for')

def exit_unrecognized_command(parser):
    """Print unrecognized command message and exit"""
    cprint('Unrecognized command\n', 'red')
    parser.print_help()
    sys.exit(1)

def exit_clowder_not_found():
    """Print clowder not found message and exit"""
    cprint('No clowder found in the current directory\n', 'red')
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
    print('')
    sys.exit(0)
