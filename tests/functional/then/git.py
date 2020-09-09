"""New syntax test file"""

from pathlib import Path

from pytest_bdd import then, parsers

import tests.functional.util as util
from tests.functional.util import ScenarioInfo


@then("project at <directory> is a git repository")
@then(parsers.parse("directory at {directory} is a git repository"))
def then_project_dir_is_git_repo(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert path.exists()
    assert path.is_dir()
    assert util.has_git_directory(path)


@then("<test_directory> is a git repository")
def then_test_dir_is_git_repo(tmp_path: Path, test_directory: str) -> None:
    path = tmp_path / test_directory
    assert path.exists()
    assert path.is_dir()
    assert util.has_git_directory(path)


@then("project at <directory> is not a git repository")
@then(parsers.parse("directory at {directory} is not a git repository"))
def then_project_dir_is_not_git_repo(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert path.exists()
    assert path.is_dir()
    assert not util.has_git_directory(path)


@then("<test_directory> is not a git repository")
def then_test_dir_is_not_git_repo(tmp_path: Path, test_directory: str) -> None:
    path = tmp_path / test_directory
    assert path.exists()
    assert path.is_dir()
    assert not util.has_git_directory(path)


@then("project at <directory> is on <end_branch>")
def then_check_directory_end_branch(tmp_path: Path, directory: str, end_branch: str) -> None:
    path = tmp_path / directory
    assert util.is_on_active_branch(path, end_branch)


@then("project at <directory> is on <test_branch>")
def then_check_directory_test_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    path = tmp_path / directory
    assert util.is_on_active_branch(path, test_branch)


@then("project at <directory> is on <start_branch>")
def then_check_directory_start_branch(tmp_path: Path, directory: str, start_branch: str) -> None:
    path = tmp_path / directory
    assert util.is_on_active_branch(path, start_branch)


@then(parsers.parse("repo at {directory} is on branch {branch}"))
@then(parsers.parse("project at {directory} is on branch {branch}"))
@then("project at <directory> is on <branch>")
def then_directory_on_branch(tmp_path: Path, directory: str, branch: str) -> None:
    path = tmp_path / directory
    assert util.is_on_active_branch(path, branch)


@then(parsers.parse("repo at {directory} is on tag {tag}"))
@then(parsers.parse("project at {directory} is on tag {tag}"))
@then("project at <directory> is on <tag>")
def then_directory_on_tag(tmp_path: Path, directory: str, tag: str) -> None:
    path = tmp_path / directory
    assert util.is_on_tag(path, tag)


@then(parsers.parse("repo at {directory} is on commit {commit}"))
@then(parsers.parse("project at {directory} is on commit {commit}"))
@then("project at <directory> is on <commit>")
def then_directory_on_commit(tmp_path: Path, directory: str, commit: str) -> None:
    path = tmp_path / directory
    assert util.is_on_commit(path, commit)


@then(parsers.parse("repo at {directory} is not on commit {commit}"))
@then(parsers.parse("project at {directory} is not on commit {commit}"))
@then("project at <directory> is not on <commit>")
def then_directory_not_on_commit(tmp_path: Path, directory: str, commit: str) -> None:
    path = tmp_path / directory
    assert not util.is_on_commit(path, commit)


@then(parsers.parse("repo at {directory} has tracking branch {test_branch}"))
@then(parsers.parse("project at {directory} has tracking branch {test_branch}"))
@then("project at <directory> has tracking <test_branch>")
def then_directory_has_tracking_test_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    path = tmp_path / directory
    assert util.tracking_branch_exists(path, test_branch)


@then("project at <directory> has tracking <branch>")
def then_directory_has_tracking_branch(tmp_path: Path, directory: str, branch: str) -> None:
    path = tmp_path / directory
    assert util.tracking_branch_exists(path, branch)


@then(parsers.parse("repo at {directory} has no tracking branch {test_branch}"))
@then(parsers.parse("project at {directory} has no tracking branch {test_branch}"))
@then("project at <directory> has no tracking <test_branch>")
def then_directory_has_no_tracking_test_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    path = tmp_path / directory
    assert not util.tracking_branch_exists(path, test_branch)


@then("project at <directory> has no tracking branch <branch>")
def then_directory_has_no_tracking_branch(tmp_path: Path, directory: str, branch: str) -> None:
    path = tmp_path / directory
    assert not util.tracking_branch_exists(path, branch)


@then(parsers.parse("repo at {directory} has detached HEAD"))
@then(parsers.parse("project at {directory} has detached HEAD"))
@then("project at <directory> has detached HEAD")
def then_directory_detached_head(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert util.is_detached_head(path)


@then(parsers.parse("repo at {directory} has no local branch {test_branch}"))
@then(parsers.parse("project at {directory} has no local branch {test_branch}"))
@then("project at <directory> has no local <test_branch>")
def then_directory_has_no_local_test_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    path = tmp_path / directory
    assert not util.local_branch_exists(path, test_branch)


@then("project at <directory> has no local <branch>")
def then_directory_has_no_local_branch(tmp_path: Path, directory: str, branch: str) -> None:
    path = tmp_path / directory
    assert not util.local_branch_exists(path, branch)


@then(parsers.parse("repo at {directory} has local branch {test_branch}"))
@then(parsers.parse("project at {directory} has local branch {test_branch}"))
@then("project at <directory> has local <test_branch>")
def then_directory_has_local_test_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    path = tmp_path / directory
    assert util.local_branch_exists(path, test_branch)


@then("project at <directory> has local <branch>")
def then_directory_has_local_branch(tmp_path: Path, directory: str, branch: str) -> None:
    path = tmp_path / directory
    assert util.local_branch_exists(path, branch)


@then(parsers.parse("repo at {directory} has no remote branch {test_branch}"))
@then(parsers.parse("project at {directory} has no remote branch {test_branch}"))
@then("project at <directory> has no remote <test_branch>")
def then_directory_has_no_remote_test_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    assert not util.remote_branch_exists(tmp_path / directory, test_branch)


@then("project at <directory> has no remote <branch>")
def then_directory_has_no_remote_branch(tmp_path: Path, directory: str, branch: str) -> None:
    assert not util.remote_branch_exists(tmp_path / directory, branch)


@then(parsers.parse("repo at {directory} has remote branch {test_branch}"))
@then(parsers.parse("project at {directory} has remote branch {test_branch}"))
@then("project at <directory> has remote <test_branch>")
def then_directory_has_remote_test_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    assert util.remote_branch_exists(tmp_path / directory, test_branch)


@then("project at <directory> has remote <branch>")
def then_directory_has_remote_branch(tmp_path: Path, directory: str, branch: str) -> None:
    assert util.remote_branch_exists(tmp_path / directory, branch)


@then(parsers.parse("repo at {directory} is clean"))
@then(parsers.parse("project at {directory} is clean"))
@then("project at <directory> is clean")
def then_directory_clean(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert not util.is_dirty(path)


@then(parsers.parse("repo at {directory} is dirty"))
@then(parsers.parse("project at {directory} is dirty"))
@then("project at <directory> is dirty")
def then_directory_dirty(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert util.is_dirty(path)


@then(parsers.parse("repo at {directory} has untracked file {filename}"))
@then(parsers.parse("project at {directory} has untracked file {filename}"))
@then("project at <directory> has untracked file <filename>")
def then_has_untracked_file(tmp_path: Path, directory: str, filename: str) -> None:
    path = tmp_path / directory
    assert util.has_untracked_file(path, filename)


@then(parsers.parse("repo at {directory} has submodule at {submodule_path}"))
@then(parsers.parse("project at {directory} has submodule at {submodule_path}"))
@then("project at <directory> has submodule at <submodule_path>")
def then_has_submodule(tmp_path: Path, directory: str, submodule_path: str) -> None:
    repo_path = tmp_path / directory
    assert util.has_submodule(repo_path, Path(submodule_path))


@then(parsers.parse("repo at {directory} has no submodule at {submodule_path}"))
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


@then(parsers.parse("repo at {directory} is in sync with upstream branch {start_branch}"))
@then(parsers.parse("project at {directory} is in sync with upstream branch {start_branch}"))
@then("project at <directory> is in sync with upstream <start_branch>")
def then_directory_in_sync_with_upstream_start_branch(tmp_path: Path, directory: str, start_branch: str) -> None:
    path = tmp_path / directory
    assert util.has_no_commits_between_refs(path, "HEAD", f"origin/{start_branch}")


@then("project at <directory> is in sync with upstream <test_branch>")
def then_directory_in_sync_with_upstream_test_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    path = tmp_path / directory
    assert util.has_no_commits_between_refs(path, "HEAD", f"origin/{test_branch}")


@then(parsers.parse("repo at {directory} has remote {remote} with url {url}"))
@then(parsers.parse("project at {directory} has remote {remote} with url {url}"))
@then("project at <directory> has <remote> with <url>")
def then_directory_in_sync_with_upstream(tmp_path: Path, directory: str, remote: str, url: str) -> None:
    path = tmp_path / directory
    assert util.has_git_remote_with_url(path, remote, url)


@then(parsers.parse("repo at {directory} has rebase in progress"))
@then(parsers.parse("project at {directory} has rebase in progress"))
@then("project at <directory> has rebase in progress")
def then_directory_has_rebase_in_progress(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert util.is_rebase_in_progress(path)


@then(parsers.parse("repo at {directory} has no rebase in progress"))
@then(parsers.parse("project at {directory} has no rebase in progress"))
@then("project at <directory> has no rebase in progress")
def then_directory_has_no_rebase_in_progress(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert not util.is_rebase_in_progress(path)


@then("project at <directory> has rebased commits in <branch> in the correct order")
def then_check_directory_rebased_commit_messages_correct_order(tmp_path: Path, directory: str, branch: str,
                                                               scenario_info: ScenarioInfo) -> None:
    path = tmp_path / directory
    number_behind = scenario_info.number_commit_messages_behind
    number_ahead = scenario_info.number_commit_messages_ahead
    assert number_behind is not None
    assert number_ahead is not None
    commit_messages_behind = scenario_info.commit_messages_behind
    commit_messages_ahead = scenario_info.commit_messages_ahead
    assert commit_messages_behind is not None
    assert commit_messages_ahead is not None

    messages = util.get_commit_messages_behind(path, f"refs/heads/{branch}", number_behind + number_ahead)
    current_message = 0
    for message in messages:
        if current_message < number_ahead:
            assert commit_messages_ahead[current_message] == message
        else:
            assert commit_messages_behind[current_message - number_ahead] == message
        current_message += 1


@then("project at <directory> has staged <filename>")
def then_has_stage_file(tmp_path: Path, directory: str, filename: str) -> None:
    path = tmp_path / directory
    assert util.is_dirty(path)
#     TODO: Add check for specific staged file


@then("project at <directory> has lfs installed")
def then_has_lfs_installed(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert util.lfs_hooks_installed(path)
    assert util.lfs_filters_installed(path)


@then("<filename> in <directory> is an lfs pointer")
def then_file_is_lfs_pointer(tmp_path: Path, filename: str, directory: str) -> None:
    path = tmp_path / directory
    assert util.is_lfs_file_pointer(path, filename)


@then("<filename> in <directory> is not an lfs pointer")
def then_file_is_not_lfs_pointer(tmp_path: Path, filename: str, directory: str) -> None:
    path = tmp_path / directory
    assert util.is_lfs_file_not_pointer(path, filename)
