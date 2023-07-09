"""
This module contains fixtures
"""

from pathlib import Path

from pytest import fixture

import clowder.util.filesystem as fs

import tests.functional.util as util


@fixture
def cats_non_symlink_yml(tmp_path: Path, cats_non_symlink_yml_session: Path) -> None:
    fs.copy_directory(cats_non_symlink_yml_session, to_path=tmp_path)
    clowder_repo = tmp_path / ".clowder"
    assert not clowder_repo.exists()
    assert util.has_clowder_yaml_file(tmp_path)


@fixture(scope="session")
def cats_non_symlink_yml_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(cats_non_symlink_yml_session.__name__)
    return util.create_non_symlink_clowder_yml(path, "cats")


@fixture
def cats_non_symlink_yaml(tmp_path: Path, cats_non_symlink_yaml_session: Path) -> None:
    fs.copy_directory(cats_non_symlink_yaml_session, to_path=tmp_path)
    clowder_repo = tmp_path / ".clowder"
    clowder_yaml = tmp_path / "clowder.yaml"
    clowder_yml = tmp_path / "clowder.yml"

    assert not clowder_repo.exists()

    assert not clowder_yml.is_symlink()
    assert not clowder_yml.is_file()
    assert not clowder_yaml.is_symlink()
    assert clowder_yaml.exists()


@fixture(scope="session")
def cats_non_symlink_yaml_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(cats_non_symlink_yaml_session.__name__)
    util.create_non_symlink_clowder_yml(path, "cats")
    clowder_yaml = path / "clowder.yaml"
    clowder_yml = path / "clowder.yml"
    fs.copy_file(clowder_yml, clowder_yaml)
    clowder_yml.unlink()
    return path


@fixture
def cats_ambiguous_non_symlink_yaml_files(tmp_path: Path, cats_ambiguous_non_symlink_yaml_files_session: Path) -> None:
    fs.copy_directory(cats_ambiguous_non_symlink_yaml_files_session, to_path=tmp_path)
    clowder_yaml = tmp_path / "clowder.yaml"
    clowder_yml = tmp_path / "clowder.yml"
    clowder_repo = tmp_path / ".clowder"

    assert not clowder_repo.exists()

    assert clowder_yml.exists()
    assert not clowder_yml.is_symlink()

    assert clowder_yaml.exists()
    assert not clowder_yaml.is_symlink()


@fixture(scope="session")
def cats_ambiguous_non_symlink_yaml_files_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(cats_ambiguous_non_symlink_yaml_files_session.__name__)
    util.create_non_symlink_clowder_yml(path, "cats")
    clowder_yaml = path / "clowder.yaml"
    clowder_yml = path / "clowder.yml"
    fs.copy_file(clowder_yml, clowder_yaml)
    return path


@fixture
def cats_clowder_repo_symlink(tmp_path: Path, cats_clowder_repo_symlink_session: Path) -> None:
    fs.copy_directory(cats_clowder_repo_symlink_session, to_path=tmp_path)
    clowder_repo = tmp_path / ".clowder"
    clowder_yaml = tmp_path / "clowder.yaml"
    clowder_yml = tmp_path / "clowder.yml"
    target = Path("clowder-symlink-source-dir")
    assert (tmp_path / target).exists()
    fs.symlink_to(clowder_repo, target)
    assert clowder_repo.is_symlink()
    assert clowder_repo.exists()
    assert not clowder_yml.is_symlink()
    assert not clowder_yml.exists()
    assert not clowder_yaml.is_symlink()
    assert not clowder_yaml.exists()


@fixture(scope="session")
def cats_clowder_repo_symlink_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(cats_clowder_repo_symlink_session.__name__)
    util.init_clowder(path, "cats")
    clowder_yml = path / "clowder.yml"
    clowder_yml.unlink()
    clowder_repo = path / ".clowder"
    source = path / "clowder-symlink-source-dir"
    clowder_repo.rename(source)
    return path
