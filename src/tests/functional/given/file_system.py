"""New syntax test file"""

from pathlib import Path

# noinspection PyPackageRequirements
from pytest_bdd import given, parsers

import tests.functional.util as util


@given("I'm in an empty directory")
@given(parsers.parse("test directory is empty"))
def given_test_dir_empty(tmp_path: Path) -> None:
    assert util.is_directory_empty(tmp_path)


@given(parsers.parse("{version} clowder version is linked"))
def given_is_clowder_version_linked(tmp_path: Path, version: str) -> None:
    if "default" == version:
        assert util.has_valid_clowder_symlink_default(tmp_path)
    else:
        assert util.has_valid_clowder_symlink_version(tmp_path, version)


@given(parsers.parse("{version} clowder version exists"))
def given_clowder_version_present(tmp_path: Path, version: str) -> None:
    assert util.has_clowder_version(tmp_path, version)


@given(parsers.parse("{version} clowder version doesn't exist"))
def given_clowder_version_not_present(tmp_path: Path, version: str) -> None:
    assert not util.has_clowder_version(tmp_path, version)


@given(parsers.parse("{file_name} file doesn't exist"))
def given_has_no_file(tmp_path: Path, file_name: str) -> None:
    path = tmp_path / file_name
    assert not path.is_symlink()
    assert not path.exists()


@given(parsers.parse("{file_name} file exists"))
def given_has_file(tmp_path: Path, file_name: str) -> None:
    path = tmp_path / file_name
    assert path.exists()
    assert path.is_file()
    assert not path.is_symlink()


@given(parsers.parse("{file_name} is not a symlink"))
def given_is_not_symlink(tmp_path: Path, file_name: str) -> None:
    path = tmp_path / file_name
    assert not path.is_symlink()


@given(parsers.parse("{file_name} symlink doesn't exist"))
def given_has_no_symlink(tmp_path: Path, file_name: str) -> None:
    path = tmp_path / file_name
    assert not path.is_symlink()
    assert not path.exists()


@given(parsers.parse("{file_name} is a symlink"))
@given(parsers.parse("{file_name} symlink exists"))
def given_has_symlink(tmp_path: Path, file_name: str) -> None:
    path = tmp_path / file_name
    assert path.is_symlink()


@given(parsers.parse("{file_name_1} and {file_name_2} symlinks exist"))
def given_has_two_symlinks(tmp_path: Path, file_name_1: str, file_name_2: str) -> None:
    path = tmp_path / file_name_1
    assert path.is_symlink()
    path = tmp_path / file_name_2
    assert path.is_symlink()


@given(parsers.parse("{file_name_1} and {file_name_2} symlinks don't exist"))
@given(parsers.parse("{file_name_1} and {file_name_2} files don't exist"))
def given_two_files_do_not_exist(tmp_path: Path, file_name_1: str, file_name_2: str) -> None:
    path = tmp_path / file_name_1
    assert not path.exists()
    path = tmp_path / file_name_2
    assert not path.exists()


@given(parsers.parse("{directory} directory exists"))
@given("<directory> exists")
def given_has_directory(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert not path.exists()


@given(parsers.parse("{directory} directory doesn't exist"))
@given("<directory> doesn't exist")
def given_has_no_directory(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert not path.exists()


@given(parsers.parse("{file_name_1} and {file_name_2} files exist"))
def given_has_two_files(tmp_path: Path, file_name_1: str, file_name_2: str) -> None:
    path = tmp_path / file_name_1
    assert path.is_file()
    assert not path.is_symlink()
    path = tmp_path / file_name_2
    assert path.is_file()
    assert not path.is_symlink()


@given(parsers.parse("{file_name_1} and {file_name_2} are not symlinks"))
def given_two_files_not_symlinks(tmp_path: Path, file_name_1: str, file_name_2: str) -> None:
    path = tmp_path / file_name_1
    assert not path.is_symlink()
    path = tmp_path / file_name_2
    assert not path.is_symlink()


@given(parsers.parse("{file_name} is a symlink pointing to {destination}"))
def given_has_symlink_to(tmp_path: Path, file_name: str, destination: str) -> None:
    path = tmp_path / file_name
    destination = Path(destination)
    assert util.is_symlink_from_to(path, destination)
