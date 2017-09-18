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

if __name__ == '__main__':
    raise SystemExit(main())

# Disable errors shown by pylint for too many instance attributes
# pylint: disable=R0902
# Disable errors shown by pylint for no specified exception types
# pylint: disable=W0702
# Disable errors shown by pylint for too many statements
# pylint: disable=R0915
# Disable errors shown by pylint for TODO's
# pylint: disable=W0511

class Command(object):
    """Command class for parsing commandline options"""

    def __init__(self):
        self.root_directory = os.getcwd()
        self.clowder = None
        self.clowder_repo = None
        self.versions = None
        self.group_names = ''
        self.project_names = ''
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
                if self.clowder.get_all_group_names() is not None:
                    self.group_names = self.clowder.get_all_group_names()
                if self.clowder.get_all_project_names() is not None:
                    self.project_names = self.clowder.get_all_project_names()
            except:
                self._invalid_yaml = True

        # clowder argparse setup
        command_description = 'Utility for managing multiple git repositories'
        parser = argparse.ArgumentParser(description=command_description,
                                         formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('--version', '-v', action='store_true',
                            dest='clowder_version', help='print clowder version')
        subparsers = parser.add_subparsers(dest='clowder_command', metavar='SUBCOMMAND')
        self._configure_subparser_clean(subparsers)
        self._configure_subparser_diff(subparsers)
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
        if not self._invalid_yaml:
            print()
        # Register exit handler to display trailing newline
        self._display_trailing_newline = True
        atexit.register(self._exit_handler_formatter)
        self.args = parser.parse_args()
        self._display_trailing_newline = False

        if self.args.clowder_version:
            print('clowder version 2.1.0')
            sys.exit()
        if self.args.clowder_command is None or not hasattr(self, self.args.clowder_command):
            exit_unrecognized_command(parser)
        # use dispatch pattern to invoke method with same name
        getattr(self, self.args.clowder_command)()
        print()

    def clean(self):
        """clowder clean command"""
        if self._invalid_yaml:
            sys.exit(1)
        if self.clowder_repo is not None:
            self.clowder_repo.print_status()
            print()
            if self.clowder is None:
                sys.exit(1)
            if self.args.projects is None:
                self.clowder.clean_groups(self.args.groups)
            else:
                self.clowder.clean_projects(self.args.projects)
        else:
            exit_clowder_not_found()

    def diff(self):
        """clowder diff command"""
        if self._invalid_yaml:
            sys.exit(1)
        if self.clowder_repo is not None:
            self.clowder_repo.print_status()
            print()
            if self.clowder is None:
                sys.exit(1)
            if self.args.projects is None:
                self.clowder.diff_groups(self.args.groups)
            else:
                self.clowder.diff_projects(self.args.projects)
        else:
            exit_clowder_not_found()

    def forall(self):
        """clowder forall command"""
        if self._invalid_yaml:
            sys.exit(1)
        if self.clowder_repo is not None:
            self.clowder_repo.print_status()
            print()
            if self.clowder is None:
                sys.exit(1)
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
        if self._invalid_yaml:
            sys.exit(1)
        if self.clowder_repo is not None:
            self.clowder_repo.print_status()
            print()
            if self.clowder is None:
                sys.exit(1)

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
            print()
            clowder_repo = ClowderRepo(self.root_directory)
            if self.args.branch is None:
                branch = 'master'
            else:
                branch = str(self.args.branch[0])
            clowder_repo.init(self.args.url, branch)
        else:
            cprint('Clowder already initialized in this directory', 'red')
            print()
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
        if self._invalid_yaml:
            sys.exit(1)
        if self.clowder_repo is not None:
            self.clowder_repo.print_status()
            print()
            if self.clowder is None:
                sys.exit(1)
            if self.args.projects is None:
                if self.args.all:
                    self.clowder.prune_groups_all(self.args.groups,
                                                  self.args.branch,
                                                  self.args.force)
                elif self.args.remote:
                    self.clowder.prune_groups_remote(self.args.groups,
                                                     self.args.branch)
                else:
                    self.clowder.prune_groups_local(self.args.groups,
                                                    self.args.branch,
                                                    self.args.force)
            else:
                if self.args.all:
                    self.clowder.prune_projects_all(self.args.projects,
                                                    self.args.branch,
                                                    self.args.force)
                elif self.args.remote:
                    self.clowder.prune_projects_remote(self.args.projects,
                                                       self.args.branch)
                else:
                    self.clowder.prune_projects_local(self.args.projects,
                                                      self.args.branch,
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
            self.clowder_repo.run_command(self.args.command[0])
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
            if self.clowder is None:
                sys.exit(1)
            self.clowder.save_version(self.args.version)
        else:
            exit_clowder_not_found()

    def start(self):
        """clowder start command"""
        if self._invalid_yaml:
            sys.exit(1)
        if self.clowder_repo is not None:
            self.clowder_repo.print_status()
            print()
            if self.clowder is None:
                sys.exit(1)
            if self.args.projects is None:
                self.clowder.start_groups(self.args.groups,
                                          self.args.branch,
                                          self.args.tracking)
            else:
                self.clowder.start_projects(self.args.projects,
                                            self.args.branch,
                                            self.args.tracking)
        else:
            exit_clowder_not_found()

    def stash(self):
        """clowder stash command"""
        if self._invalid_yaml:
            sys.exit(1)
        if self.clowder_repo is not None:
            self.clowder_repo.print_status()
            print()
            if self.clowder is None:
                sys.exit(1)
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
            print()
            if self.clowder is None:
                sys.exit(1)
            if self.args.fetch:
                print(' - Fetch upstream changes for projects')
                print()
                if self.args.projects is None:
                    self.clowder.fetch_groups(self.args.groups)
                else:
                    self.clowder.fetch_projects(self.args.projects)
                print()
            if self.args.projects is None:
                self.clowder.status_groups(self.args.groups)
            else:
                self.clowder.status_projects(self.args.projects)
        else:
            exit_clowder_not_found()

# Disable errors shown by pylint for too many local variables
# pylint: disable=R0201
    def _configure_subparser_clean(self, subparsers):
        """Configure clowder clean subparser and arguments"""
        # clowder clean
        clean_help = 'Discard current changes in projects'
        parser_clean = subparsers.add_parser('clean', help=clean_help)
        group_clean = parser_clean.add_mutually_exclusive_group()
        if self.group_names is not '':
            clean_help_groups = '''
                                 groups to clean:
                                 {0}
                                 '''
            clean_help_groups = clean_help_groups.format(', '.join(self.group_names))
        else:
            clean_help_groups = 'groups to clean'
        group_clean.add_argument('--groups', '-g', choices=self.group_names,
                                 default=self.group_names, nargs='+',
                                 help=clean_help_groups, metavar='GROUP')
        if self.project_names is not '':
            clean_help_projects = '''
                                   projects to clean:
                                   {0}
                                   '''
            clean_help_projects = clean_help_projects.format(', '.join(self.project_names))
        else:
            clean_help_projects = 'projects to clean'
        group_clean.add_argument('--projects', '-p', choices=self.project_names,
                                 nargs='+', help=clean_help_projects, metavar='PROJECT')

    def _configure_subparser_diff(self, subparsers):
        """Configure clowder diff subparser and arguments"""
        # clowder diff
        diff_help = 'Show git diff for projects'
        parser_diff = subparsers.add_parser('diff', help=diff_help)
        group_diff = parser_diff.add_mutually_exclusive_group()
        if self.group_names is not '':
            diff_help_groups = '''
                               groups to diff:
                               {0}
                               '''
            diff_help_groups = diff_help_groups.format(', '.join(self.group_names))
        else:
            diff_help_groups = 'groups to diff'
        group_diff.add_argument('--groups', '-g', choices=self.group_names,
                                default=self.group_names, nargs='+',
                                help=diff_help_groups, metavar='GROUP')
        if self.project_names is not '':
            diff_help_projects = '''
                                 projects to diff:
                                 {0}
                                 '''
            diff_help_projects = diff_help_projects.format(', '.join(self.project_names))
        else:
            diff_help_projects = 'projects to diff'
        group_diff.add_argument('--projects', '-p', choices=self.project_names,
                                nargs='+', help=diff_help_projects, metavar='PROJECT')

    def _configure_subparser_forall(self, subparsers):
        """Configure clowder forall subparser and arguments"""
        # clowder forall
        forall_help = 'Run command or script in project directories'
        parser_forall = subparsers.add_parser('forall', help=forall_help)
        parser_forall.add_argument('--ignore-errors', '-i', action='store_true',
                                   help='ignore errors in command or script')
        group_forall_command = parser_forall.add_mutually_exclusive_group()
        group_forall_command.add_argument('--command', '-c', nargs=1, metavar='COMMAND',
                                          help='command or script to run in project directories')
        group_forall_targets = parser_forall.add_mutually_exclusive_group()
        if self.group_names is not '':
            forall_help_groups = '''
                                 groups to run command or script for:
                                 {0}
                                 '''
            forall_help_groups = forall_help_groups.format(', '.join(self.group_names))
        else:
            forall_help_groups = 'groups to run command or script for'
        group_forall_targets.add_argument('--groups', '-g', choices=self.group_names,
                                          default=self.group_names, nargs='+',
                                          help=forall_help_groups, metavar='GROUP')
        if self.project_names is not '':
            forall_help_projects = '''
                                   projects to run command or script for:
                                   {0}
                                   '''
            forall_help_projects = forall_help_projects.format(', '.join(self.project_names))
        else:
            forall_help_projects = 'projects to run command or script for'
        group_forall_targets.add_argument('--projects', '-p', choices=self.project_names,
                                          nargs='+', help=forall_help_projects,
                                          metavar='PROJECT')

    def _configure_subparser_herd(self, subparsers):
        """Configure clowder herd subparser and arguments"""
        # clowder herd
        herd_help = 'Clone and sync latest changes for projects'
        parser_herd = subparsers.add_parser('herd', help=herd_help)
        parser_herd.add_argument('--depth', '-d', default=None, type=int, nargs=1,
                                 help='depth to herd', metavar='DEPTH')
        # TODO: clowder herd -b
        # parser_herd.add_argument('--branch', '-b', nargs=1, default=None, help='Branch to herd')
        group_herd = parser_herd.add_mutually_exclusive_group()
        if self.group_names is not '':
            herd_help_groups = '''
                                 groups to herd:
                                 {0}
                                 '''
            herd_help_groups = herd_help_groups.format(', '.join(self.group_names))
        else:
            herd_help_groups = 'groups to herd'
        group_herd.add_argument('--groups', '-g', choices=self.group_names,
                                default=self.group_names, nargs='+',
                                help=herd_help_groups, metavar='GROUP')
        if self.project_names is not '':
            herd_help_projects = '''
                                   projects to herd:
                                   {0}
                                   '''
            herd_help_projects = herd_help_projects.format(', '.join(self.project_names))
        else:
            herd_help_projects = 'projects to herd'
        group_herd.add_argument('--projects', '-p', choices=self.project_names,
                                nargs='+', help=herd_help_projects, metavar='PROJECT')

    def _configure_subparser_init(self, subparsers):
        """Configure clowder init subparser and arguments"""
        # clowder init
        init_help = 'Clone repository to clowder directory and create clowder.yaml symlink'
        parser_init = subparsers.add_parser('init', help=init_help)
        parser_init.add_argument('url', help='url of repo containing clowder.yaml', metavar='URL')
        parser_init.add_argument('--branch', '-b', nargs=1,
                                 help='branch of repo containing clowder.yaml', metavar='BRANCH')

    def _configure_subparser_link(self, subparsers):
        """Configure clowder link subparser and arguments"""
        # clowder link
        parser_link = subparsers.add_parser('link', help='Symlink clowder.yaml version')
        if self.versions is not None:
            link_help_version = '''
                                   version to symlink:
                                   {0}
                                   '''
            link_help_version = link_help_version.format(', '.join(self.versions))
        else:
            link_help_version = 'version to symlink'
        parser_link.add_argument('--version', '-v', choices=self.versions, nargs=1,
                                 default=None, help=link_help_version, metavar='VERSION')

    def _configure_subparser_prune(self, subparsers):
        """Configure clowder prune subparser and arguments"""
        # clowder prune
        parser_prune = subparsers.add_parser('prune', help='Prune old branch')
        parser_prune.add_argument('--force', '-f', action='store_true',
                                  help='force prune branches')
        parser_prune.add_argument('branch', help='name of branch to remove', metavar='BRANCH')
        group_prune_options = parser_prune.add_mutually_exclusive_group()
        group_prune_options.add_argument('--all', '-a', action='store_true',
                                         help='prune local and remote branches')
        group_prune_options.add_argument('--remote', '-r', action='store_true',
                                         help='prune remote branches')
        group_prune = parser_prune.add_mutually_exclusive_group()
        if self.group_names is not '':
            prune_help_groups = '''
                                 groups to prune branch for:
                                 {0}
                                 '''
            prune_help_groups = prune_help_groups.format(', '.join(self.group_names))
        else:
            prune_help_groups = 'groups to prune branch for'
        group_prune.add_argument('--groups', '-g', choices=self.group_names,
                                 default=self.group_names, nargs='+',
                                 help=prune_help_groups, metavar='GROUP')
        if self.project_names is not '':
            prune_help_projects = '''
                                   projects to prune branch for:
                                   {0}
                                   '''
            prune_help_projects = prune_help_projects.format(', '.join(self.project_names))
        else:
            prune_help_projects = 'projects to prune branch for'
        group_prune.add_argument('--projects', '-p', choices=self.project_names,
                                 nargs='+', help=prune_help_projects, metavar='PROJECT')

    def _configure_subparser_repo(self, subparsers):
        """Configure clowder repo subparser and arguments"""
        # clowder repo
        parser_repo = subparsers.add_parser('repo', help='Manage clowder repo')
        repo_subparsers = parser_repo.add_subparsers(dest='repo_command', metavar='SUBCOMMAND')
        # clowder repo add
        repo_add_help = 'Add files in clowder repo'
        parser_repo_add = repo_subparsers.add_parser('add', help=repo_add_help)
        parser_repo_add.add_argument('files', nargs='+',
                                     help='files to add', metavar='FILE')
        # clowder repo checkout
        repo_checkout_help = 'Checkout ref in clowder repo'
        parser_repo_checkout = repo_subparsers.add_parser('checkout', help=repo_checkout_help)
        parser_repo_checkout.add_argument('ref', nargs=1,
                                          help='git ref to checkout', metavar='REF')
        # clowder repo clean
        repo_clean_help = 'Discard changes in clowder repo'
        repo_subparsers.add_parser('clean', help=repo_clean_help)
        # clowder repo commit
        repo_commit_help = 'Commit current changes in clowder repo yaml files'
        parser_repo_commit = repo_subparsers.add_parser('commit', help=repo_commit_help)
        parser_repo_commit.add_argument('message', nargs=1,
                                        help='commit message', metavar='MESSAGE')
        # clowder repo run
        repo_run_help = 'Run command in clowder repo'
        parser_repo_run = repo_subparsers.add_parser('run', help=repo_run_help)
        repo_run_command_help = 'command to run in clowder repo directory'
        parser_repo_run.add_argument('command', nargs=1,
                                     help=repo_run_command_help, metavar='COMMAND')
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
        parser_save.add_argument('version', help='version to save', metavar='VERSION')

    def _configure_subparser_start(self, subparsers):
        """Configure clowder start subparser and arguments"""
        # clowder start
        parser_start = subparsers.add_parser('start', help='Start a new feature')
        parser_start.add_argument('--tracking', '-t', action='store_true',
                                  help='create remote tracking branch')
        parser_start.add_argument('branch', help='name of branch to create', metavar='BRANCH')
        group_start = parser_start.add_mutually_exclusive_group()
        if self.group_names is not '':
            start_help_groups = '''
                                 groups to start feature branch for:
                                 {0}
                                 '''
            start_help_groups = start_help_groups.format(', '.join(self.group_names))
        else:
            start_help_groups = 'groups to start feature branch for'
        group_start.add_argument('--groups', '-g', choices=self.group_names,
                                 default=self.group_names, nargs='+',
                                 help=start_help_groups, metavar='GROUP')
        if self.project_names is not '':
            start_help_projects = '''
                                   projects to start feature branch for:
                                   {0}
                                   '''
            start_help_projects = start_help_projects.format(', '.join(self.project_names))
        else:
            start_help_projects = 'projects to start feature branch for'
        group_start.add_argument('--projects', '-p', choices=self.project_names,
                                 nargs='+', help=start_help_projects, metavar='PROJECT')

    def _configure_subparser_stash(self, subparsers):
        """Configure clowder stash subparser and arguments"""
        # clowder stash
        parser_stash = subparsers.add_parser('stash',
                                             help='Stash current changes')
        group_stash = parser_stash.add_mutually_exclusive_group()
        if self.group_names is not '':
            stash_help_groups = '''
                                 groups to stash:
                                 {0}
                                 '''
            stash_help_groups = stash_help_groups.format(', '.join(self.group_names))
        else:
            stash_help_groups = 'groups to stash'
        group_stash.add_argument('--groups', '-g', choices=self.group_names,
                                 default=self.group_names, nargs='+',
                                 help=stash_help_groups, metavar='GROUP')
        if self.project_names is not '':
            stash_help_projects = '''
                                   projects to stash:
                                   {0}
                                   '''
            stash_help_projects = stash_help_projects.format(', '.join(self.project_names))
        else:
            stash_help_projects = 'projects to stash'
        group_stash.add_argument('--projects', '-p', choices=self.project_names,
                                 nargs='+', help=stash_help_projects, metavar='PROJECT')

    def _configure_subparser_status(self, subparsers):
        """Configure clowder status subparser and arguments"""
        # clowder status
        parser_status = subparsers.add_parser('status', help='Print project status')
        parser_status.add_argument('--fetch', '-f', action='store_true',
                                   help='fetch projects before printing status')
        if self.group_names is not '':
            status_help_groups = '''
                                 groups to print status for:
                                 {0}
                                 '''
            status_help_groups = status_help_groups.format(', '.join(self.group_names))
        else:
            status_help_groups = 'groups to print status for'
        group_status = parser_status.add_mutually_exclusive_group()
        group_status.add_argument('--groups', '-g', choices=self.group_names,
                                  default=self.group_names, nargs='+',
                                  help=status_help_groups, metavar='GROUP')
        if self.project_names is not '':
            status_help_projects = '''
                                   projects to print status for:
                                   {0}
                                   '''
            status_help_projects = status_help_projects.format(', '.join(self.project_names))
        else:
            status_help_projects = 'projects to print status for'
        group_status.add_argument('--projects', '-p', choices=self.project_names,
                                  nargs='+', help=status_help_projects, metavar='PROJECT')

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
