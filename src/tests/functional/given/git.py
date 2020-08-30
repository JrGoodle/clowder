"""New syntax test file"""

from pathlib import Path

# noinspection PyPackageRequirements
from pytest_bdd import scenarios, given, parsers

import tests.functional.util as util

scenarios('../../features')


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
