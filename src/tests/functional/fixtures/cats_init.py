"""
This module contains fixtures
"""

import os
from pathlib import Path

# noinspection PyPackageRequirements
from pytest import fixture

import tests.functional.util as util


@fixture
def cats_init(tmp_path: Path, cats_init_session: Path) -> None:
    util.copy_directory(cats_init_session, to=tmp_path)
    # TODO: Remove once clowder.yml is relative symlink
    symlink = util.valid_clowder_symlink(tmp_path)
    os.unlink(symlink)
    util.run_command("clowder link", tmp_path, check=True)


@fixture(scope="session")
def cats_init_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(cats_init_session.__name__)
    return util.init_clowder(path, "cats")


@fixture
def cats_init_yaml_validation(tmp_path: Path, cats_init_yaml_validation_session: Path) -> None:
    util.copy_directory(cats_init_yaml_validation_session, to=tmp_path)
    # TODO: Remove once clowder.yml is relative symlink
    symlink = util.valid_clowder_symlink(tmp_path)
    os.unlink(symlink)
    result = util.run_command("clowder link", tmp_path)
    assert result.returncode == 0


@fixture(scope="session")
def cats_init_yaml_validation_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(cats_init_yaml_validation_session.__name__)
    return util.init_clowder(path, "cats", branch="yaml-validation")


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
def cats_non_symlink_yaml(tmp_path: Path, cats_non_symlink_yaml_session: Path) -> None:
    util.copy_directory(cats_non_symlink_yaml_session, to=tmp_path)
    clowder_repo = tmp_path / ".clowder"
    assert not clowder_repo.exists()
    assert util.has_clowder_yaml_file(tmp_path)


@fixture(scope="session")
def cats_non_symlink_yaml_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(cats_non_symlink_yaml_session.__name__)
    return util.create_non_symlink_clowder_yaml(path, "cats")
