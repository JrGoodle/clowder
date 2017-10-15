"""Git utilities"""

from __future__ import print_function
import atexit
import multiprocessing as mp
import os
import signal
import subprocess
import sys
# from clowder.utility.clowder_utilities import suppress_stdout


class ClowderPool(object):
    """Wrapper for multiprocessing Pool"""

    pids = []

    def __init__(self):
        # original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
        self._pool = mp.Pool()
        # signal.signal(signal.SIGINT, original_sigint_handler)

    def apply_async(self, func, arguments):
        """Wrapper for Pool apply_async"""
        # with suppress_stdout():
        self._pool.apply_async(func, kwds=arguments)  # , error_callback=self.kill_pool)

    def close(self):
        """Wrapper for Pool close"""
        self._pool.close()

    @classmethod
    def execute_command(cls, command, path, shell=True, env=None):
        """Run subprocess command"""
        cmd_env = os.environ.copy()
        if env is not None:
            cmd_env.update(env)
        try:
            process = subprocess.Popen(" ".join(command), shell=shell, env=cmd_env, cwd=path, preexec_fn=os.setsid)
            atexit.register(subprocess_exit_handler, process)
            cls.pids.append(process.pid)
            process.communicate()
        except (KeyboardInterrupt, SystemExit):
            os.kill(process.pid, signal.SIGTERM)
        return process.returncode

    @classmethod
    def execute_forall_command(cls, command, path, clowder_path, name, remote, fork_remote, ref):
        """Execute forall command with additional environment variables and display continuous output"""
        forall_env = {'CLOWDER_PATH': clowder_path, 'PROJECT_PATH': path, 'PROJECT_NAME': name,
                      'PROJECT_REMOTE': remote, 'PROJECT_REF': ref}
        if fork_remote is not None:
            forall_env['FORK_REMOTE'] = fork_remote
        return cls.execute_command(command, path, shell=True, env=forall_env)

    def join(self):
        """Wrapper for Pool join"""
        try:
            self._pool.join()
        except (KeyboardInterrupt, SystemExit) as err:
            self.kill_pool(err)
            sys.exit(1)

    def kill_pool(self, err_msg):
        """Error handler for process pool"""
        print(err_msg)
        for pid in self.pids:
            try:
                # os.kill(pid, signal.SIGTERM)
                os.killpg(os.getpgid(pid), signal.SIGTERM)
            except:
                pass
        self._pool.terminate()

    def terminate(self):
        """Wrapper for Pool terminate"""
        self._pool.terminate()


def subprocess_exit_handler(process):
    """terminate subprocess"""
    try:
        os.kill(process.pid, 0)
        process.kill()
    except:
        pass
