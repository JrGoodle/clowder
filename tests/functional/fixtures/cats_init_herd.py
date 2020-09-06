"""
This module contains fixtures
"""

import os
from pathlib import Path

from pytest import fixture

import tests.functional.util as util


@fixture
def cats_init_herd(tmp_path: Path, cats_init_herd_session: Path) -> None:
    util.copy_directory(cats_init_herd_session, to=tmp_path)
    # TODO: Remove once clowder.yml is relative symlink
    symlink = util.valid_clowder_symlink(tmp_path)
    os.unlink(symlink)
    util.run_command("clowder link", tmp_path, check=True)


@fixture(scope="session")
def cats_init_herd_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(cats_init_herd_session.__name__)
    return util.init_herd_clowder(path, "cats")


@fixture
def cats_init_herd_ssh(tmp_path: Path, cats_init_herd_ssh_session: Path) -> None:
    util.copy_directory(cats_init_herd_ssh_session, to=tmp_path)
    # TODO: Remove once clowder.yml is relative symlink
    symlink = util.valid_clowder_symlink(tmp_path)
    os.unlink(symlink)
    util.run_command("clowder link ssh", tmp_path, check=True)


@fixture(scope="session")
def cats_init_herd_ssh_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(cats_init_herd_ssh_session.__name__)
    return util.init_herd_clowder(path, "cats", protocol="ssh", version="ssh")


# @fixture
# def cats_init_yaml_validation_herd_test_empty_project(tmp_path: Path, cats_init_yaml_validation_herd_test_empty_project_session: Path) -> None: # noqa
#     util.copy_directory(cats_init_yaml_validation_herd_test_empty_project_session, to=tmp_path)
#     # TODO: Remove once clowder.yml is relative symlink
#     symlink = util.valid_clowder_symlink(tmp_path)
#     os.unlink(symlink)
#     util.run_command("clowder link test-empty-project", tmp_path, check=True)
#
#
# @fixture(scope="session")
# def cats_init_yaml_validation_herd_test_empty_project_session(tmp_path_factory) -> Path:
#     path = tmp_path_factory.mktemp(cats_init_yaml_validation_herd_test_empty_project_session.__name__)
#     return util.init_herd_clowder(path, "cats", branch="yaml-validation", version="test-empty-project")
