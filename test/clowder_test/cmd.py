"""Main entrypoint for clowder test runner"""

from __future__ import print_function

import atexit
import os
import signal
import subprocess
import sys

import argcomplete
import argparse
import psutil

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
        self._scripts_dir = os.path.join(os.getcwd(), 'test', 'scripts')
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
        getattr(self, self.args.test_command)()
        print()

    def all(self):
        """clowder branch command"""
        self.cats()
        self.cocos2d()
        self.llvm()
        self.offline()
        self.parallel()
        self.swift()
        self.unittests()

    def cats(self):
        """clowder cats tests entrypoint"""
        cats_command = 'cats_' + self.args.cats_command
        getattr(self, cats_command)()

    def cats_all(self):
        """clowder cats tests"""
        test_env = {}
        if self.args.write:
            test_env["ACCESS_LEVEL"] = 'write'
        else:
            test_env["ACCESS_LEVEL"] = 'read'
        return_code = execute_command('./test_example_cats.sh', self._scripts_dir, shell=True, env=test_env)
        sys.exit(return_code)

    def cats_branch(self):
        """clowder cats branch tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        return_code = execute_command('./branch.sh', path, shell=True)
        sys.exit(return_code)

    def cats_clean(self):
        """clowder cats clean tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        return_code = execute_command('./clean.sh', path, shell=True)
        sys.exit(return_code)

    def cats_diff(self):
        """clowder cats diff tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        return_code = execute_command('./diff.sh', path, shell=True)
        sys.exit(return_code)

    def cats_forall(self):
        """clowder cats forall tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        return_code = execute_command('./forall.sh', path, shell=True)
        sys.exit(return_code)

    def cats_help(self):
        """clowder cats help tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        return_code = execute_command('./help.sh', path, shell=True)
        sys.exit(return_code)

    def cats_herd_branch(self):
        """clowder cats herd branch tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        return_code = execute_command('./herd_branch.sh', path, shell=True)
        sys.exit(return_code)

    def cats_herd_tag(self):
        """clowder cats herd tag tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        return_code = execute_command('./herd_tag.sh', path, shell=True)
        sys.exit(return_code)

    def cats_herd(self):
        """clowder cats herd tests"""
        test_env = {}
        if self.args.write:
            test_env["ACCESS_LEVEL"] = 'write'
        else:
            test_env["ACCESS_LEVEL"] = 'read'
        path = os.path.join(self._scripts_dir, 'cats')
        return_code = execute_command('./herd.sh', path, shell=True, env=test_env)
        sys.exit(return_code)

    def cats_import(self):
        """clowder cats import tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        return_code = execute_command('./import.sh', path, shell=True)
        sys.exit(return_code)

    def cats_init(self):
        """clowder cats init tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        return_code = execute_command('./init.sh', path, shell=True)
        sys.exit(return_code)

    def cats_link(self):
        """clowder cats link tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        return_code = execute_command('./link.sh', path, shell=True)
        sys.exit(return_code)

    def cats_prune(self):
        """clowder cats prune tests"""
        test_env = {}
        if self.args.write:
            test_env["ACCESS_LEVEL"] = 'write'
        else:
            test_env["ACCESS_LEVEL"] = 'read'
        path = os.path.join(self._scripts_dir, 'cats')
        return_code = execute_command('./prune.sh', path, shell=True, env=test_env)
        sys.exit(return_code)

    def cats_repo(self):
        """clowder cats repo tests"""
        test_env = {}
        if self.args.write:
            test_env["ACCESS_LEVEL"] = 'write'
        else:
            test_env["ACCESS_LEVEL"] = 'read'
        path = os.path.join(self._scripts_dir, 'cats')
        return_code = execute_command('./repo.sh', path, shell=True, env=test_env)
        sys.exit(return_code)

    def cats_reset(self):
        """clowder cats reset tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        return_code = execute_command('./reset.sh', path, shell=True)
        sys.exit(return_code)

    def cats_save(self):
        """clowder cats save tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        return_code = execute_command('./save.sh', path, shell=True)
        sys.exit(return_code)

    def cats_start(self):
        """clowder cats start tests"""
        test_env = {}
        if self.args.write:
            test_env["ACCESS_LEVEL"] = 'write'
        else:
            test_env["ACCESS_LEVEL"] = 'read'
        path = os.path.join(self._scripts_dir, 'cats')
        return_code = execute_command('./start.sh', path, shell=True, env=test_env)
        sys.exit(return_code)

    def cats_stash(self):
        """clowder cats stash tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        return_code = execute_command('./stash.sh', path, shell=True)
        sys.exit(return_code)

    def cats_status(self):
        """clowder cats status tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        return_code = execute_command('./status.sh', path, shell=True)
        sys.exit(return_code)

    def cats_yaml_validation(self):
        """clowder cats yaml validation tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        return_code = execute_command('./yaml_validation.sh', path, shell=True)
        sys.exit(return_code)

    def cats_yaml(self):
        """clowder cats yaml tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        return_code = execute_command('./yaml.sh', path, shell=True)
        sys.exit(return_code)

    def cocos2d(self):
        """clowder cocos2d tests"""
        return_code = execute_command('./test_example_cocos2d.sh', self._scripts_dir, shell=True)
        sys.exit(return_code)

    def llvm(self):
        """clowder llvm tests"""
        test_env = {}
        if self.args.write:
            test_env["ACCESS_LEVEL"] = 'write'
        else:
            test_env["ACCESS_LEVEL"] = 'read'
        return_code = execute_command('./test_example_llvm.sh', self._scripts_dir, shell=True, env=test_env)
        sys.exit(return_code)

    def offline(self):
        """clowder offline tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        return_code = execute_command('./offline.sh', path, shell=True)
        sys.exit(return_code)

    def parallel(self):
        """clowder parallel tests"""
        return_code = execute_command('./test_parallel.sh', self._scripts_dir, shell=True)
        sys.exit(return_code)

    def swift(self):
        """clowder swift tests"""
        test_env = {}
        if self.args.write:
            test_env["ACCESS_LEVEL"] = 'write'
        else:
            test_env["ACCESS_LEVEL"] = 'read'
        return_code = execute_command('./test_example_swift.sh', self._scripts_dir, shell=True, env=test_env)
        sys.exit(return_code)

    def unittests(self):
        """clowder unit tests"""
        test_env = {}
        if self.args.version == 'python2':
            test_env["PYTHON_VERSION"] = 'python'
        else:
            test_env["PYTHON_VERSION"] = 'python3'
        return_code = execute_command('./unittests.sh', self._scripts_dir, shell=True, env=test_env)
        sys.exit(return_code)

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
        self._subparsers.add_parser('llvm', help='Run llvm tests')

    def _configure_offline_subparser(self):
        """clowder offline tests subparser"""
        self._subparsers.add_parser('offline', help='Run offline tests')

    def _configure_parallel_subparser(self):
        """clowder parallel tests subparser"""
        self._subparsers.add_parser('parallel', help='Run parallel tests')

    def _configure_swift_subparser(self):
        """clowder swift tests subparser"""
        self._subparsers.add_parser('swift', help='Run swift tests')

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


def execute_command(command, path, shell=True, env=None, print_output=True):
    """Run subprocess command"""
    cmd_env = os.environ.copy()
    process = None
    if env:
        cmd_env.update(env)
    if print_output:
        pipe = None
    else:
        pipe = subprocess.PIPE
    try:
        process = subprocess.Popen(command, shell=shell, env=cmd_env, cwd=path, stdout=pipe, stderr=pipe)
        atexit.register(subprocess_exit_handler)
        process.communicate()
    except (KeyboardInterrupt, SystemExit):
        if process:
            return process.returncode
        return 1
    else:
        return process.returncode


PARENT_ID = os.getpid()


def subprocess_exit_handler():
    """
    Process pool terminator
    Adapted from https://stackoverflow.com/a/45259908
    """

    def sig_int(signal_num, frame):
        """Signal handler"""
        # print('signal: %s' % signal_num)
        parent = psutil.Process(PARENT_ID)
        for child in parent.children():
            if child.pid != os.getpid():
                # print("killing child: %s" % child.pid)
                child.terminate()
        # print("killing parent: %s" % parent_id)
        parent.terminate()
        # print("suicide: %s" % os.getpid())
        psutil.Process(os.getpid()).terminate()
        print('\n\n')
    signal.signal(signal.SIGINT, sig_int)
