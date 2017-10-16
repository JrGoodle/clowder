"""Git utilities"""

from __future__ import print_function
# import atexit
import multiprocessing as mp
import os
import signal
import sys
import psutil
from termcolor import cprint
from clowder.exception.clowder_git_exception import ClowderGitException


class ClowderPool(object):
    """Wrapper for multiprocessing Pool"""

    def __init__(self):
        self._pool = mp.Pool(initializer=worker_init)

    def apply_async(self, func, args=(), kwds={}, callback=None, error_callback=None):
        """Wrapper for Pool apply_async"""
        return self._pool.apply_async(func, args=args, kwds=kwds, callback=callback, error_callback=error_callback)

    def close(self):
        """Wrapper for Pool close"""
        self._pool.close()

    def join(self):
        """Wrapper for Pool join"""
        try:
            self._pool.join()
        except (KeyboardInterrupt, SystemExit, ClowderGitException):
            self._pool.terminate()
            sys.exit(1)

    def terminate(self, err):
        """Wrapper for Pool terminate"""
        cprint(" - Command terminated", 'red')
        print(err)
        self._pool.terminate()


# def subprocess_exit_handler(process):
#     """terminate subprocess"""
#     try:
#         os.kill(process.pid, 0)
#         process.kill()
#     except:
#         pass


PARENT_ID = os.getpid()


def worker_init():
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
                child.kill()
        # print("killing parent: %s" % parent_id)
        parent.kill()
        # print("suicide: %s" % os.getpid())
        psutil.Process(os.getpid()).kill()
        print('\n\n')
    signal.signal(signal.SIGINT, sig_int)
