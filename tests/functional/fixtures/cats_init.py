"""
This module contains fixtures
"""

from pathlib import Path

from pytest import fixture

import pygoodle.filesystem as fs

import tests.functional.util as util


@fixture
def cats_init(tmp_path: Path, cats_init_session: Path) -> None:
    fs.copy_directory(cats_init_session, to=tmp_path)


@fixture(scope="session")
def cats_init_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(cats_init_session.__name__)
    return util.init_clowder(path, "cats")


@fixture
def cats_init_extension(tmp_path: Path, cats_init_extension_session: Path) -> None:
    fs.copy_directory(cats_init_extension_session, to=tmp_path)


@fixture(scope="session")
def cats_init_extension_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(cats_init_extension_session.__name__)
    return util.init_clowder(path, "cats", branch="extension")


@fixture
def cats_init_ssh(tmp_path: Path, cats_init_ssh_session: Path) -> None:
    fs.copy_directory(cats_init_ssh_session, to=tmp_path)


@fixture(scope="session")
def cats_init_ssh_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(cats_init_ssh_session.__name__)
    return util.init_clowder(path, "cats", protocol="ssh", version="ssh")
