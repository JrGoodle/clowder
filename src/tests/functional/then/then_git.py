"""New syntax test file"""

from pathlib import Path

from git import Repo
# noinspection PyPackageRequirements
from pytest_bdd import scenarios, then, parsers

import tests.functional.util as util

scenarios('../../features')


@then("project at <directory> is a git repository")
@then(parsers.parse("project at {directory} is a git repository"))
def then_is_git_repo(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert path.exists()
    assert path.is_dir()
    assert util.has_git_directory(path)


@then("project at <directory> is on <end_branch>")
def then_check_directory_end_branch(tmp_path: Path, directory: str, end_branch: str) -> None:
    path = tmp_path / directory
    assert util.is_on_active_branch(path, end_branch)


@then("project at <directory> is on <branch>")
def then_directory_on_branch(tmp_path: Path, directory: str, branch: str) -> None:
    path = tmp_path / directory
    assert util.is_on_active_branch(path, branch)


@then("project at <directory> is on <tag>")
def then_directory_on_tag(tmp_path: Path, directory: str, tag: str) -> None:
    path = tmp_path / directory
    assert util.is_detached_head_on_tag(path, tag)


@then("project at <directory> is on <commit>")
def then_directory_on_commit(tmp_path: Path, directory: str, commit: str) -> None:
    path = tmp_path / directory
    assert util.is_detached_head_on_commit(path, commit)


@then("project at <directory> has no local branch <test_branch>")
def then_directory_has_no_local_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    path = tmp_path / directory
    assert not util.local_branch_exists(path, test_branch)


@then("project at <directory> has local branch <test_branch>")
def then_directory_has_local_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    path = tmp_path / directory
    assert util.local_branch_exists(path, test_branch)


@then("project at <directory> has no remote branch <test_branch>")
def then_directory_has_no_remote_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    assert not util.remote_branch_exists(tmp_path / directory, test_branch)


@then("project at <directory> has remote branch <test_branch>")
def then_directory_has_remote_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    assert util.remote_branch_exists(tmp_path / directory, test_branch)


@then("project at <directory> is clean")
def then_directory_clean(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert not util.is_dirty(path)


@then("project at <directory> is dirty")
def then_directory_dirty(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert util.is_dirty(path)


@then(parsers.parse("{directory} has untracked file {name}"))
def then_has_untracked_file(tmp_path: Path, directory: str, name: str) -> None:
    repo_path = tmp_path / directory
    path = tmp_path / directory / name
    repo = Repo(repo_path)
    assert f"{path.stem}{path.suffix}" in repo.untracked_files


@then("project at <directory> is in sync with upstream <start_branch>")
def then_directory_in_sync_with_upstream(tmp_path: Path, directory: str, start_branch: str) -> None:
    path = tmp_path / directory
    assert util.number_of_commits_between_refs(path, "HEAD", f"origin/{start_branch}") == 0
    assert util.number_of_commits_between_refs(path, f"origin/{start_branch}", "HEAD") == 0
