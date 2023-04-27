"""
This module contains fixtures
"""

from pathlib import Path

from pytest import fixture

import pygoodle.filesystem as fs

import tests.functional.util as util


@fixture
def cats_init_herd(tmp_path: Path, cats_init_herd_session: Path) -> None:
    fs.copy_directory(cats_init_herd_session, to_path=tmp_path)


@fixture(scope="session")
def cats_init_herd_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(cats_init_herd_session.__name__)
    return util.init_herd_clowder(path, "cats")


@fixture
def cats_init_herd_ssh(tmp_path: Path, cats_init_herd_ssh_session: Path) -> None:
    fs.copy_directory(cats_init_herd_ssh_session, to_path=tmp_path)


@fixture(scope="session")
def cats_init_herd_ssh_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(cats_init_herd_ssh_session.__name__)
    return util.init_herd_clowder(path, "cats", protocol="ssh", version="ssh")


# @fixture
# def cats_init_yaml_validation_herd_test_empty_project(tmp_path: Path, cats_init_yaml_validation_herd_test_empty_project_session: Path) -> None:  # noqa
#     util.copy_directory(cats_init_yaml_validation_herd_test_empty_project_session, to_path=tmp_path)
#
# @fixture(scope="session")
# def cats_init_yaml_validation_herd_test_empty_project_session(tmp_path_factory) -> Path:
#     path = tmp_path_factory.mktemp(cats_init_yaml_validation_herd_test_empty_project_session.__name__)
#     return util.init_herd_clowder(path, "cats", branch="yaml-validation", version="test-empty-project")
