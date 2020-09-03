"""New syntax test file"""

from pathlib import Path

from pytest_bdd import then, parsers

import tests.functional.util as util


@then(parsers.parse("test directory is empty"))
def then_test_dir_empty(tmp_path: Path) -> None:
    assert util.is_directory_empty(tmp_path)


@then(parsers.parse("{directory} directory exists"))
@then("<directory> exists")
@then(parsers.parse("project at {directory} exists"))
@then("project at <directory> exists")
def then_has_directory(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert path.exists()
    assert path.is_dir()


@then(parsers.parse("{directory} directory doesn't exist"))
@then("<directory> doesn't exist")
@then(parsers.parse("project at {directory} doesn't exists"))
@then("project at <directory> doesn't exist")
def then_has_no_directory(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert not path.exists()


@then(parsers.parse("{file_name} file doesn't exist"))
def then_has_no_file(tmp_path: Path, file_name: str) -> None:
    path = tmp_path / file_name
    assert not path.exists()


@then(parsers.parse("{file_name} is not a directory"))
@then(parsers.parse("{file_name} file exists"))
def then_has_file(tmp_path: Path, file_name: str) -> None:
    path = tmp_path / file_name
    assert path.exists()
    assert not path.is_dir()


@then(parsers.parse("{file_name} file exists in directory {directory}"))
def then_has_file_in_directory(tmp_path: Path, file_name: str, directory: str) -> None:
    path = tmp_path / directory / file_name
    assert path.exists()
    assert not path.is_dir()


@then(parsers.parse("{file_name} file doesn't exist in directory {directory}"))
def then_has_no_file_in_directory(tmp_path: Path, file_name: str, directory: str) -> None:
    path = tmp_path / directory / file_name
    assert not path.exists()


@then(parsers.parse("{file_name} is not a symlink"))
def then_file_not_symlink(tmp_path: Path, file_name: str) -> None:
    path = tmp_path / file_name
    assert not path.is_symlink()


@then(parsers.parse("{file_name} symlink doesn't exist"))
def then_has_no_symlink(tmp_path: Path, file_name: str) -> None:
    path = tmp_path / file_name
    assert not path.exists()


@then(parsers.parse("{file_name} is a symlink"))
@then(parsers.parse("{file_name} symlink exists"))
def then_has_symlink(tmp_path: Path, file_name: str) -> None:
    path = tmp_path / file_name
    assert path.exists()
    assert path.is_symlink()


@then(parsers.parse("{file_name} is a symlink pointing to {destination}"))
def then_is_symlink_pointing_to(tmp_path: Path, file_name: str, destination: str) -> None:
    path = tmp_path / file_name
    destination = tmp_path / destination
    assert util.is_symlink_from_to(path, destination)


@then(parsers.parse("{file_name_1} and {file_name_2} files exist"))
def then_has_two_files(tmp_path: Path, file_name_1: str, file_name_2: str) -> None:
    path = tmp_path / file_name_1
    assert path.is_file()
    assert not path.is_symlink()
    path = tmp_path / file_name_2
    assert path.is_file()
    assert not path.is_symlink()


@then(parsers.parse("{file_name_1} and {file_name_2} symlinks don't exist"))
@then(parsers.parse("{file_name_1} and {file_name_2} files don't exist"))
def then_two_files_do_not_exist(tmp_path: Path, file_name_1: str, file_name_2: str) -> None:
    path = tmp_path / file_name_1
    assert not path.exists()
    path = tmp_path / file_name_2
    assert not path.exists()


@then(parsers.parse("{file_name_1} and {file_name_2} are not symlinks"))
def then_two_files_not_symlinks(tmp_path: Path, file_name_1: str, file_name_2: str) -> None:
    path = tmp_path / file_name_1
    assert not path.is_symlink()
    path = tmp_path / file_name_2
    assert not path.is_symlink()


@then(parsers.parse("{version} clowder version exists"))
def then_clowder_version_exists(tmp_path: Path, version: str) -> None:
    assert util.has_clowder_version(tmp_path, version)


@then(parsers.parse("{version} clowder version is linked"))
def then_yaml_version_linked(tmp_path: Path, version: str) -> None:
    if version == "default":
        assert util.has_valid_clowder_symlink_default(tmp_path)
    else:
        assert util.has_valid_clowder_symlink_version(tmp_path, version)
