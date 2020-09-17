#!/usr/bin/env python

import os
import random
import shutil
import string
import subprocess
import sys
from pathlib import Path
from subprocess import CompletedProcess
from typing import Optional


def run_command(cwd: Path, cmd: str) -> CompletedProcess:
    cmd_env = os.environ.copy()
    completed_process = subprocess.run(cmd, cwd=cwd, shell=True, env=cmd_env)
    return completed_process


def start_docker() -> None:
    build_ssh_dir = path / "build" / "ssh"
    shutil.rmtree(build_dir, ignore_errors=True)
    home_ssh_dir = Path.home() / ".ssh"
    shutil.copytree(home_ssh_dir, build_ssh_dir)

    result = run_command(path, "docker-compose up --build -d")
    print(result.stdout)
    result = run_command(path, "docker-compose exec --privileged clowder pip install --requirement requirements.txt")
    print(result.stdout)
    result = run_command(path, "docker-compose exec --privileged clowder pip install --editable .")
    print(result.stdout)

    shutil.rmtree(build_ssh_dir, ignore_errors=True)


def stop_docker() -> None:
    run_command(path, "docker-compose rm --force --stop clowder")


command_arg = ""
if len(sys.argv) == 2:
    command_arg = sys.argv[1]
else:
    print("Wrong number of arguments")
    exit(1)

# Repo path
path = Path(__file__).resolve().parent.parent.resolve()

if command_arg == "start":
    start_docker()
elif command_arg == "stop":
    stop_docker()
else:
    print("Unknown argument")
    exit(1)
