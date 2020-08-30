"""New syntax test file"""

from pathlib import Path

# noinspection PyPackageRequirements
from pytest_bdd import scenarios, given, parsers

import tests.functional.util as util

scenarios('../../features')


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


@given("I'm in an empty directory")
def given_is_empty_directory(tmp_path: Path) -> None:
    print(f"tmp_path: {tmp_path}")
    assert util.is_directory_empty(tmp_path)


@given(parsers.parse("file {file_name} doesn't exist"))
def given_has_no_file(tmp_path: Path, file_name: str) -> None:
    path = tmp_path / file_name
    assert not path.exists()


@given(parsers.parse("file {file_name} exists"))
def given_has_file(tmp_path: Path, file_name: str) -> None:
    path = tmp_path / file_name
    assert path.exists()
    assert not path.is_dir()


@given(parsers.parse("symlink {file_name} doesn't exist"))
def given_has_no_symlink(tmp_path: Path, file_name: str) -> None:
    path = tmp_path / file_name
    assert not path.exists()


@given(parsers.parse("symlink {file_name} exists"))
def given_has_symlink(tmp_path: Path, file_name: str) -> None:
    path = tmp_path / file_name
    assert util.is_valid_symlink(path)


@given(parsers.parse("symlinks {file_name_1} and {file_name_2} exist"))
def given_has_two_symlinks(tmp_path: Path, file_name_1: str, file_name_2: str) -> None:
    path = tmp_path / file_name_1
    assert util.is_valid_symlink(path)
    path = tmp_path / file_name_2
    assert util.is_valid_symlink(path)


@given("<directory> doesn't exist")
def given_has_no_directory(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert not path.exists()


@given("clowder versions directory doesn't exist")
def given_has_no_clowder_versions_directory(tmp_path: Path) -> None:
    path = tmp_path / ".clowder" / "versions"
    assert not path.exists()


@given("project at <directory> is on branch <start_branch>")
def given_directory_on_start_branch(tmp_path: Path, directory: str, start_branch: str) -> None:
    path = tmp_path / directory
    assert util.is_on_active_branch(path, start_branch)


@given(parsers.parse("project at {directory} has local branch {test_branch}"))
@given("project at <directory> has local branch <test_branch>")
def given_directory_has_local_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    assert util.local_branch_exists(tmp_path / directory, test_branch)


@given(parsers.parse("project at {directory} has no local branch {test_branch}"))
@given("project at <directory> has no local branch <test_branch>")
def given_directory_has_no_local_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    assert not util.local_branch_exists(tmp_path / directory, test_branch)


@given(parsers.parse("project at {directory} has no remote branch {test_branch}"))
@given("project at <directory> has no remote branch <test_branch>")
def given_directory_has_no_remote_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    assert not util.remote_branch_exists(tmp_path / directory, test_branch)


@given(parsers.parse("project at {directory} has remote branch {test_branch}"))
@given("project at <directory> has remote branch <test_branch>")
def given_directory_has_remote_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    assert util.remote_branch_exists(tmp_path / directory, test_branch)


@given(parsers.parse("project at {directory} is on branch {branch}"))
@given("project at <directory> is on branch <branch>")
def given_directory_branch(tmp_path: Path, directory: str, branch: str) -> None:
    path = tmp_path / directory
    assert util.is_on_active_branch(path, branch)


@given("project at <directory> is on tag <tag>")
def given_directory_tag(tmp_path: Path, directory: str, tag: str) -> None:
    path = tmp_path / directory
    assert util.is_on_tag(path, tag)


@given(parsers.parse("project at {directory} is on commit {commit}"))
@given("project at <directory> is on commit <commit>")
def given_directory_commit(tmp_path: Path, directory: str, commit: str) -> None:
    path = tmp_path / directory
    assert util.is_on_commit(path, commit)


@given("project at <directory> has detached HEAD")
def given_directory_detached_head(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert util.is_detached_head(path)


@given(parsers.parse("project at {directory} is clean"))
@given("project at <directory> is clean")
def given_directory_clean(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert not util.is_dirty(path)


@given(parsers.parse("project at {directory} is dirty"))
@given("project at <directory> is dirty")
def given_directory_dirty(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert util.is_dirty(path)


@given("clowder repo is clean")
def given_clowder_repo_clean(tmp_path: Path) -> None:
    path = tmp_path / ".clowder"
    assert not util.is_dirty(path)


@given("clowder repo is dirty")
def given_clowder_repo_dirty(tmp_path: Path) -> None:
    path = tmp_path / ".clowder"
    assert util.is_dirty(path)
