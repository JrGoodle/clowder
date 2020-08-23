"""New syntax test file"""

import os
import subprocess

# noinspection PyPackageRequirements
from pytest_bdd import scenarios, given, when, then, parsers

scenarios('../features/new_syntax.feature')


@given("I'm using the default cats clowder.yml")
def step_impl():
    pass


@given("I'm in an empty directory")
def is_empty_directory(tmpdir):
    print(f"tmpdir: {tmpdir}")
    assert is_directory_empty(tmpdir)


@when(parsers.parse("I run 'clowder {command}'"))
def run_clowder(tmpdir, command):
    # pipe = None if print_output else subprocess.PIPE
    subprocess.run(f"clowder {command}", shell=True, cwd=tmpdir, check=True)


@then(parsers.parse("Project at directory {directory} is on branch {branch}"))
def check_directory_branch(directory, branch):
    # Check branch at directory path
    pass


def is_directory_empty(dir_name):
    if os.path.exists(dir_name) and os.path.isdir(dir_name):
        if not os.listdir(dir_name):
            print("Directory is empty")
            return True
        else:
            print("Directory is not empty")
            return False
    else:
        print("Given Directory don't exists")
        raise Exception
