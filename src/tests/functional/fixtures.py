"""
This module contains fixtures
"""

import os
import shutil
from pathlib import Path

# noinspection PyPackageRequirements
from pytest import fixture

import tests.functional.util as util
from .util import CommandResults, TestInfo


@fixture
def command_results() -> CommandResults:
    return CommandResults()


@fixture
def test_info() -> TestInfo:
    return TestInfo()


@fixture
def misc_init_default(tmp_path: Path, misc_init_default_session: Path) -> None:
    copy_directory(misc_init_default_session, to=tmp_path)
    symlink = util.valid_clowder_symlink(tmp_path)
    os.unlink(symlink)
    command = "clowder link"
    util.run_command(command, tmp_path, check=True)


@fixture
def misc_init_herd_default(tmp_path: Path, misc_init_herd_default_session: Path) -> None:
    copy_directory(misc_init_herd_default_session, to=tmp_path)
    symlink = util.valid_clowder_symlink(tmp_path)
    os.unlink(symlink)
    command = "clowder link"
    util.run_command(command, tmp_path, check=True)


@fixture
def cats_init_default(tmp_path: Path, cats_init_default_session: Path) -> None:
    copy_directory(cats_init_default_session, to=tmp_path)
    symlink = util.valid_clowder_symlink(tmp_path)
    os.unlink(symlink)
    command = "clowder link"
    util.run_command(command, tmp_path, check=True)


@fixture
def cats_init_herd_default(tmp_path: Path, cats_init_herd_default_session: Path) -> None:
    copy_directory(cats_init_herd_default_session, to=tmp_path)
    symlink = util.valid_clowder_symlink(tmp_path)
    os.unlink(symlink)
    command = "clowder link"
    util.run_command(command, tmp_path, check=True)


@fixture(scope="session")
def cats_init_herd_default_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(cats_init_herd_default_session.__name__)

    command = f"clowder init {util.get_url('cats', 'https')}"
    util.run_command(command, path, check=True)
    command = "clowder herd"
    util.run_command(command, path, check=True)

    validate_clowder_repo_with_symlink(path / ".clowder")

    for example, repo in util.CATS_REPOS_DEFAULT.items():
        repo_path = path / repo["path"]
        branch = repo["branch"]
        assert repo_path.exists()
        assert repo_path.is_dir()
        assert util.has_git_directory(repo_path)
        assert util.is_on_active_branch(repo_path, branch)
        assert not util.is_dirty(repo_path)

    return path


@fixture(scope="session")
def misc_init_herd_default_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(misc_init_herd_default_session.__name__)

    command = f"clowder init {util.get_url('misc', 'https')}"
    util.run_command(command, path, check=True)
    command = "clowder herd"
    util.run_command(command, path, check=True)

    validate_clowder_repo_with_symlink(path / ".clowder")

    for example, repo in util.MISC_REPOS_DEFAULT.items():
        repo_path = path / repo["path"]
        branch = repo["branch"]
        assert repo_path.exists()
        assert repo_path.is_dir()
        assert util.has_git_directory(repo_path)
        assert util.is_on_active_branch(repo_path, branch)
        assert not util.is_dirty(repo_path)

    return path


@fixture(scope="session")
def cats_init_default_session(tmp_path_factory) -> Path:
    tmp_path = tmp_path_factory.mktemp(cats_init_default_session.__name__)

    command = f"clowder init {util.get_url('cats', 'https')}"
    util.run_command(command, tmp_path, check=True)

    validate_clowder_repo_with_symlink(tmp_path / ".clowder")

    for example, repo in util.CATS_REPOS_DEFAULT.items():
        path = tmp_path / repo["path"]
        assert not path.exists()

    return tmp_path


@fixture(scope="session")
def misc_init_default_session(tmp_path_factory) -> Path:
    tmp_path = tmp_path_factory.mktemp(misc_init_default_session.__name__)

    command = f"clowder init {util.get_url('misc', 'https')}"
    util.run_command(command, tmp_path, check=True)

    validate_clowder_repo_with_symlink(tmp_path / ".clowder")

    for example, repo in util.MISC_REPOS_DEFAULT.items():
        path = tmp_path / repo["path"]
        assert not path.exists()

    return tmp_path


def validate_clowder_repo_with_symlink(clowder_repo: Path) -> None:
    assert clowder_repo.exists()
    assert clowder_repo.is_dir()
    assert util.has_git_directory(clowder_repo)
    assert util.valid_clowder_symlink(clowder_repo.parent) is not None


def copy_directory(from_dir: Path, to: Path):
    # TODO: Replace rmdir() with copytree(dirs_exist_ok=True) when support for Python 3.7 is dropped
    to.rmdir()
    shutil.copytree(from_dir, to, symlinks=True)
