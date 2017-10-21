"""Main entrypoint for clowder test runner"""

from __future__ import print_function

import argparse
import multiprocessing as mp
import os
import signal
import sys

import argcomplete
import psutil
from termcolor import cprint

from clowder_test.execute import execute_command

# Disable errors shown by pylint for too many public methods
# pylint: disable=R0904
# Disable errors shown by pylint for no specified exception types
# pylint: disable=W0702


PARENT_ID = os.getpid()


def worker_init():
    """
    Process pool terminator
    Adapted from https://stackoverflow.com/a/45259908
    """
    def sig_int(signal_num, frame):
        """Signal handler"""
        del signal_num, frame
        # print('signal: %s' % signal_num)
        parent = psutil.Process(PARENT_ID)
        for child in parent.children(recursive=True):
            if child.pid != os.getpid():
                # print("killing child: %s" % child.pid)
                child.terminate()
        # print("killing parent: %s" % parent_id)
        parent.terminate()
        # print("suicide: %s" % os.getpid())
        psutil.Process(os.getpid()).terminate()
        print('\n\n')
    signal.signal(signal.SIGINT, sig_int)


POOL = mp.Pool(initializer=worker_init)


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
        result = POOL.apply_async(execute_command, args=(['./test_example_cats.sh'], self._scripts_dir),
                                  kwds={'shell': True, 'env': test_env})
        pool_handler(result)
        POOL.close()
        POOL.join()

    def cats_branch(self):
        """clowder cats branch tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        result = POOL.apply_async(execute_command, args=(['./branch.sh'], path), kwds={'shell': True})
        pool_handler(result)
        POOL.close()
        POOL.join()

    def cats_clean(self):
        """clowder cats clean tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        result = POOL.apply_async(execute_command, args=(['./clean.sh'], path), kwds={'shell': True})
        pool_handler(result)
        POOL.close()
        POOL.join()

    def cats_diff(self):
        """clowder cats diff tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        result = POOL.apply_async(execute_command, args=(['./diff.sh'], path), kwds={'shell': True})
        pool_handler(result)
        POOL.close()
        POOL.join()

    def cats_forall(self):
        """clowder cats forall tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        result = POOL.apply_async(execute_command, args=(['./forall.sh'], path), kwds={'shell': True})
        pool_handler(result)
        POOL.close()
        POOL.join()

    def cats_help(self):
        """clowder cats help tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        result = POOL.apply_async(execute_command, args=(['./help.sh'], path), kwds={'shell': True})
        pool_handler(result)
        POOL.close()
        POOL.join()

    def cats_herd_branch(self):
        """clowder cats herd branch tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        result = POOL.apply_async(execute_command, args=(['./herd_branch.sh'], path), kwds={'shell': True})
        pool_handler(result)
        POOL.close()
        POOL.join()

    def cats_herd_tag(self):
        """clowder cats herd tag tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        result = POOL.apply_async(execute_command, args=(['./herd_tag.sh'], path), kwds={'shell': True})
        pool_handler(result)
        POOL.close()
        POOL.join()

    def cats_herd(self):
        """clowder cats herd tests"""
        test_env = {}
        if self.args.write:
            test_env["ACCESS_LEVEL"] = 'write'
        else:
            test_env["ACCESS_LEVEL"] = 'read'
        path = os.path.join(self._scripts_dir, 'cats')
        result = POOL.apply_async(execute_command, args=(['./herd.sh'], path), kwds={'shell': True})
        pool_handler(result)
        POOL.close()
        POOL.join()

    def cats_import(self):
        """clowder cats import tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        result = POOL.apply_async(execute_command, args=(['./import.sh'], path), kwds={'shell': True})
        pool_handler(result)
        POOL.close()
        POOL.join()

    def cats_init(self):
        """clowder cats init tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        result = POOL.apply_async(execute_command, args=(['./init.sh'], path), kwds={'shell': True})
        pool_handler(result)
        POOL.close()
        POOL.join()

    def cats_link(self):
        """clowder cats link tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        result = POOL.apply_async(execute_command, args=(['./link.sh'], path), kwds={'shell': True})
        pool_handler(result)
        POOL.close()
        POOL.join()

    def cats_prune(self):
        """clowder cats prune tests"""
        test_env = {}
        if self.args.write:
            test_env["ACCESS_LEVEL"] = 'write'
        else:
            test_env["ACCESS_LEVEL"] = 'read'
        path = os.path.join(self._scripts_dir, 'cats')
        result = POOL.apply_async(execute_command, args=(['./prune.sh'], path), kwds={'shell': True})
        pool_handler(result)
        POOL.close()
        POOL.join()

    def cats_repo(self):
        """clowder cats repo tests"""
        test_env = {}
        if self.args.write:
            test_env["ACCESS_LEVEL"] = 'write'
        else:
            test_env["ACCESS_LEVEL"] = 'read'
        path = os.path.join(self._scripts_dir, 'cats')
        result = POOL.apply_async(execute_command, args=(['./repo.sh'], path), kwds={'shell': True})
        pool_handler(result)
        POOL.close()
        POOL.join()

    def cats_reset(self):
        """clowder cats reset tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        result = POOL.apply_async(execute_command, args=(['./reset.sh'], path), kwds={'shell': True})
        pool_handler(result)
        POOL.close()
        POOL.join()

    def cats_save(self):
        """clowder cats save tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        result = POOL.apply_async(execute_command, args=(['./save.sh'], path), kwds={'shell': True})
        pool_handler(result)
        POOL.close()
        POOL.join()

    def cats_start(self):
        """clowder cats start tests"""
        test_env = {}
        if self.args.write:
            test_env["ACCESS_LEVEL"] = 'write'
        else:
            test_env["ACCESS_LEVEL"] = 'read'
        path = os.path.join(self._scripts_dir, 'cats')
        result = POOL.apply_async(execute_command, args=(['./start.sh'], path), kwds={'shell': True})
        pool_handler(result)
        POOL.close()
        POOL.join()

    def cats_stash(self):
        """clowder cats stash tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        return_code = execute_command(['./stash.sh'], path, shell=True)
        sys.exit(return_code)

    def cats_status(self):
        """clowder cats status tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        result = POOL.apply_async(execute_command, args=(['./status.sh'], path), kwds={'shell': True})
        pool_handler(result)
        POOL.close()
        POOL.join()

    def cats_yaml_validation(self):
        """clowder cats yaml validation tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        result = POOL.apply_async(execute_command, args=(['./yaml_validation.sh'], path), kwds={'shell': True})
        pool_handler(result)
        POOL.close()
        POOL.join()

    def cats_yaml(self):
        """clowder cats yaml tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        result = POOL.apply_async(execute_command, args=(['./yaml.sh'], path), kwds={'shell': True})
        pool_handler(result)
        POOL.close()
        POOL.join()

    def cocos2d(self):
        """clowder cocos2d tests"""
        result = POOL.apply_async(execute_command,
                                  args=(['./test_example_cocos2d.sh'], self._scripts_dir),
                                  kwds={'shell': True})
        pool_handler(result)
        POOL.close()
        POOL.join()

    def llvm(self):
        """clowder llvm tests"""
        test_env = {}
        if self.args.write:
            test_env["ACCESS_LEVEL"] = 'write'
        else:
            test_env["ACCESS_LEVEL"] = 'read'
        result = POOL.apply_async(execute_command,
                                  args=(['./test_example_llvm.sh'], self._scripts_dir),
                                  kwds={'shell': True, 'env': test_env})
        pool_handler(result)
        POOL.close()
        POOL.join()

    def offline(self):
        """clowder offline tests"""
        path = os.path.join(self._scripts_dir, 'cats')
        result = POOL.apply_async(execute_command, args=(['./offline.sh'], path), kwds={'shell': True})
        pool_handler(result)
        POOL.close()
        POOL.join()

    def parallel(self):
        """clowder parallel tests"""
        result = POOL.apply_async(execute_command,
                                  args=(['./test_parallel.sh'], self._scripts_dir),
                                  kwds={'shell': True})
        pool_handler(result)
        POOL.close()
        POOL.join()

    def swift(self):
        """clowder swift tests"""
        test_env = {}
        if self.args.write:
            test_env["ACCESS_LEVEL"] = 'write'
        else:
            test_env["ACCESS_LEVEL"] = 'read'
        result = POOL.apply_async(execute_command,
                                  args=(['./test_example_swift.sh'], self._scripts_dir),
                                  kwds={'shell': True, 'env': test_env})
        pool_handler(result)
        POOL.close()
        POOL.join()

    def unittests(self):
        """clowder unit tests"""
        test_env = {}
        if self.args.version == 'python2':
            test_env["PYTHON_VERSION"] = 'python'
        else:
            test_env["PYTHON_VERSION"] = 'python3'
        result = POOL.apply_async(execute_command,
                                  args=(['./unittests.sh'], self._scripts_dir),
                                  kwds={'shell': True, 'env': test_env})
        pool_handler(result)
        POOL.close()
        POOL.join()

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


def pool_handler(result):
    """Pool handler for finishing jobs"""
    try:
        result.get()
        if not result.successful():
            print()
            cprint(' - Test failed', 'red')
            print()
            POOL.close()
            POOL.join()
            sys.exit(1)
    except Exception as err:
        print()
        cprint(err, 'red')
        print()
        POOL.close()
        POOL.join()
        sys.exit(1)

def exit_unrecognized_command(parser):
    """Print unrecognized command message and exit"""
    parser.print_help()
    print()
    sys.exit(1)
