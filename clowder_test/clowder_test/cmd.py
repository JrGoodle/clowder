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

        parser.add_argument('--parallel', '-p', action='store_true', help='run tests with parallel commands')

        parser.add_argument('--write', '-w', action='store_true', help='run tests requiring test repo write access')

        self._subparsers = parser.add_subparsers(dest='test_command', metavar='SUBCOMMAND')
        self._configure_all_subparser()
        self._configure_cats_subparser()
        self._configure_cocos2d_subparser()
        self._configure_llvm_subparser()
        self._configure_offline_subparser()
        self._configure_parallel_subparser()
        self._configure_swift_subparser()
        self._configure_unittest_subparser()
        self._configure_write_subparser()

        # Argcomplete and arguments parsing
        argcomplete.autocomplete(parser)
        self.args = parser.parse_args()
        if self.args.test_command is None or not hasattr(self, self.args.test_command):
            exit_unrecognized_command(parser)

        # use dispatch pattern to invoke method with same name
        scripts_dir = os.path.join(os.getcwd(), 'test', 'scripts')
        return_code = execute_command('./setup_local_test_directory.sh', scripts_dir)
        if return_code != 0:
            print(' - Failed to setup local test directory')
            sys.exit(return_code)

        access = 'write' if self.args.write else 'read'
        self.test_env = {'ACCESS_LEVEL': access}
        if self.args.parallel:
            self.test_env["PARALLEL"] = '--parallel'

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

        return_code = self._execute_command('./test_example_cats.sh', path)
        self._exit(return_code)

    def cats_branch(self, path):
        """clowder cats branch tests"""

        return_code = self._execute_command('./branch.sh', path)
        self._exit(return_code)

    def cats_checkout(self, path):
        """clowder cats checkout tests"""

        return_code = self._execute_command('./checkout.sh', path)
        self._exit(return_code)

    def cats_clean(self, path):
        """clowder cats clean tests"""

        return_code = self._execute_command('./clean.sh', path)
        self._exit(return_code)

    def cats_diff(self, path):
        """clowder cats diff tests"""

        return_code = self._execute_command('./diff.sh', path)
        self._exit(return_code)

    def cats_forall(self, path):
        """clowder cats forall tests"""

        return_code = self._execute_command('./forall.sh', path)
        self._exit(return_code)

    def cats_help(self, path):
        """clowder cats help tests"""

        return_code = self._execute_command('./help.sh', path)
        self._exit(return_code)

    def cats_herd_branch(self, path):
        """clowder cats herd branch tests"""

        return_code = self._execute_command('./herd_branch.sh', path)
        self._exit(return_code)

    def cats_herd_tag(self, path):
        """clowder cats herd tag tests"""

        return_code = self._execute_command('./herd_tag.sh', path)
        self._exit(return_code)

    def cats_herd(self, path):
        """clowder cats herd tests"""

        return_code = self._execute_command('./herd.sh', path)
        self._exit(return_code)

    def cats_import(self, path):
        """clowder cats import tests"""

        return_code = self._execute_command('./import.sh', path)
        self._exit(return_code)

    def cats_init(self, path):
        """clowder cats init tests"""

        return_code = self._execute_command('./init.sh', path)
        self._exit(return_code)

    def cats_link(self, path):
        """clowder cats link tests"""

        return_code = self._execute_command('./link.sh', path)
        self._exit(return_code)

    def cats_prune(self, path):
        """clowder cats prune tests"""

        return_code = self._execute_command('./prune.sh', path)
        self._exit(return_code)

    def cats_repo(self, path):
        """clowder cats repo tests"""

        return_code = self._execute_command('./repo.sh', path)
        self._exit(return_code)

    def cats_reset(self, path):
        """clowder cats reset tests"""

        return_code = self._execute_command('./reset.sh', path)
        self._exit(return_code)

    def cats_save(self, path):
        """clowder cats save tests"""

        return_code = self._execute_command('./save.sh', path)
        self._exit(return_code)

    def cats_start(self, path):
        """clowder cats start tests"""

        return_code = self._execute_command('./start.sh', path)
        self._exit(return_code)

    def cats_stash(self, path):
        """clowder cats stash tests"""

        return_code = self._execute_command('./stash.sh', path)
        self._exit(return_code)

    def cats_status(self, path):
        """clowder cats status tests"""

        return_code = self._execute_command('./status.sh', path)
        self._exit(return_code)

    def cats_yaml_validation(self, path):
        """clowder cats yaml validation tests"""

        return_code = self._execute_command('./yaml_validation.sh', path)
        self._exit(return_code)

    def cats_yaml(self, path):
        """clowder cats yaml tests"""

        return_code = self._execute_command('./yaml.sh', path)
        self._exit(return_code)

    def cocos2d(self, path):
        """clowder cocos2d tests entrypoint"""

        cocos2d_command = 'cocos2d_' + self.args.cocos2d_command
        if self.args.cocos2d_command != 'all':
            path = os.path.join(path, 'cocos2d')
        getattr(self, cocos2d_command)(path)

    def cocos2d_all(self, path):
        """clowder cocos2d tests"""

        return_code = self._execute_command('./test_example_cocos2d.sh', path)
        self._exit(return_code)

    def cocos2d_clean(self, path):
        """clowder cocos2d clean tests"""

        return_code = self._execute_command('./clean.sh', path)
        self._exit(return_code)

    def cocos2d_herd(self, path):
        """clowder cocos2d herd tests"""

        return_code = self._execute_command('./herd.sh', path)
        self._exit(return_code)

    def cocos2d_skip(self, path):
        """clowder cocos2d skip tests"""

        return_code = self._execute_command('./skip.sh', path)
        self._exit(return_code)

    def llvm(self, path):
        """clowder llvm tests entrypoint"""

        llvm_command = 'llvm_' + self.args.llvm_command
        if self.args.llvm_command != 'all':
            path = os.path.join(path, 'llvm')
        getattr(self, llvm_command)(path)

    def llvm_all(self, path):
        """clowder llvm tests"""

        return_code = self._execute_command('./test_example_llvm.sh', path)
        self._exit(return_code)

    def llvm_branch(self, path):
        """clowder llvm branch tests"""

        return_code = self._execute_command('./branch.sh', path)
        self._exit(return_code)

    def llvm_forks(self, path):
        """clowder llvm forks tests"""

        return_code = self._execute_command('./forks.sh', path)
        self._exit(return_code)

    def llvm_herd(self, path):
        """clowder llvm herd tests"""

        return_code = self._execute_command('./herd.sh', path)
        self._exit(return_code)

    def llvm_reset(self, path):
        """clowder llvm reset tests"""

        return_code = self._execute_command('./reset.sh', path)
        self._exit(return_code)

    def llvm_sync(self, path):
        """clowder llvm sync tests"""

        return_code = self._execute_command('./sync.sh', path)
        self._exit(return_code)

    def offline(self, path):
        """clowder offline tests"""

        path = os.path.join(path, 'cats')
        return_code = self._execute_command('./offline.sh', path)
        self._exit(return_code)

    def parallel(self, path):
        """clowder parallel tests"""

        return_code = self._execute_command('./test_parallel.sh', path)
        self._exit(return_code)

    def swift(self, path):
        """clowder swift tests entrypoint"""

        swift_command = 'swift_' + self.args.swift_command
        if self.args.swift_command != 'all':
            path = os.path.join(path, 'swift')
        getattr(self, swift_command)(path)

    def swift_all(self, path):
        """clowder swift tests"""

        return_code = self._execute_command('./test_example_swift.sh', path)
        self._exit(return_code)

    def swift_config_versions(self, path):
        """clowder swift config versions tests"""

        return_code = self._execute_command('./config_versions.sh', path)
        self._exit(return_code)

    def swift_configure_remotes(self, path):
        """clowder swift configure remotes tests"""

        return_code = self._execute_command('./configure_remotes.sh', path)
        self._exit(return_code)

    def swift_reset(self, path):
        """clowder swift reset tests"""

        return_code = self._execute_command('./reset.sh', path)
        self._exit(return_code)

    def unittests(self, path):
        """clowder unit tests"""

        if self.args.version == 'python2':
            self.test_env["PYTHON_VERSION"] = 'python'
        else:
            self.test_env["PYTHON_VERSION"] = 'python3'

        return_code = self._execute_command('./unittests.sh', path)
        self._exit(return_code)

    def write(self, path):
        """clowder write tests"""

        self.test_env['ACCESS_LEVEL'] = 'write'

        example_dir = os.path.join(path, 'cats')
        return_code = self._execute_command('./write_herd.sh', example_dir)
        self._exit(return_code)
        return_code = self._execute_command('./write_prune.sh', example_dir)
        self._exit(return_code)
        return_code = self._execute_command('./write_repo.sh', example_dir)
        self._exit(return_code)
        return_code = self._execute_command('./write_start.sh', example_dir)
        self._exit(return_code)

        example_dir = os.path.join(path, 'llvm')
        return_code = self._execute_command('./write_forks.sh', example_dir)
        self._exit(return_code)
        return_code = self._execute_command('./write_sync.sh', example_dir)
        self._exit(return_code)

        example_dir = os.path.join(path, 'swift')
        return_code = self._execute_command('./write_configure_remotes.sh', example_dir)
        self._exit(return_code)

    def _configure_all_subparser(self):
        """clowder all tests subparser"""

        self._subparsers.add_parser('all', help='Run all tests')

    def _configure_cats_subparser(self):
        """clowder cats tests subparser"""

        parser = self._subparsers.add_parser('cats', help='Run cats tests')
        cats_subparser = parser.add_subparsers(dest='cats_command', metavar='SUBCOMMAND')
        cats_subparser.add_parser('all', help='Run all cats tests')
        cats_subparser.add_parser('branch', help='Run cats branch tests')
        cats_subparser.add_parser('checkout', help='Run cats checkout tests')
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

        parser = self._subparsers.add_parser('cocos2d', help='Run cocos2d tests')
        cocos2d_subparser = parser.add_subparsers(dest='cocos2d_command', metavar='SUBCOMMAND')
        cocos2d_subparser.add_parser('all', help='Run all cocos2d tests')
        cocos2d_subparser.add_parser('clean', help='Run clean cocos2d tests')
        cocos2d_subparser.add_parser('herd', help='Run herd cocos2d tests')
        cocos2d_subparser.add_parser('skip', help='Run skip cocos2d tests')

    def _configure_llvm_subparser(self):
        """clowder llvm tests subparser"""

        parser = self._subparsers.add_parser('llvm', help='Run llvm tests')
        llvm_subparser = parser.add_subparsers(dest='llvm_command', metavar='SUBCOMMAND')
        llvm_subparser.add_parser('all', help='Run all llvm tests')
        llvm_subparser.add_parser('branch', help='Run llvm branch tests')
        llvm_subparser.add_parser('forks', help='Run llvm forks tests')
        llvm_subparser.add_parser('herd', help='Run llvm herd tests')
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
        swift_subparser.add_parser('configure_remotes', help='Run swift configure remotes tests')
        swift_subparser.add_parser('reset', help='Run swift reset tests')

    def _configure_unittest_subparser(self):
        """clowder unit tests subparser"""

        unittest_subparser = self._subparsers.add_parser('unittests',
                                                         help='Run unit tests')
        unittest_subparser.add_argument('version', choices=['python2', 'python3'],
                                        help='Python vesion to run unit tests for',
                                        metavar='PYTHON_VERSION')

    def _configure_write_subparser(self):
        """clowder write tests subparser"""

        self._subparsers.add_parser('write', help='Run tests requiring remote write permissions')

    def _execute_command(self, command, path):
        """Private exit handler"""

        return execute_command(command, path, env=self.test_env)

    @staticmethod
    def _exit(return_code):
        """Private exit handler"""

        if return_code != 0:
            sys.exit(return_code)


def exit_unrecognized_command(parser):
    """Print unrecognized command message and exit"""

    parser.print_help()
    print()
    sys.exit(1)
