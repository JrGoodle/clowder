#! /usr/bin/env python3
"""Main entrypoint for clowder command"""
import argparse
import os
import signal
import sys
import argcomplete
import colorama
from termcolor import cprint, colored
from clowder.clowder_repo import ClowderRepo
from clowder.clowder_controller import ClowderController
from clowder.utility.repeated_timer import RepeatedTimer

if __name__ == '__main__':
    raise SystemExit(main())

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
        # Load current clowder.yml config if it exists
        clowder_path = os.path.join(self.root_directory, '.clowder')
        if os.path.isdir(clowder_path):
            clowder_symlink = os.path.join(self.root_directory, 'clowder.yaml')
            self.clowder_repo = ClowderRepo(self.root_directory)
            if not os.path.islink(clowder_symlink):
                print('')
                clowder_output = colored('.clowder', 'green')
                print(clowder_output)
                self.clowder_repo.link()
            self.clowder = ClowderController(self.root_directory)
            self.versions = self.clowder.get_saved_version_names()
            if self.clowder.get_all_group_names() is not None:
                self.group_names = self.clowder.get_all_group_names()
            if self.clowder.get_all_project_names() is not None:
                self.project_names = self.clowder.get_all_project_names()
        # clowder argparse setup
        command_description = 'Utility for managing multiple git repositories'
        parser = argparse.ArgumentParser(description=command_description)
        parser.add_argument('--version', '-v', action='store_true',
                            dest='clowder_version', help='Print clowder version')
        subparsers = parser.add_subparsers(dest='clowder_command')
        self._configure_subparser_clean(subparsers)
        self._configure_subparser_forall(subparsers)
        self._configure_subparser_herd(subparsers)
        self._configure_subparser_init(subparsers)
        self._configure_subparser_link(subparsers)
        self._configure_subparser_prune(subparsers)
        self._configure_subparser_repo(subparsers)
        self._configure_subparser_save(subparsers)
        self._configure_subparser_start(subparsers)
        self._configure_subparser_stash(subparsers)
        self._configure_subparser_status(subparsers)
        # Argcomplete and arguments parsing
        argcomplete.autocomplete(parser)
        self.args = parser.parse_args()

        if self.args.clowder_version:
            print('clowder version 2.0.0')
            sys.exit()
        print('')
        if self.args.clowder_command is None or not hasattr(self, self.args.clowder_command):
            exit_unrecognized_command(parser)
        # use dispatch pattern to invoke method with same name
        getattr(self, self.args.clowder_command)()
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
                self.clowder.forall_groups_run(self.args.command[0],
                                               self.args.groups,
                                               self.args.ignore_errors)
            else:
                self.clowder.forall_projects_run(self.args.command[0],
                                                 self.args.projects,
                                                 self.args.ignore_errors)
        else:
            exit_clowder_not_found()

    def herd(self):
        """clowder herd command"""
        if self.clowder_repo is not None:
            self.clowder_repo.print_status()
            print('')

            # TODO: clowder herd -b
            # if self.args.branch is None:
            #     ref = None
            # else:
            #     ref = self.args.branch[0]
            ref = None

            if self.args.depth is None:
                depth = None
            else:
                depth = self.args.depth[0]

            if self.args.projects is None:
                if self.args.groups is None:
                    self.clowder.herd_groups(self.clowder.get_all_group_names(), ref, depth)
                else:
                    self.clowder.herd_groups(self.args.groups, ref, depth)
            else:
                self.clowder.herd_projects(self.args.projects, ref, depth)
        else:
            exit_clowder_not_found()

    def init(self):
        """clowder init command"""
        if self.clowder_repo is None:
            url_output = colored(self.args.url, 'green')
            print('Create clowder repo from ' + url_output)
            print('')
            clowder_repo = ClowderRepo(self.root_directory)
            clowder_repo.init(self.args.url, self.args.branch)
        else:
            cprint('Clowder already initialized in this directory', 'red')
            print('')
            sys.exit(1)

    def link(self):
        """clowder link command"""
        self.clowder_repo.print_status()

        if self.clowder_repo is not None:
            if self.args.version is None:
                version = None
            else:
                version = self.args.version[0]

            self.clowder_repo.link(version)
        else:
            exit_clowder_not_found()

    def prune(self):
        """clowder prune command"""
        if self.clowder_repo is not None:
            self.clowder_repo.print_status()
            print('')
            if self.args.projects is None:
                self.clowder.prune_groups(self.args.groups,
                                          self.args.branch,
                                          self.args.remote,
                                          self.args.force)
            else:
                self.clowder.prune_projects(self.args.projects,
                                            self.args.branch,
                                            self.args.remote,
                                            self.args.force)
        else:
            exit_clowder_not_found()

    def repo(self):
        """clowder repo command"""
        if self.clowder_repo is not None:
            self.clowder_repo.print_status()
            repo_command = 'repo_' + self.args.repo_command
            getattr(self, repo_command)()
        else:
            exit_clowder_not_found()

    def repo_add(self):
        """clowder repo add command"""
        if self.clowder_repo is not None:
            self.clowder_repo.add(self.args.files)
        else:
            exit_clowder_not_found()

    def repo_checkout(self):
        """clowder repo checkout command"""
        if self.clowder_repo is not None:
            self.clowder_repo.checkout(self.args.ref[0])
        else:
            exit_clowder_not_found()

    def repo_clean(self):
        """clowder repo clean command"""
        if self.clowder_repo is not None:
            self.clowder_repo.clean()
        else:
            exit_clowder_not_found()

    def repo_commit(self):
        """clowder repo commit command"""
        if self.clowder_repo is not None:
            self.clowder_repo.commit(self.args.message[0])
        else:
            exit_clowder_not_found()

    def repo_pull(self):
        """clowder repo pull command"""
        if self.clowder_repo is not None:
            self.clowder_repo.pull()
        else:
            exit_clowder_not_found()

    def repo_push(self):
        """clowder repo push command"""
        if self.clowder_repo is not None:
            self.clowder_repo.push()
        else:
            exit_clowder_not_found()

    def repo_run(self):
        """clowder repo run command"""
        if self.clowder_repo is not None:
            self.clowder_repo.run_command(self.args.cmd[0])
        else:
            exit_clowder_not_found()

    def repo_status(self):
        """clowder repo status command"""
        if self.clowder_repo is not None:
            self.clowder_repo.status()
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
                self.clowder.start_groups(self.args.groups, self.args.branch)
            else:
                self.clowder.start_projects(self.args.projects, self.args.branch)
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
            if self.args.fetch:
                print(' - Fetching upstream changes for projects', end="", flush=True)
                timer = RepeatedTimer(1, self._print_progress)
                if self.args.projects is None:
                    self.clowder.fetch_groups(self.args.groups)
                else:
                    self.clowder.fetch_projects(self.args.projects)
                timer.stop()
                print('\n')
            if self.args.projects is None:
                self.clowder.status_groups(self.args.groups, self.args.verbose)
            else:
                self.clowder.status_projects(self.args.projects, self.args.verbose)
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
        forall_help = 'Run command or script in project directories'
        parser_forall = subparsers.add_parser('forall', help=forall_help)
        parser_forall.add_argument('--ignore-errors', '-i', action='store_true',
                                   help='Ignore errors in command or script')
        group_forall_command = parser_forall.add_mutually_exclusive_group()
        group_forall_command.add_argument('--command', '-c', nargs=1,
                                          help='Command or script to run in project directories')
        group_forall_targets = parser_forall.add_mutually_exclusive_group()
        group_forall_targets.add_argument('--groups', '-g', choices=self.group_names,
                                          default=self.group_names, nargs='+',
                                          help='Groups to run command or script for')
        group_forall_targets.add_argument('--projects', '-p', choices=self.project_names,
                                          nargs='+', help='Projects to run command or script for')

    def _configure_subparser_herd(self, subparsers):
        """Configure clowder herd subparser and arguments"""
        # clowder herd
        herd_help = 'Clone and sync latest changes for projects'
        parser_herd = subparsers.add_parser('herd', help=herd_help)
        parser_herd.add_argument('--depth', '-d', default=None, type=int, nargs=1,
                                 help='Depth to herd')
        # TODO: clowder herd -b
        # parser_herd.add_argument('--branch', '-b', nargs=1, default=None, help='Branch to herd')
        group_herd = parser_herd.add_mutually_exclusive_group()
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
        parser_init.add_argument('--branch', '-b', default='master', nargs='?',
                                 help='Branch of repo containing clowder.yaml')

    def _configure_subparser_link(self, subparsers):
        """Configure clowder link subparser and arguments"""
        # clowder link
        parser_link = subparsers.add_parser('link', help='Symlink clowder.yaml version')
        parser_link.add_argument('--version', '-v', choices=self.versions, nargs=1,
                                 default=None, help='Version name to symlink')

    def _configure_subparser_prune(self, subparsers):
        """Configure clowder prune subparser and arguments"""
        # clowder prune
        parser_prune = subparsers.add_parser('prune', help='Prune old branch')
        parser_prune.add_argument('--force', '-f', action='store_true',
                                  help='Force prune branches')
        parser_prune.add_argument('branch', help='Name of branch to remove')
        parser_prune.add_argument('--remote', '-r', action='store_true',
                                  help='Prune remote branches')
        group_prune = parser_prune.add_mutually_exclusive_group()
        group_prune.add_argument('--groups', '-g', choices=self.group_names,
                                 default=self.group_names, nargs='+',
                                 help='Groups to prune branch for')
        group_prune.add_argument('--projects', '-p', choices=self.project_names,
                                 nargs='+', help='Projects to prune branch for')

    def _configure_subparser_repo(self, subparsers):
        """Configure clowder repo subparser and arguments"""
        # clowder repo
        parser_repo = subparsers.add_parser('repo', help='Manage clowder repo')
        repo_subparsers = parser_repo.add_subparsers(dest='repo_command')
        # clowder repo add
        repo_add_help = 'Add files in clowder repo'
        parser_repo_add = repo_subparsers.add_parser('add', help=repo_add_help)
        parser_repo_add.add_argument('files', nargs='+', help='Files to add')
        # clowder repo checkout
        repo_checkout_help = 'Checkout ref in clowder repo'
        parser_repo_checkout = repo_subparsers.add_parser('checkout', help=repo_checkout_help)
        parser_repo_checkout.add_argument('ref', nargs=1, help='Git ref to checkout')
        # clowder repo clean
        repo_clean_help = 'Discard changes in clowder repo'
        repo_subparsers.add_parser('clean', help=repo_clean_help)
        # clowder repo commit
        repo_commit_help = 'Commit current changes in clowder repo yaml files'
        parser_repo_commit = repo_subparsers.add_parser('commit', help=repo_commit_help)
        parser_repo_commit.add_argument('message', nargs=1, help='Commit message')
        # clowder repo run
        repo_run_help = 'Run command in clowder repo'
        parser_repo_run = repo_subparsers.add_parser('run', help=repo_run_help)
        repo_run_command_help = 'Command to run in clowder repo directory'
        parser_repo_run.add_argument('cmd', nargs=1, help=repo_run_command_help)
        # clowder repo pull
        repo_pull_help = 'Pull upstream changes in clowder repo'
        repo_subparsers.add_parser('pull', help=repo_pull_help)
        # clowder repo push
        repo_subparsers.add_parser('push', help='Push changes in clowder repo')
        # clowder repo status
        repo_subparsers.add_parser('status', help='Print clowder repo git status')

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
        group_start = parser_start.add_mutually_exclusive_group()
        group_start.add_argument('--groups', '-g', choices=self.group_names,
                                 default=self.group_names, nargs='+',
                                 help='Groups to start feature for')
        group_start.add_argument('--projects', '-p', choices=self.project_names,
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
        parser_status.add_argument('--fetch', '-f', action='store_true',
                                   help='Fetch projects before printing status')
        parser_status.add_argument('--verbose', '-v', action='store_true',
                                   help='Print detailed diff status')
        group_status = parser_status.add_mutually_exclusive_group()
        group_status.add_argument('--groups', '-g', choices=self.group_names,
                                  default=self.group_names, nargs='+',
                                  help='Groups to print status for')
        group_status.add_argument('--projects', '-p', choices=self.project_names,
                                  nargs='+', help='Projects to print status for')


    def _print_progress(self):
        print('.', end="", flush=True)

def exit_unrecognized_command(parser):
    """Print unrecognized command message and exit"""
    parser.print_help()
    print('')
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
