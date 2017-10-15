"""Git utilities"""

from __future__ import print_function
# import atexit
import multiprocessing as mp
import os
import psutil
import signal
import subprocess
import sys
# from clowder.utility.clowder_utilities import suppress_stdout


class ClowderPool(object):
    """Wrapper for multiprocessing Pool"""

    def __init__(self):
        self._pool = mp.Pool(initializer=worker_init)

    @classmethod
    def execute_command(cls, command, path, shell=True, env=None, print_output=True):
        """Run subprocess command"""
        cmd_env = os.environ.copy()
        if env is not None:
            cmd_env.update(env)
        try:
            if print_output:
                process = subprocess.Popen('exec ' + ' '.join(command), shell=shell, env=cmd_env, cwd=path)
            else:
                process = subprocess.Popen('exec ' + ' '.join(command), shell=shell, env=cmd_env, cwd=path,
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # atexit.register(subprocess_exit_handler, process)
            process.communicate()
        except (KeyboardInterrupt, SystemExit):
            process.kill()
        return process.returncode

    @classmethod
    def execute_forall_command(cls, command, path, clowder_path, name, remote, fork_remote, ref, print_output=True):
        """Execute forall command with additional environment variables and display continuous output"""
        forall_env = {'CLOWDER_PATH': clowder_path, 'PROJECT_PATH': path, 'PROJECT_NAME': name,
                      'PROJECT_REMOTE': remote, 'PROJECT_REF': ref}
        if fork_remote is not None:
            forall_env['FORK_REMOTE'] = fork_remote
        return cls.execute_command(command, path, shell=True, env=forall_env, print_output=print_output)

    def apply_async(self, func, arguments):
        """Wrapper for Pool apply_async"""
        # with suppress_stdout():
        self._pool.apply_async(func, kwds=arguments)

    def close(self):
        """Wrapper for Pool close"""
        self._pool.close()

    def join(self):
        """Wrapper for Pool join"""
        try:
            self._pool.join()
        except (KeyboardInterrupt, SystemExit):
            self._pool.terminate()
            sys.exit(1)

    # def kill_pool(self, err_msg):
    #     """Error handler for process pool"""
    #     print(err_msg)
    #     self._pool.terminate()

    def terminate(self):
        """Wrapper for Pool terminate"""
        self._pool.terminate()


# def subprocess_exit_handler(process):
#     """terminate subprocess"""
#     try:
#         os.kill(process.pid, 0)
#         process.kill()
#     except:
#         pass


parent_id = os.getpid()



def worker_init():
    """
    Process pool terminator
    Adapted from https://stackoverflow.com/a/45259908
    """
    def sig_int(signal_num, frame):
        # print('signal: %s' % signal_num)
        parent = psutil.Process(parent_id)
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