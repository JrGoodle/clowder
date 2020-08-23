"""New syntax test file"""

import os
import subprocess
from pathlib import Path

from git import Repo
# noinspection PyPackageRequirements
from pytest_bdd import scenarios, given, when, then, parsers

scenarios('../features/new_syntax.feature')

TEST_REPOS = {
    "cats": {"url": "github.com", "name": "JrGoodle/cats"},
    "misc": {"url": "github.com", "name": "JrGoodle/misc-clowder-tests"},
    "swift": {"url": "github.com", "name": "JrGoodle/swift-clowder"}
}


@given(parsers.parse("{example} example is initialized"))
def example_init(tmpdir, example):
    url = get_url(example)
    command = f"clowder init {url}"
    run_command(command, tmpdir)


@given(parsers.parse("{example} example is initialized to {branch}"))
def example_init_branch(tmpdir, example, branch):
    url = get_url(example)
    command = f"clowder init {url} -b {branch}"
    run_command(command, tmpdir)


@given(parsers.parse("{example} example is initialized with {protocol}"))
def example_init_branch_protocol(tmpdir, example, protocol):
    url = get_url(example, protocol=protocol)
    command = f"clowder init {url}"
    run_command(command, tmpdir)


@given(parsers.parse("{example} example is initialized to {branch} with {protocol}"))
def example_init_branch_protocol(tmpdir, example, branch, protocol):
    url = get_url(example, protocol=protocol)
    command = f"clowder init {url} -b {branch}"
    run_command(command, tmpdir)


@given(parsers.parse("{version} yaml version is linked"))
def link_yaml_version(tmpdir, version):
    version_file = Path(tmpdir / ".clowder" / "versions" / f"{version}.clowder.yml")
    assert version_file.exists()
    command = f"clowder link {version}"
    run_command(command, tmpdir)
    path = Path(tmpdir / "clowder.yml")
    assert path.exists()
    assert path.is_file()
    assert path.is_symlink()
    assert version_file.samefile(path.resolve())


@given("I'm in an empty directory")
def is_empty_directory(tmpdir):
    print(f"tmpdir: {tmpdir}")
    assert is_directory_empty(tmpdir)


@given("<directory> doesn't exist")
def has_no_directory(tmpdir, directory):
    path = Path(tmpdir / directory)
    assert not path.exists()


@then("project at <directory> exists")
def has_directory(tmpdir, directory):
    path = Path(tmpdir / directory)
    assert path.exists()


@then("project at <directory> is a git repository")
def is_git_repo(tmpdir, directory):
    path = Path(tmpdir / directory)
    assert path.exists()
    assert has_git_directory(path)


@when(parsers.parse("I run 'clowder {command}'"))
def run_clowder(tmpdir, command):
    run_command(f"clowder {command}", tmpdir)


@then("project at <directory> is on <branch>")
def check_directory_branch(tmpdir, directory, branch):
    path = Path(tmpdir / directory)
    repo = Repo(str(path))
    active_branch = repo.active_branch.name
    print(f"TEST: active brach '{active_branch}' is '{branch}'")
    assert active_branch == branch


@then("project at <directory> is clean")
def check_directory_clean(tmpdir, directory):
    path = Path(tmpdir / directory)
    repo = Repo(str(path))
    print(f"TEST: Project at {directory} is clean")
    assert not is_dirty(repo)


def is_dirty(repo) -> bool:
    """Check whether repo is dirty

    :return: True, if repo is dirty
    :rtype: bool
    """

    # if not self.repo_path.is_dir():
    #     return False

    return repo.is_dirty()  # or self._is_rebase_in_progress() or self._has_untracked_files()


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


def has_git_directory(dir_name):
    path = Path(dir_name / ".git")
    return path.is_dir()


def run_command(command, path):
    print(f"TEST: {command}")
    # pipe = None if print_output else subprocess.PIPE
    subprocess.run(command, shell=True, cwd=path, check=True)


def get_url(example, protocol="ssh"):
    source_url = TEST_REPOS[example]["url"]
    name = TEST_REPOS[example]["name"]
    if protocol == "ssh":
        url = f"git@{source_url}:{name}.git"
    elif protocol == "https":
        url = f"https://{source_url}/{name}.git"
    else:
        raise Exception
    print(f"TEST: {url}")
    return url
