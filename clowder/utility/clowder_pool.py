"""Git utilities"""

from __future__ import print_function
import multiprocessing as mp
import signal
# from clowder.utility.clowder_utilities import suppress_stdout


class ClowderPool(object):
    """Wrapper for multiprocessing Pool"""

    def __init__(self):
        original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
        self._pool = mp.Pool()
        signal.signal(signal.SIGINT, original_sigint_handler)

    def apply_async(self, function, arguments):
        """Wrapper for Pool apply_async"""
        # with suppress_stdout():
        self._pool.apply_async(function, arguments, error_callback=self.kill_pool)

    def close(self):
        """Wrapper for Pool close"""
        self._pool.close()

    def join(self):
        """Wrapper for Pool join"""
        self._pool.join()

    def kill_pool(self, err_msg):
        """Error handler for process pool"""
        print(err_msg)
        self._pool.terminate()
        self._pool.join()

    def terminate(self):
        """Wrapper for Pool terminate"""
        self._pool.terminate()
