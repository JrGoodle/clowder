"""Main entrypoint for clowder test runner"""

from __future__ import print_function

import argparse
import os
import sys
import argcomplete

from clowder_test.execute import execute_command


# Disable errors shown by pylint for too many public methods
# pylint: disable=R0904
# Disable errors shown by pylint for no specified exception types
# pylint: disable=W0702


def main():
    """Main entrypoint for clowder test runner"""
    Command()


if __name__ == '__main__':
    raise SystemExit(main())


class Command(object):
    """Command class for parsing commandline options"""

    def __init__(self):
        # clowder argparse setup
        command_description = 'Clowder test runner'
        parser = argparse.ArgumentParser(description=command_description,
                                         formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('--write', '-w', action='store_true',
                            help='run tests requiring test repo write access')
        self._subparsers = parser.add_subparsers(dest='test_command', metavar='SUBCOMMAND')
        self._configure_all_subparser()
        self._configure_cats_subparser()
        self._configure_cocos2d_subparser()
        self._configure_llvm_subparser()
        self._configure_offline_subparser()
        self._configure_parallel_subparser()
        self._configure_swift_subparser()
        self._configure_unittest_subparser()
        # Argcomplete and arguments parsing
        argcomplete.autocomplete(parser)
        self.args = parser.parse_args()
        if self.args.test_command is None or not hasattr(self, self.args.test_command):
            exit_unrecognized_command(parser)
        # use dispatch pattern to invoke method with same name
        scripts_dir = os.path.join(os.getcwd(), 'test', 'scripts')
        return_code = execute_command('./setup_local_test_directory.sh', scripts_dir, shell=True)
        if return_code != 0:
            print(' - Failed to setup local test directory')
            sys.exit(return_code)
        getattr(self, self.args.test_command)(scripts_dir)
        print()

    def all(self, path):
        """clowder branch command"""
        self.cats(path)
        self.cocos2d(path)
        self.llvm(path)
        self.offline(path)
        self.parallel(path)
        self.swift(path)
        self.unittests(path)

    def cats(self, path):
        """clowder cats tests entrypoint"""
        cats_command = 'cats_' + self.args.cats_command
        if self.args.cats_command != 'all':
            path = os.path.join(path, 'cats')
        getattr(self, cats_command)(path)

    def cats_all(self, path):
        """clowder cats tests"""
        test_env = {}
        if self.args.write:
            test_env["ACCESS_LEVEL"] = 'write'
        else:
            test_env["ACCESS_LEVEL"] = 'read'
        return_code = execute_command('./test_example_cats.sh', path, shell=True, env=test_env)
        sys.exit(return_code)

    @classmethod
    def cats_branch(cls, path):
        """clowder cats branch tests"""
        return_code = execute_command('./branch.sh', path, shell=True)
        sys.exit(return_code)

    @classmethod
    def cats_clean(cls, path):
        """clowder cats clean tests"""
        return_code = execute_command('./clean.sh', path, shell=True)
        sys.exit(return_code)

    @classmethod
    def cats_diff(cls, path):
        """clowder cats diff tests"""
        return_code = execute_command('./diff.sh', path, shell=True)
        sys.exit(return_code)

    @classmethod
    def cats_forall(cls, path):
        """clowder cats forall tests"""
        return_code = execute_command('./forall.sh', path, shell=True)
        sys.exit(return_code)

    @classmethod
    def cats_help(cls, path):
        """clowder cats help tests"""
        return_code = execute_command('./help.sh', path, shell=True)
        sys.exit(return_code)

    @classmethod
    def cats_herd_branch(cls, path):
        """clowder cats herd branch tests"""
        return_code = execute_command('./herd_branch.sh', path, shell=True)
        sys.exit(return_code)

    @classmethod
    def cats_herd_tag(cls, path):
        """clowder cats herd tag tests"""
        return_code = execute_command('./herd_tag.sh', path, shell=True)
        sys.exit(return_code)

    def cats_herd(self, path):
        """clowder cats herd tests"""
        test_env = {}
        if self.args.write:
            test_env["ACCESS_LEVEL"] = 'write'
        else:
            test_env["ACCESS_LEVEL"] = 'read'
        return_code = execute_command('./herd.sh', path, shell=True)
        sys.exit(return_code)

    @classmethod
    def cats_import(cls, path):
        """clowder cats import tests"""
        return_code = execute_command('./import.sh', path, shell=True)
        sys.exit(return_code)

    @classmethod
    def cats_init(cls, path):
        """clowder cats init tests"""
        return_code = execute_command('./init.sh', path, shell=True)
        sys.exit(return_code)

    @classmethod
    def cats_link(cls, path):
        """clowder cats link tests"""
        return_code = execute_command('./link.sh', path, shell=True)
        sys.exit(return_code)

    def cats_prune(self, path):
        """clowder cats prune tests"""
        test_env = {}
        if self.args.write:
            test_env["ACCESS_LEVEL"] = 'write'
        else:
            test_env["ACCESS_LEVEL"] = 'read'
        return_code = execute_command('./prune.sh', path, shell=True)
        sys.exit(return_code)

    def cats_repo(self, path):
        """clowder cats repo tests"""
        test_env = {}
        if self.args.write:
            test_env["ACCESS_LEVEL"] = 'write'
        else:
            test_env["ACCESS_LEVEL"] = 'read'
        return_code = execute_command('./repo.sh', path, shell=True)
        sys.exit(return_code)

    @classmethod
    def cats_reset(cls, path):
        """clowder cats reset tests"""
        return_code = execute_command('./reset.sh', path, shell=True)
        sys.exit(return_code)

    @classmethod
    def cats_save(cls, path):
        """clowder cats save tests"""
        return_code = execute_command('./save.sh', path, shell=True)
        sys.exit(return_code)

    def cats_start(self, path):
        """clowder cats start tests"""
        test_env = {}
        if self.args.write:
            test_env["ACCESS_LEVEL"] = 'write'
        else:
            test_env["ACCESS_LEVEL"] = 'read'
        return_code = execute_command('./start.sh', path, shell=True)
        sys.exit(return_code)

    @classmethod
    def cats_stash(cls, path):
        """clowder cats stash tests"""
        return_code = execute_command('./stash.sh', path, shell=True)
        sys.exit(return_code)

    @classmethod
    def cats_status(cls, path):
        """clowder cats status tests"""
        return_code = execute_command('./status.sh', path, shell=True)
        sys.exit(return_code)

    @classmethod
    def cats_yaml_validation(cls, path):
        """clowder cats yaml validation tests"""
        return_code = execute_command('./yaml_validation.sh', path, shell=True)
        sys.exit(return_code)

    @classmethod
    def cats_yaml(cls, path):
        """clowder cats yaml tests"""
        return_code = execute_command('./yaml.sh', path, shell=True)
        sys.exit(return_code)

    @classmethod
    def cocos2d(cls, path):
        """clowder cocos2d tests"""
        return_code = execute_command('./test_example_cocos2d.sh', path, shell=True)
        sys.exit(return_code)

    def llvm(self, path):
        """clowder llvm tests entrypoint"""
        llvm_command = 'llvm_' + self.args.llvm_command
        if self.args.llvm_command != 'all':
            path = os.path.join(path, 'llvm')
        getattr(self, llvm_command)(path)

    def llvm_all(self, path):
        """clowder llvm tests"""
        test_env = {}
        if self.args.write:
            test_env["ACCESS_LEVEL"] = 'write'
        else:
            test_env["ACCESS_LEVEL"] = 'read'
        return_code = execute_command('./test_example_llvm.sh', path, shell=True, env=test_env)
        sys.exit(return_code)

    @classmethod
    def llvm_branch(cls, path):
        """clowder llvm branch tests"""
        return_code = execute_command('./branch.sh', path, shell=True)
        sys.exit(return_code)

    @classmethod
    def llvm_forks(cls, path):
        """clowder llvm forks tests"""
        return_code = execute_command('./forks.sh', path, shell=True)
        sys.exit(return_code)

    @classmethod
    def llvm_reset(cls, path):
        """clowder llvm reset tests"""
        return_code = execute_command('./reset.sh', path, shell=True)
        sys.exit(return_code)

    @classmethod
    def llvm_sync(cls, path):
        """clowder llvm sync tests"""
        return_code = execute_command('./sync.sh', path, shell=True)
        sys.exit(return_code)

    @classmethod
    def offline(cls, path):
        """clowder offline tests"""
        path = os.path.join(path, 'cats')
        return_code = execute_command('./offline.sh', path, shell=True)
        sys.exit(return_code)

    @classmethod
    def parallel(cls, path):
        """clowder parallel tests"""
        return_code = execute_command('./test_parallel.sh', path, shell=True)
        sys.exit(return_code)

    def swift(self, path):
        """clowder swift tests entrypoint"""
        swift_command = 'swift_' + self.args.swift_command
        if self.args.swift_command != 'all':
            path = os.path.join(path, 'swift')
        getattr(self, swift_command)(path)

    def swift_all(self, path):
        """clowder swift tests"""
        test_env = {}
        if self.args.write:
            test_env["ACCESS_LEVEL"] = 'write'
        else:
            test_env["ACCESS_LEVEL"] = 'read'
        return_code = execute_command('./test_example_swift.sh', path, shell=True, env=test_env)
        sys.exit(return_code)

    @classmethod
    def swift_config_versions(cls, path):
        """clowder swift config versions tests"""
        return_code = execute_command('./config_versions.sh', path, shell=True)
        sys.exit(return_code)

    @classmethod
    def swift_reset(cls, path):
        """clowder swift reset tests"""
        return_code = execute_command('./reset.sh', path, shell=True)
        sys.exit(return_code)

    def unittests(self, path):
        """clowder unit tests"""
        test_env = {}
        if self.args.version == 'python2':
            test_env["PYTHON_VERSION"] = 'python'
        else:
            test_env["PYTHON_VERSION"] = 'python3'
        return_code = execute_command('./unittests.sh', path, shell=True, env=test_env)
        sys.exit(return_code)

    def _configure_all_subparser(self):
        """clowder all tests subparser"""
        self._subparsers.add_parser('all', help='Run all tests')

    def _configure_cats_subparser(self):
        """clowder cats tests subparser"""
        parser = self._subparsers.add_parser('cats', help='Run cats tests')
        cats_subparser = parser.add_subparsers(dest='cats_command', metavar='SUBCOMMAND')
        cats_subparser.add_parser('all', help='Run all cats tests')
        cats_subparser.add_parser('branch', help='Run cats branch tests')
        cats_subparser.add_parser('clean', help='Run cats clean tests')
        cats_subparser.add_parser('diff', help='Run cats diff tests')
        cats_subparser.add_parser('forall', help='Run cats forall tests')
        cats_subparser.add_parser('help', help='Run cats help tests')
        cats_subparser.add_parser('herd_branch', help='Run cats herd branch tests')
        cats_subparser.add_parser('herd_tag', help='Run cats herd tag tests')
        cats_subparser.add_parser('herd', help='Run cats herd tests')
        cats_subparser.add_parser('import', help='Run cats import tests')
        cats_subparser.add_parser('init', help='Run cats init tests')
        cats_subparser.add_parser('link', help='Run cats link tests')
        cats_subparser.add_parser('prune', help='Run cats prune tests')
        cats_subparser.add_parser('repo', help='Run cats repo tests')
        cats_subparser.add_parser('reset', help='Run cats reset tests')
        cats_subparser.add_parser('save', help='Run cats save tests')
        cats_subparser.add_parser('start', help='Run cats start tests')
        cats_subparser.add_parser('stash', help='Run cats stash tests')
        cats_subparser.add_parser('status', help='Run cats status tests')
        cats_subparser.add_parser('yaml_validation', help='Run cats yaml validation tests')
        cats_subparser.add_parser('yaml', help='Run cats yaml tests')

    def _configure_cocos2d_subparser(self):
        """clowder cocos2d tests subparser"""
        self._subparsers.add_parser('cocos2d', help='Run cocos2d tests')

    def _configure_llvm_subparser(self):
        """clowder llvm tests subparser"""
        parser = self._subparsers.add_parser('llvm', help='Run llvm tests')
        llvm_subparser = parser.add_subparsers(dest='llvm_command', metavar='SUBCOMMAND')
        llvm_subparser.add_parser('all', help='Run all llvm tests')
        llvm_subparser.add_parser('branch', help='Run llvm branch tests')
        llvm_subparser.add_parser('forks', help='Run llvm forks tests')
        llvm_subparser.add_parser('reset', help='Run llvm reset tests')
        llvm_subparser.add_parser('sync', help='Run llvm sync tests')

    def _configure_offline_subparser(self):
        """clowder offline tests subparser"""
        self._subparsers.add_parser('offline', help='Run offline tests')

    def _configure_parallel_subparser(self):
        """clowder parallel tests subparser"""
        self._subparsers.add_parser('parallel', help='Run parallel tests')

    def _configure_swift_subparser(self):
        """clowder swift tests subparser"""
        parser = self._subparsers.add_parser('swift', help='Run swift tests')
        swift_subparser = parser.add_subparsers(dest='swift_command', metavar='SUBCOMMAND')
        swift_subparser.add_parser('all', help='Run all swift tests')
        swift_subparser.add_parser('config_versions', help='Run swift config versions tests')
        swift_subparser.add_parser('reset', help='Run swift reset tests')

    def _configure_unittest_subparser(self):
        """clowder unit tests subparser"""
        unittest_subparser = self._subparsers.add_parser('unittests',
                                                         help='Run unit tests')
        unittest_subparser.add_argument('version', choices=['python2', 'python3'],
                                        help='Python vesion to run unit tests for',
                                        metavar='PYTHON_VERSION')


def exit_unrecognized_command(parser):
    """Print unrecognized command message and exit"""
    parser.print_help()
    print()
    sys.exit(1)
