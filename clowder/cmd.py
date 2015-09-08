#! /usr/bin/env python3
"""Main entrypoint for clowder command"""

if __name__ == '__main__':
    raise SystemExit(main())

import argcomplete, argparse, colorama, os, signal, sys
from termcolor import cprint
from clowder.clowder_repo import ClowderRepo
from clowder.clowder_yaml import ClowderYAML
from clowder.utility.clowder_utilities import (
    print_clowder_repo_status,
    print_exiting
)

class Command(object):
    """Command class for parsing commandline options"""

    def __init__(self):
        self.root_directory = os.getcwd()
        self.clowder = None
        self.versions = None
        self.group_names = ''
        self.project_names = ''
        # Load current clowder.yml config if it exists
        if os.path.isdir(os.path.join(self.root_directory, 'clowder')):
            self.clowder = ClowderYAML(self.root_directory)
            self.versions = self.clowder.get_fixed_version_names()
            if self.clowder.get_all_group_names() is not None:
                self.group_names = self.clowder.get_all_group_names()
            if self.clowder.get_all_project_names() is not None:
                self.project_names = self.clowder.get_all_project_names()
        # clowder argparse setup
        command_description = 'Utility for managing multiple git repositories'
        parser = argparse.ArgumentParser(description=command_description)
        subparsers = parser.add_subparsers(dest='command')
        self._configure_subparsers(subparsers)
        # Argcomplete and arguments parsing
        argcomplete.autocomplete(parser)
        self.args = parser.parse_args()

        print('')
        if not hasattr(self, self.args.command):
            exit_unrecognized_command(parser)
        # use dispatch pattern to invoke method with same name
        getattr(self, self.args.command)()
        print('')

    def breed(self):
        """clowder breed command"""
        if self.clowder is None:
            cprint('Breed from %s\n' % self.args.url, 'yellow')
            clowder_repo = ClowderRepo(self.root_directory)
            clowder_repo.breed(self.args.url)
        else:
            cprint('Clowder already bred in this directory, exiting...\n', 'red')
            sys.exit()

    def fix(self):
        """clowder fix command"""
        if self.clowder is not None:
            cprint('Fix...\n', 'yellow')
            self.clowder.fix_version(self.args.version)
        else:
            exit_clowder_not_found()

    def forall(self):
        """clowder forall command"""
        if self.clowder is not None:
            cprint('Forall...\n', 'yellow')
            print_clowder_repo_status(self.root_directory)
            print('')
            self.clowder.forall(self.args.cmd, self.args.groups)
        else:
            exit_clowder_not_found()

    def groom(self):
        """clowder groom command"""
        if self.clowder is not None:
            cprint('Groom...\n', 'yellow')
            print_clowder_repo_status(self.root_directory)
            print('')
            if self.args.projects is None:
                self.clowder.groom_groups(self.args.groups)
            else:
                self.clowder.groom_projects(self.args.projects)
        else:
            exit_clowder_not_found()

    def herd(self):
        """clowder herd command"""
        if self.clowder is not None:
            cprint('Herd...\n', 'yellow')
            print_clowder_repo_status(self.root_directory)
            clowder_repo = ClowderRepo(self.root_directory)
            clowder_repo.symlink_yaml(self.args.version)
            print('')
            clowder = ClowderYAML(self.root_directory)
            if self.args.projects is None:
                clowder.herd_groups(self.args.groups)
            else:
                clowder.herd_projects(self.args.projects)
        else:
            exit_clowder_not_found()

    def meow(self):
        """clowder meow command"""
        if self.clowder is not None:
            cprint('Meow...\n', 'yellow')
            print_clowder_repo_status(self.root_directory)
            print('')
            if self.args.verbose:
                self.clowder.meow_verbose(self.args.groups)
            else:
                self.clowder.meow(self.args.groups)
        else:
            exit_clowder_not_found()

    def stash(self):
        """clowder stash command"""
        if self.clowder is not None:
            cprint('Stash...\n', 'yellow')
            print_clowder_repo_status(self.root_directory)
            print('')
            if self.args.projects is None:
                self.clowder.stash_groups(self.args.groups)
            else:
                self.clowder.stash_projects(self.args.projects)
        else:
            exit_clowder_not_found()

    def sync(self):
        """clowder sync command"""
        if self.clowder is not None:
            cprint('Sync...\n', 'yellow')
            print_clowder_repo_status(self.root_directory)
            print('')
            clowder_repo = ClowderRepo(self.root_directory)
            clowder_repo.sync()
        else:
            exit_clowder_not_found()

# Disable errors shown by pylint for unused arguments
# pylint: disable=R0914
    def _configure_subparsers(self, subparsers):
        """Configure all clowder command subparsers and arguments"""
        # clowder breed
        breed_help = 'Clone repository to clowder directory and create clowder.yaml symlink'
        parser_breed = subparsers.add_parser('breed', help=breed_help)
        parser_breed.add_argument('url', help='URL of repo containing clowder.yaml')
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
        # clowder forall
        forall_help = 'Run command in project directories'
        parser_forall = subparsers.add_parser('forall', help=forall_help)
        parser_forall.add_argument('cmd', help='Command to run in project directories')
        parser_forall.add_argument('--groups', '-g', choices=self.group_names,
                                   default=self.group_names, nargs='+',
                                   help='Groups to run command for')
        # clowder meow
        parser_meow = subparsers.add_parser('meow', help='Print status for projects')
        parser_meow.add_argument('--verbose', '-v', action='store_true',
                                 help='Print detailed diff status')
        parser_meow.add_argument('--groups', '-g', choices=self.group_names,
                                 default=self.group_names, nargs='+',
                                 help='Groups to print status for')
        # clowder fix
        fix_help = 'Create version of clowder.yaml for current repos'
        parser_fix = subparsers.add_parser('fix', help=fix_help)
        parser_fix.add_argument('version', help='Version name to fix')
        # clowder groom
        groom_help = 'Discard current changes in all projects'
        parser_groom = subparsers.add_parser('groom', help=groom_help)
        group_groom = parser_groom.add_mutually_exclusive_group()
        group_groom.add_argument('--groups', '-g', choices=self.group_names,
                                 default=self.group_names, nargs='+',
                                 help='Groups to groom')
        group_groom.add_argument('--projects', '-p', choices=self.project_names,
                                 nargs='+', help='Projects to groom')
        # clowder stash
        parser_stash = subparsers.add_parser('stash',
                                             help='Stash current changes in all projects')
        group_stash = parser_stash.add_mutually_exclusive_group()
        group_stash.add_argument('--groups', '-g', choices=self.group_names,
                                 default=self.group_names, nargs='+',
                                 help='Groups to stash')
        group_stash.add_argument('--projects', '-p', choices=self.project_names,
                                 nargs='+', help='Projects to stash')
        # clowder sync
        subparsers.add_parser('sync', add_help=False, help='Sync clowder repo')

def main():
    """Main entrypoint for clowder command"""
    signal.signal(signal.SIGINT, signal_handler)
    colorama.init()
    Command()

def exit_unrecognized_command(parser):
    """Print unrecognized command message and exit"""
    cprint('Unrecognized command\n', 'red')
    parser.print_help()
    print_exiting()

def exit_clowder_not_found():
    """Print clowder not found message and exit"""
    cprint('No clowder found in the current directory, exiting...\n', 'red')
    print_exiting()

# Disable errors shown by pylint for unused arguments
# pylint: disable=W0613
def signal_handler(sig, frame):
    """Signal handler for Ctrl+C trap"""
    print('')
    sys.exit(0)
