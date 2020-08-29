"""New syntax test file"""

from pathlib import Path

# noinspection PyPackageRequirements
from pytest_bdd import scenarios, then, parsers

import tests.functional.util as util

scenarios('../../features')


@then("project at <directory> exists")
@then(parsers.parse("project at {directory} exists"))
def then_has_project_directory(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert path.exists()
    assert path.is_dir()


@then("project at <directory> doesn't exist")
@then(parsers.parse("project at {directory} doesn't exists"))
def then_has_no_project_directory(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert not path.exists()


@then(parsers.parse("clowder version {version} exists"))
def then_clowder_version_exists(tmp_path: Path, version: str) -> None:
    assert util.has_clowder_version(tmp_path, version)


@then("clowder versions directory exists")
def then_has_clowder_versions_directory(tmp_path: Path) -> None:
    path = tmp_path / ".clowder" / "versions"
    assert path.exists()
    assert path.is_dir()


@then(parsers.parse("file {file_name} doesn't exist"))
def then_has_no_file(tmp_path: Path, file_name: str) -> None:
    path = tmp_path / file_name
    assert not path.exists()


@then(parsers.parse("file {file_name} exists"))
def then_has_file(tmp_path: Path, file_name: str) -> None:
    path = tmp_path / file_name
    assert path.exists()
    assert not path.is_dir()


@then(parsers.parse("symlink {file_name} doesn't exist"))
def then_has_no_symlink(tmp_path: Path, file_name: str) -> None:
    path = tmp_path / file_name
    assert not path.exists()


@then(parsers.parse("symlink {file_name} exists"))
def then_has_symlink(tmp_path: Path, file_name: str) -> None:
    path = tmp_path / file_name
    assert path.exists()
    assert not path.is_dir()
    assert path.is_symlink()


@then(parsers.parse("{version} clowder version is linked"))
def then_yaml_version_linked(tmp_path: Path, version: str) -> None:
    if version == "default":
        assert util.has_valid_clowder_symlink_default(tmp_path)
    else:
        assert util.has_valid_clowder_symlink_version(tmp_path, version)
