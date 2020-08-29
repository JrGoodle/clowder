"""New syntax test file"""

from pathlib import Path

from git import Repo
# noinspection PyPackageRequirements
from pytest_bdd import scenarios, then, parsers

import tests.functional.util as util
from .util import CommandResults

scenarios('../features')


@then("the command succeeds")
def then_command_succeeded(command_results: CommandResults) -> None:
    assert len(command_results.completed_processes) == 1
    assert all([result.returncode == 0 for result in command_results.completed_processes])


@then("the commands succeed")
def then_commands_succeeded(command_results: CommandResults) -> None:
    assert len(command_results.completed_processes) > 1
    assert all([result.returncode == 0 for result in command_results.completed_processes])


@then("the command fails")
def then_command_failed(command_results: CommandResults) -> None:
    assert len(command_results.completed_processes) == 1
    assert all([result.returncode != 0 for result in command_results.completed_processes])


@then("the commands fail")
def then_commands_failed(command_results: CommandResults) -> None:
    assert len(command_results.completed_processes) > 1
    assert all([result.returncode != 0 for result in command_results.completed_processes])


@then(parsers.parse("the command exited with return code {code:d}"))
def then_command_exit_return_code(command_results: CommandResults, code: int) -> None:
    assert len(command_results.completed_processes) == 1
    assert all([result.returncode == code for result in command_results.completed_processes])


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


@then(parsers.parse("clowder version {version} exists"))
def then_clowder_version_exists(tmp_path: Path, version: str) -> None:
    assert util.has_clowder_version(tmp_path, version)


@then("clowder versions directory exists")
def then_has_clowder_versions_directory(tmp_path: Path) -> None:
    path = tmp_path / ".clowder" / "versions"
    assert path.exists()
    assert path.is_dir()


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


@then(parsers.parse("{directory} has untracked file {name}"))
def then_has_untracked_file(tmp_path: Path, directory: str, name: str) -> None:
    repo_path = tmp_path / directory
    path = tmp_path / directory / name
    repo = Repo(repo_path)
    assert f"{path.stem}{path.suffix}" in repo.untracked_files


@then(parsers.parse("{version} clowder version is linked"))
def then_link_yaml_version(tmp_path: Path, version: str) -> None:
    if version == "default":
        assert util.has_valid_clowder_symlink_default(tmp_path)
    else:
        assert util.has_valid_clowder_symlink_version(tmp_path, version)


@then("project at <directory> is in sync with upstream <start_branch>")
def then_directory_in_sync_with_upstream(tmp_path: Path, directory: str, start_branch: str) -> None:
    path = tmp_path / directory
    assert util.number_of_commits_between_refs(path, "HEAD", f"origin/{start_branch}") == 0
    assert util.number_of_commits_between_refs(path, f"origin/{start_branch}", "HEAD") == 0
