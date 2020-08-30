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


@then("project at <directory> is on branch <end_branch>")
def then_check_directory_end_branch(tmp_path: Path, directory: str, end_branch: str) -> None:
    path = tmp_path / directory
    assert util.is_on_active_branch(path, end_branch)


@then(parsers.parse("project at {directory} is on branch {branch}"))
@then("project at <directory> is on branch <branch>")
def then_directory_on_branch(tmp_path: Path, directory: str, branch: str) -> None:
    path = tmp_path / directory
    assert util.is_on_active_branch(path, branch)


@then("project at <directory> is on tag <tag>")
def then_directory_on_tag(tmp_path: Path, directory: str, tag: str) -> None:
    path = tmp_path / directory
    assert util.is_on_tag(path, tag)


@then("project at <directory> is on commit <commit>")
def then_directory_on_commit(tmp_path: Path, directory: str, commit: str) -> None:
    path = tmp_path / directory
    assert util.is_on_commit(path, commit)


@then(parsers.parse("project at {directory} is not on commit {commit}"))
@then("project at <directory> is not on commit <commit>")
def then_directory_not_on_commit(tmp_path: Path, directory: str, commit: str) -> None:
    path = tmp_path / directory
    assert not util.is_on_commit(path, commit)


@then("project at <directory> has detached HEAD")
def then_directory_detached_head(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert util.is_detached_head(path)


@then(parsers.parse("project at {directory} has no local branch {test_branch}"))
@then("project at <directory> has no local branch <test_branch>")
def then_directory_has_no_local_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    path = tmp_path / directory
    assert not util.local_branch_exists(path, test_branch)


@then(parsers.parse("project at {directory} has local branch {test_branch}"))
@then("project at <directory> has local branch <test_branch>")
def then_directory_has_local_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    path = tmp_path / directory
    assert util.local_branch_exists(path, test_branch)


@then(parsers.parse("project at {directory} has no remote branch {test_branch}"))
@then("project at <directory> has no remote branch <test_branch>")
def then_directory_has_no_remote_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    assert not util.remote_branch_exists(tmp_path / directory, test_branch)


@then(parsers.parse("project at {directory} has remote branch {test_branch}"))
@then("project at <directory> has remote branch <test_branch>")
def then_directory_has_remote_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    assert util.remote_branch_exists(tmp_path / directory, test_branch)


@then(parsers.parse("project at {directory} is clean"))
@then("project at <directory> is clean")
def then_directory_clean(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert not util.is_dirty(path)


@then(parsers.parse("project at {directory} is dirty"))
@then("project at <directory> is dirty")
def then_directory_dirty(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert util.is_dirty(path)


@then(parsers.parse("{directory} has untracked file {name}"))
def then_has_untracked_file(tmp_path: Path, directory: str, name: str) -> None:
    repo_path = tmp_path / directory
    path = repo_path / name
    # TODO: Move to utils
    repo = Repo(repo_path)
    assert f"{path.stem}{path.suffix}" in repo.untracked_files


@then(parsers.parse("project at {directory} has submodule at {submodule_path}"))
@then("project at <directory> has submodule at <submodule_path>")
def then_has_submodule(tmp_path: Path, directory: str, submodule_path: str) -> None:
    repo_path = tmp_path / directory
    assert util.has_submodule(repo_path, Path(submodule_path))


@then(parsers.parse("project at {directory} has no submodule at {submodule_path}"))
@then("project at <directory> has no submodule at <submodule_path>")
def then_has_no_submodule(tmp_path: Path, directory: str, submodule_path: str) -> None:
    repo_path = tmp_path / directory
    assert not util.has_submodule(repo_path, Path(submodule_path))


@then(parsers.parse("submodule in {directory} at {submodule_path} hasn't been initialized"))
@then("submodule in <directory> at <submodule_path> hasn't been initialized")
def then_submodule_not_initialized(tmp_path: Path,  directory: str, submodule_path: str) -> None:
    path = tmp_path / directory / submodule_path
    assert util.is_submodule_placeholder(path)
    assert not util.is_submodule_initialized(path)


@then(parsers.parse("submodule in {directory} at {submodule_path} has been initialized"))
@then("submodule in <directory> at <submodule_path> has been initialized")
def then_submodule_initialized(tmp_path: Path, directory: str, submodule_path: str) -> None:
    path = tmp_path / directory / submodule_path
    assert not util.is_submodule_placeholder(path)
    assert util.is_submodule_initialized(path)


@then("clowder repo is clean")
def then_clowder_repo_clean(tmp_path: Path) -> None:
    path = tmp_path / ".clowder"
    assert not util.is_dirty(path)


@then("clowder repo is dirty")
def then_clowder_repo_dirty(tmp_path: Path) -> None:
    path = tmp_path / ".clowder"
    assert util.is_dirty(path)


@then(parsers.parse("clowder repo has untracked file {name}"))
def then_clowder_repo_has_untracked_file(tmp_path: Path, name: str) -> None:
    repo_path = tmp_path / ".clowder"
    path = repo_path / name
    # TODO: Move to utils
    repo = Repo(repo_path)
    assert f"{path.stem}{path.suffix}" in repo.untracked_files


@then("project at <directory> is in sync with upstream <start_branch>")
def then_directory_in_sync_with_upstream(tmp_path: Path, directory: str, start_branch: str) -> None:
    path = tmp_path / directory
    assert util.number_of_commits_between_refs(path, "HEAD", f"origin/{start_branch}") == 0
    assert util.number_of_commits_between_refs(path, f"origin/{start_branch}", "HEAD") == 0


@then("project at <directory> has remote <remote> with url <url>")
def then_directory_in_sync_with_upstream(tmp_path: Path, directory: str, remote: str, url: str) -> None:
    path = tmp_path / directory
    assert util.has_git_remote_with_url(path, remote, url)
