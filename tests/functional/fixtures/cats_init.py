"""
This module contains fixtures
"""

import os
from pathlib import Path

from pytest import fixture

import tests.functional.util as util


@fixture
def cats_init(tmp_path: Path, cats_init_session: Path) -> None:
    util.copy_directory(cats_init_session, to=tmp_path)
    # TODO: Remove once clowder.yml is relative symlink
    symlink = util.valid_clowder_symlink(tmp_path)
    os.unlink(symlink)
    result = util.run_command("clowder link", tmp_path)
    assert result.returncode == 0


@fixture(scope="session")
def cats_init_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(cats_init_session.__name__)
    return util.init_clowder(path, "cats")


@fixture
def cats_init_extension(tmp_path: Path, cats_init_extension_session: Path) -> None:
    util.copy_directory(cats_init_extension_session, to=tmp_path)
    # TODO: Remove once clowder.yml is relative symlink
    symlink = util.valid_clowder_symlink(tmp_path)
    os.unlink(symlink)
    result = util.run_command("clowder link", tmp_path)
    assert result.returncode == 0


@fixture(scope="session")
def cats_init_extension_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(cats_init_extension_session.__name__)
    return util.init_clowder(path, "cats", branch="extension")


@fixture
def cats_init_ssh(tmp_path: Path, cats_init_ssh_session: Path) -> None:
    util.copy_directory(cats_init_ssh_session, to=tmp_path)
    # TODO: Remove once clowder.yml is relative symlink
    symlink = util.valid_clowder_symlink(tmp_path)
    os.unlink(symlink)
    result = util.run_command("clowder link ssh", tmp_path)
    assert result.returncode == 0


@fixture(scope="session")
def cats_init_ssh_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(cats_init_ssh_session.__name__)
    return util.init_clowder(path, "cats", protocol="ssh", version="ssh")
