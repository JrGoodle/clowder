"""Process pool"""

import multiprocessing as mp
import os
import signal

import psutil

from clowder.util.progress import Progress


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


RESULTS = []
POOL = mp.Pool(initializer=worker_init)
PROGRESS = Progress()
