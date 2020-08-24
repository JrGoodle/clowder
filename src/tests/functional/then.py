"""New syntax test file"""

from pathlib import Path

from git import Repo
# noinspection PyPackageRequirements
from pytest_bdd import scenarios, then, parsers

import tests.functional.util as util

scenarios('../features')


@then(parsers.parse("the command printed {branch_type} branches"))
def then_has_project_directory(tmp_path: Path, branch_type: str) -> None:
    # FIXME: Implement
    pass


@then("project at <directory> exists")
@then(parsers.parse("project at {directory} exists"))
def then_has_project_directory(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert path.exists()
    assert path.is_dir()


@then("project at <directory> is a git repository")
@then(parsers.parse("project at {directory} is a git repository"))
def then_is_git_repo(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert path.exists()
    assert path.is_dir()
    assert util.has_git_directory(path)


@then("project at <directory> is on <branch>")
def then_check_directory_branch(tmp_path: Path, directory: str, branch: str) -> None:
    path = tmp_path / directory
    assert util.is_on_active_branch(path, branch)


@then("project at <directory> is on <tag>")
def then_check_directory_tag(tmp_path: Path, directory: str, tag: str) -> None:
    path = tmp_path / directory
    assert util.is_detached_head_on_tag(path, tag)


@then("project at <directory> is on <commit>")
def then_check_directory_commit(tmp_path: Path, directory: str, commit: str) -> None:
    path = tmp_path / directory
    assert util.is_detached_head_on_commit(path, commit)


@then("project at <directory> is clean")
def then_check_directory_clean(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    print(f"TEST: Project at {directory} is clean")
    assert not util.is_dirty(path)


@then(parsers.parse("{directory} has untracked file {name}"))
def then_has_untracked_file(tmp_path: Path, directory: str, name: str) -> None:
    repo_path = tmp_path / directory
    path = tmp_path / directory / name
    repo = Repo(repo_path)
    assert f"{path.stem}{path.suffix}" in repo.untracked_files
