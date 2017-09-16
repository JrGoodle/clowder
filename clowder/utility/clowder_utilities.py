"""Clowder utilities"""
import errno
import os
import subprocess

def execute_command(cmd, path):
    """Execute command and display continuous output"""
    for output in execute(cmd, path):
        print(output, end='')

def execute(cmd, path):
    """Execute command"""
    # https://stackoverflow.com/questions/4417546/constantly-print-subprocess-output-while-process-is-running
    process = subprocess.Popen(cmd, cwd=path,
                               stdout=subprocess.PIPE,
                               universal_newlines=True)
    # print("the commandline is {}".format(process.args))
    for stdout_line in iter(process.stdout.readline, ''):
        yield stdout_line
    process.stdout.close()
    return_code = process.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

def force_symlink(file1, file2):
    """Force symlink creation"""
    try:
        os.symlink(file1, file2)
    except OSError as error:
        if error.errno == errno.EEXIST:
            os.remove(file2)
            os.symlink(file1, file2)
