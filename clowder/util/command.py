"""Subprocess command utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import os
import subprocess
from pathlib import Path
from subprocess import CompletedProcess, PIPE, STDOUT
from typing import List, Optional, Union

from .console import CONSOLE
from .format import Format


def get_stdout(command: str, cwd: Path = Path.cwd()) -> Optional[str]:
    if not cwd.is_dir():
        return None
    result = run(command, cwd=cwd, print_output=False, check=False)
    if result.returncode != 0:
        return None
    output: str = result.stdout
    output = output.strip()
    if not output:
        return None
    return output


def run_silent(command: str, cwd: Path = Path.cwd()) -> CompletedProcess:
    return run(command, cwd=cwd, check=False, print_output=False)


def run(command: Union[str, List[str]], cwd: Path = Path.cwd(), check: bool = True,
        env: Optional[dict] = None, stdout=PIPE, stderr=STDOUT,
        print_output: Optional[bool] = None, print_command: bool = False,
        login: bool = False, interactive: bool = False, executable: Optional[str] = None) -> CompletedProcess:

    if print_output is None:
        print_output = CONSOLE.print_output

    if print_output:
        stdout = None
        stderr = None

    if print_command:
        output = Format.default(f"> {command}")
        output = Format.bold(output)
        CONSOLE.stdout(output)

    # if isinstance(command, list):
    #     cmd = ' '.join(command)
    # else:
    #     cmd = command

    if isinstance(command, str):
        command = [command]
    if login:
        command = ['-l'] + command
    if interactive:
        command = ['-i'] + command

    cmd_env = os.environ.copy()
    if env is not None:
        cmd_env.update(env)

    if executable is not None:
        executable = executable
        cmd_env['SHELL'] = executable

    # TODO: Replace universal_newlines with text when Python 3.6 support is dropped
    completed_process = subprocess.run(
        command,
        cwd=cwd,
        env=cmd_env,
        shell=True,
        stdout=stdout,
        stderr=stderr,
        universal_newlines=True,
        check=check,
        executable=executable
    )

    return completed_process
