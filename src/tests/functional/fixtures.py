"""
This module contains fixtures
"""

import os
import shutil
from pathlib import Path

# noinspection PyPackageRequirements
import pytest

import tests.functional.common as common


@pytest.fixture
def init_default(tmp_path: Path, example: str, cats_init_default: Path) -> None:
    if example == "cats":
        copy_directory(cats_init_default, to=tmp_path)
    else:
        assert False

    symlink = common.valid_clowder_symlink(tmp_path)
    os.unlink(symlink)
    command = "clowder link"
    common.run_command(command, tmp_path)


@pytest.fixture
def init_herd_default(tmp_path: Path, example: str, cats_init_herd_default: Path) -> None:
    if example == "cats":
        copy_directory(cats_init_herd_default, to=tmp_path)
    else:
        assert False


@pytest.fixture(scope="session")
def cats_init_herd_default(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(cats_init_herd_default.__name__)

    command = f"clowder init {common.get_url('cats', 'https')}"
    common.run_command(command, path)
    command = "clowder herd"
    common.run_command(command, path)

    validate_clowder_repo_with_symlink(path / ".clowder")

    for example, repo in common.CATS_REPOS_DEFAULT.items():
        repo_path = path / repo["path"]
        branch = repo["branch"]
        assert repo_path.exists()
        assert repo_path.is_dir()
        assert common.has_git_directory(repo_path)
        assert common.is_on_active_branch(repo_path, branch)
        assert not common.is_dirty(repo_path)

    return path


@pytest.fixture(scope="session")
def cats_init_default(tmp_path_factory) -> Path:
    tmp_path = tmp_path_factory.mktemp(cats_init_default.__name__)

    command = f"clowder init {common.get_url('cats', 'https')}"
    common.run_command(command, tmp_path)

    validate_clowder_repo_with_symlink(tmp_path / ".clowder")

    for example, repo in common.CATS_REPOS_DEFAULT.items():
        path = tmp_path / repo["path"]
        assert not path.exists()

    return tmp_path


def validate_clowder_repo_with_symlink(clowder_repo: Path) -> None:
    assert clowder_repo.exists()
    assert clowder_repo.is_dir()
    assert common.has_git_directory(clowder_repo)
    assert common.valid_clowder_symlink(clowder_repo.parent) is not None


def copy_directory(from_dir: Path, to: Path):
    shutil.copytree(from_dir, to, symlinks=True, dirs_exist_ok=True)
