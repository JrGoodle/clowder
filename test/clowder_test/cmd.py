"""Main entrypoint for clowder test runner"""

from __future__ import print_function
import argparse
import os
import subprocess
import sys
import argcomplete


# Disable errors shown by pylint for too many public methods
# pylint: disable=R0904


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
        self._scripts_dir = os.path.join(os.getcwd(), 'test', 'scripts')
        parser = argparse.ArgumentParser(description=command_description,
                                         formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('--python2', action='store_true',
                            help='run tests for Python 2')
        parser.add_argument('--write', '-w', action='store_true',
                            help='run tests requiring test repo write access')
        self._subparsers = parser.add_subparsers(dest='test_command', metavar='SUBCOMMAND')
        self._configure_all_subparser()
        self._configure_cats_subparser()
        self._configure_cocos2d_subparser()
        self._configure_llvm_subparser()
        self._configure_offline_subparser()
        self._configure_swift_subparser()
        self._configure_unittest_subparser()
        # Argcomplete and arguments parsing
        argcomplete.autocomplete(parser)
        self.args = parser.parse_args()
        if self.args.test_command is None or not hasattr(self, self.args.test_command):
            exit_unrecognized_command(parser)
        # use dispatch pattern to invoke method with same name
        getattr(self, self.args.clowder_command)()
        print()

    def all(self):
        """clowder branch command"""
        self.cats()
        self.cocos2d()
        self.llvm()
        self.offline()
        self.swift()
        self.unittests()

    def cats(self):
        """clowder cats tests entrypoint"""
        cats_command = 'cats_' + self.args.cats_command
        getattr(self, cats_command)()

    def cats_all(self):
        """clowder cats tests"""
        test_env = os.environ.copy()
        if self.args.write:
            test_env["ACCESS_LEVEL"] = 'write'
        else:
            test_env["ACCESS_LEVEL"] = 'read'
        script = os.path.join(self._scripts_dir, 'test_example_cats.sh')
        subprocess.call(script, shell=True, env=test_env)

    def cats_branch(self):
        """clowder cats branch tests"""
        script = os.path.join(self._scripts_dir, 'test_cats_branch.sh')
        subprocess.call(script, shell=True)

    def cats_clean(self):
        """clowder cats clean tests"""
        script = os.path.join(self._scripts_dir, 'test_cats_clean.sh')
        subprocess.call(script, shell=True)

    def cats_diff(self):
        """clowder cats diff tests"""
        script = os.path.join(self._scripts_dir, 'test_cats_diff.sh')
        subprocess.call(script, shell=True)

    def cats_forall(self):
        """clowder cats forall tests"""
        script = os.path.join(self._scripts_dir, 'test_cats_forall.sh')
        subprocess.call(script, shell=True)

    def cats_herd_branch(self):
        """clowder cats herd branch tests"""
        script = os.path.join(self._scripts_dir, 'test_cats_herd_branch.sh')
        subprocess.call(script, shell=True)

    def cats_herd(self):
        """clowder cats herd tests"""
        test_env = os.environ.copy()
        if self.args.write:
            test_env["ACCESS_LEVEL"] = 'write'
        else:
            test_env["ACCESS_LEVEL"] = 'read'
        script = os.path.join(self._scripts_dir, 'test_cats_herd.sh')
        subprocess.call(script, shell=True, env=test_env)

    def cats_import(self):
        """clowder cats import tests"""
        script = os.path.join(self._scripts_dir, 'test_cats_import.sh')
        subprocess.call(script, shell=True)

    def cats_init(self):
        """clowder cats init tests"""
        script = os.path.join(self._scripts_dir, 'test_cats_init.sh')
        subprocess.call(script, shell=True)

    def cats_link(self):
        """clowder cats link tests"""
        script = os.path.join(self._scripts_dir, 'test_cats_link.sh')
        subprocess.call(script, shell=True)

    def cats_prune(self):
        """clowder cats prune tests"""
        test_env = os.environ.copy()
        if self.args.write:
            test_env["ACCESS_LEVEL"] = 'write'
        else:
            test_env["ACCESS_LEVEL"] = 'read'
        script = os.path.join(self._scripts_dir, 'test_cats_prune.sh')
        subprocess.call(script, shell=True, env=test_env)

    def cats_repo(self):
        """clowder cats repo tests"""
        test_env = os.environ.copy()
        if self.args.write:
            test_env["ACCESS_LEVEL"] = 'write'
        else:
            test_env["ACCESS_LEVEL"] = 'read'
        script = os.path.join(self._scripts_dir, 'test_cats_repo.sh')
        subprocess.call(script, shell=True, env=test_env)

    def cats_save(self):
        """clowder cats save tests"""
        script = os.path.join(self._scripts_dir, 'test_cats_save.sh')
        subprocess.call(script, shell=True)

    def cats_start(self):
        """clowder cats start tests"""
        test_env = os.environ.copy()
        if self.args.write:
            test_env["ACCESS_LEVEL"] = 'write'
        else:
            test_env["ACCESS_LEVEL"] = 'read'
        script = os.path.join(self._scripts_dir, 'test_cats_start.sh')
        subprocess.call(script, shell=True, env=test_env)

    def cats_stash(self):
        """clowder cats stash tests"""
        script = os.path.join(self._scripts_dir, 'test_cats_stash.sh')
        subprocess.call(script, shell=True)

    def cats_status(self):
        """clowder cats status tests"""
        script = os.path.join(self._scripts_dir, 'test_cats_status.sh')
        subprocess.call(script, shell=True)

    def cats_yaml_validation(self):
        """clowder cats yaml validation tests"""
        script = os.path.join(self._scripts_dir, 'test_cats_yaml_validation.sh')
        subprocess.call(script, shell=True)

    def cats_yaml(self):
        """clowder cats yaml tests"""
        script = os.path.join(self._scripts_dir, 'test_cats_yaml.sh')
        subprocess.call(script, shell=True)

    def cocos2d(self):
        """clowder cocos2d tests"""
        script = os.path.join(self._scripts_dir, 'test_example_cocos2d.sh')
        subprocess.call(script, shell=True)

    def llvm(self):
        """clowder llvm tests"""
        test_env = os.environ.copy()
        if self.args.write:
            test_env["ACCESS_LEVEL"] = 'write'
        else:
            test_env["ACCESS_LEVEL"] = 'read'
        script = os.path.join(self._scripts_dir, 'test_example_llvm.sh')
        subprocess.call(script, shell=True, env=test_env)

    def offline(self):
        """clowder offline tests"""
        script = os.path.join(self._scripts_dir, 'test_cats_offline.sh')
        subprocess.call(script, shell=True)

    def swift(self):
        """clowder swift tests"""
        test_env = os.environ.copy()
        if self.args.write:
            test_env["ACCESS_LEVEL"] = 'write'
        else:
            test_env["ACCESS_LEVEL"] = 'read'
        script = os.path.join(self._scripts_dir, 'test_example_swift.sh')
        subprocess.call(script, shell=True, env=test_env)

    def unittests(self):
        """clowder unit tests"""
        self.args.python2

    def _configure_all_subparser(self):
        """clowder all tests subparser"""
        self._subparsers.add_parser('all', help='Run all tests')

    def _configure_cats_subparser(self):
        """clowder cats tests subparser"""
        parser = self._subparsers.add_parser('cats', help='Run cats tests')
        cats_subparser = parser.add_subparsers(dest='cats_command',
                                               metavar='SUBCOMMAND')
        cats_subparser.add_parser('all', help='Run all cats tests')
        cats_subparser.add_parser('branch', help='Run cats branch tests')
        cats_subparser.add_parser('clean', help='Run cats clean tests')
        cats_subparser.add_parser('diff', help='Run cats diff tests')
        cats_subparser.add_parser('forall', help='Run cats forall tests')
        cats_subparser.add_parser('herd_branch', help='Run cats herd branch tests')
        cats_subparser.add_parser('herd', help='Run cats herd tests')
        cats_subparser.add_parser('import', help='Run cats import tests')
        cats_subparser.add_parser('init', help='Run cats init tests')
        cats_subparser.add_parser('link', help='Run cats link tests')
        cats_subparser.add_parser('prune', help='Run cats prune tests')
        cats_subparser.add_parser('repo', help='Run cats repo tests')
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
        self._subparsers.add_parser('llvm', help='Run llvm tests')

    def _configure_offline_subparser(self):
        """clowder offline tests subparser"""
        self._subparsers.add_parser('offline', help='Run offline tests')

    def _configure_swift_subparser(self):
        """clowder swift tests subparser"""
        self._subparsers.add_parser('swift', help='Run swift tests')

    def _configure_unittest_subparser(self):
        """clowder unit tests subparser"""
        self._subparsers.add_parser('swift', help='Run swift tests')


def exit_unrecognized_command(parser):
    """Print unrecognized command message and exit"""
    parser.print_help()
    print()
    sys.exit(1)
