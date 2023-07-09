"""New syntax test file"""

from pathlib import Path

from clowder.util.git import GitOffline, HEAD, Repo, Submodule
from pytest_bdd import then, parsers

from tests.functional.util import ScenarioInfo


@then("project at <directory> is a git repository")
@then(parsers.parse("project at {directory} is a git repository"))
@then(parsers.parse("directory at {directory} is a git repository"))
def then_project_dir_is_git_repo(tmp_path: Path, directory: str):
    repo = Repo(tmp_path / directory)
    assert repo.exists


@then("<test_directory> is a git repository")
def then_test_dir_is_git_repo(tmp_path: Path, test_directory: str) -> None:
    path = tmp_path / test_directory
    repo = Repo(path)
    assert repo.exists


@then("project at <directory> is not a git repository")
@then(parsers.parse("directory at {directory} is not a git repository"))
def then_project_dir_is_not_git_repo(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    repo = Repo(path)
    assert not repo.exists
    assert path.exists()
    assert path.is_dir()


@then("<test_directory> is not a git repository")
def then_test_dir_is_not_git_repo(tmp_path: Path, test_directory: str) -> None:
    path = tmp_path / test_directory
    repo = Repo(path)
    assert not repo.exists
    assert path.exists()
    assert path.is_dir()


@then("project at <directory> is on <end_branch>")
def then_check_directory_end_branch(tmp_path: Path, directory: str, end_branch: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.get_local_branch(end_branch).is_checked_out


@then("project at <directory> is on <test_branch>")
def then_check_directory_test_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.get_local_branch(test_branch).is_checked_out


@then("project at <directory> is on <start_branch>")
def then_check_directory_start_branch(tmp_path: Path, directory: str, start_branch: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.get_local_branch(start_branch).is_checked_out


@then(parsers.parse("repo at {directory} is on branch {branch}"))
@then(parsers.parse("project at {directory} is on branch {branch}"))
@then("project at <directory> is on <branch>")
def then_directory_on_branch(tmp_path: Path, directory: str, branch: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.get_local_branch(branch).is_checked_out


@then(parsers.parse("repo at {directory} is on tag {tag}"))
@then(parsers.parse("project at {directory} is on tag {tag}"))
@then("project at <directory> is on <tag>")
def then_directory_on_tag(tmp_path: Path, directory: str, tag: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.get_local_tag(tag).is_checked_out


@then(parsers.parse("repo at {directory} is on commit {commit}"))
@then(parsers.parse("project at {directory} is on commit {commit}"))
@then("project at <directory> is on <commit>")
def then_directory_on_commit(tmp_path: Path, directory: str, commit: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.sha() == commit


@then(parsers.parse("repo at {directory} is not on commit {commit}"))
@then(parsers.parse("project at {directory} is not on commit {commit}"))
@then("project at <directory> is not on <commit>")
def then_directory_not_on_commit(tmp_path: Path, directory: str, commit: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.sha() != commit


@then(parsers.parse("repo at {directory} has tracking branch {test_branch}"))
@then(parsers.parse("project at {directory} has tracking branch {test_branch}"))
@then("project at <directory> has tracking <test_branch>")
def then_directory_has_tracking_test_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.has_tracking_branch(test_branch)


@then("project at <directory> has tracking <branch>")
def then_directory_has_tracking_branch(tmp_path: Path, directory: str, branch: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.has_tracking_branch(branch)


@then(parsers.parse("repo at {directory} has no tracking branch {test_branch}"))
@then(parsers.parse("project at {directory} has no tracking branch {test_branch}"))
@then("project at <directory> has no tracking <test_branch>")
def then_directory_has_no_tracking_test_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    repo = Repo(tmp_path / directory)
    assert not repo.has_tracking_branch(test_branch)


@then("project at <directory> has no tracking branch <branch>")
def then_directory_has_no_tracking_branch(tmp_path: Path, directory: str, branch: str) -> None:
    repo = Repo(tmp_path / directory)
    assert not repo.has_tracking_branch(branch)


@then(parsers.parse("repo at {directory} has detached HEAD"))
@then(parsers.parse("project at {directory} has detached HEAD"))
@then("project at <directory> has detached HEAD")
def then_directory_detached_head(tmp_path: Path, directory: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.is_detached


@then(parsers.parse("repo at {directory} has no local branch {test_branch}"))
@then(parsers.parse("project at {directory} has no local branch {test_branch}"))
@then("project at <directory> has no local <test_branch>")
def then_directory_has_no_local_test_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    repo = Repo(tmp_path / directory)
    assert not repo.has_local_branch(test_branch)


@then("project at <directory> has no local <branch>")
def then_directory_has_no_local_branch(tmp_path: Path, directory: str, branch: str) -> None:
    repo = Repo(tmp_path / directory)
    assert not repo.has_local_branch(branch)


@then(parsers.parse("repo at {directory} has local branch {test_branch}"))
@then(parsers.parse("project at {directory} has local branch {test_branch}"))
@then("project at <directory> has local <test_branch>")
def then_directory_has_local_test_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.has_local_branch(test_branch)


@then("project at <directory> has local <branch>")
def then_directory_has_local_branch(tmp_path: Path, directory: str, branch: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.has_local_branch(branch)


@then(parsers.parse("repo at {directory} has no remote branch {test_branch}"))
@then(parsers.parse("project at {directory} has no remote branch {test_branch}"))
@then("project at <directory> has no remote <test_branch>")
def then_directory_has_no_remote_test_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    repo = Repo(tmp_path / directory)
    assert not repo.has_remote_branch(test_branch)


@then("project at <directory> has no remote <branch>")
def then_directory_has_no_remote_branch(tmp_path: Path, directory: str, branch: str) -> None:
    repo = Repo(tmp_path / directory)
    assert not repo.has_remote_branch(branch)


@then(parsers.parse("repo at {directory} has remote branch {test_branch}"))
@then(parsers.parse("project at {directory} has remote branch {test_branch}"))
@then("project at <directory> has remote <test_branch>")
def then_directory_has_remote_test_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.has_remote_branch(test_branch)


@then("project at <directory> has remote <branch>")
def then_directory_has_remote_branch(tmp_path: Path, directory: str, branch: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.has_remote_branch(branch)


@then(parsers.parse("repo at {directory} is clean"))
@then(parsers.parse("project at {directory} is clean"))
@then("project at <directory> is clean")
def then_directory_clean(tmp_path: Path, directory: str) -> None:
    repo = Repo(tmp_path / directory)
    assert not repo.is_dirty


@then(parsers.parse("repo at {directory} is dirty"))
@then(parsers.parse("project at {directory} is dirty"))
@then("project at <directory> is dirty")
def then_directory_dirty(tmp_path: Path, directory: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.is_dirty


@then(parsers.parse("repo at {directory} has untracked file {filename}"))
@then(parsers.parse("project at {directory} has untracked file {filename}"))
@then("project at <directory> has untracked file <filename>")
def then_has_untracked_file(tmp_path: Path, directory: str, filename: str) -> None:
    repo = Repo(tmp_path / directory)
    assert Path(filename) in repo.untracked_files


@then(parsers.parse("repo at {directory} has untracked files"))
@then(parsers.parse("project at {directory} has untracked files"))
@then("project at <directory> has untracked files")
def then_directory_has_untracked_files(tmp_path: Path, directory: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.has_untracked_files


@then(parsers.parse("repo at {directory} has no untracked files"))
@then(parsers.parse("project at {directory} has no untracked files"))
@then("project at <directory> has no untracked files")
def then_directory_has_no_untracked_files(tmp_path: Path, directory: str) -> None:
    repo = Repo(tmp_path / directory)
    assert not repo.has_untracked_files


@then(parsers.parse("repo at {directory} has submodule at {submodule_path}"))
@then(parsers.parse("project at {directory} has submodule at {submodule_path}"))
@then("project at <directory> has submodule at <submodule_path>")
def then_has_submodule(tmp_path: Path, directory: str, submodule_path: str) -> None:
    repo_path = tmp_path / directory
    repo = Repo(repo_path)
    assert repo.has_submodule(Path(submodule_path))


@then(parsers.parse("repo at {directory} has no submodule at {submodule_path}"))
@then(parsers.parse("project at {directory} has no submodule at {submodule_path}"))
@then("project at <directory> has no submodule at <submodule_path>")
def then_has_no_submodule(tmp_path: Path, directory: str, submodule_path: str) -> None:
    repo_path = tmp_path / directory
    repo = Repo(repo_path)
    assert not repo.has_submodule(Path(submodule_path))


# TODO: Add @given versions of these and update tests with checks before @when
@then(parsers.parse("submodule in {directory} at {submodule_path} is not initialized"))
@then("submodule in <directory> at <submodule_path> is not initialized")
def then_submodule_not_initialized(tmp_path: Path,  directory: str, submodule_path: str) -> None:
    repo_path = tmp_path / directory
    repo = Repo(repo_path)
    submodule = Submodule(repo_path, Path(submodule_path))
    assert repo.has_submodule(Path(submodule_path))
    assert GitOffline.is_submodule_placeholder(repo_path / submodule_path)
    assert not submodule.is_initialized


@then(parsers.parse("submodule in {directory} at {submodule_path} is initialized"))
@then("submodule in <directory> at <submodule_path> is initialized")
def then_submodule_initialized(tmp_path: Path, directory: str, submodule_path: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.get_submodule(Path(submodule_path)).is_initialized


@then(parsers.parse("repo at {directory} is in sync with upstream branch {start_branch}"))
@then(parsers.parse("project at {directory} is in sync with upstream branch {start_branch}"))
@then("project at <directory> is in sync with upstream <start_branch>")
def then_directory_in_sync_with_upstream_start_branch(tmp_path: Path, directory: str, start_branch: str) -> None:
    path = tmp_path / directory
    assert GitOffline.has_no_commits_between_refs(path, HEAD, f"origin/{start_branch}")


@then("project at <directory> is in sync with upstream <test_branch>")
def then_directory_in_sync_with_upstream_test_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    path = tmp_path / directory
    assert GitOffline.has_no_commits_between_refs(path, HEAD, f"origin/{test_branch}")


@then(parsers.parse("repo at {directory} has remote {remote} with url {url}"))
@then(parsers.parse("project at {directory} has remote {remote} with url {url}"))
@then("project at <directory> has <remote> with <url>")
def then_directory_has_remote_with_url(tmp_path: Path, directory: str, remote: str, url: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.has_remote(remote=remote, fetch_url=url, push_url=url)


@then(parsers.parse("repo at {directory} has rebase in progress"))
@then(parsers.parse("project at {directory} has rebase in progress"))
@then("project at <directory> has rebase in progress")
def then_directory_has_rebase_in_progress(tmp_path: Path, directory: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.is_rebase_in_progress


@then(parsers.parse("repo at {directory} has no rebase in progress"))
@then(parsers.parse("project at {directory} has no rebase in progress"))
@then("project at <directory> has no rebase in progress")
def then_directory_has_no_rebase_in_progress(tmp_path: Path, directory: str) -> None:
    repo = Repo(tmp_path / directory)
    assert not repo.is_rebase_in_progress


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

    messages = GitOffline.get_commit_messages_behind(path, f"refs/heads/{branch}", number_behind + number_ahead)
    current_message = 0
    for message in messages:
        if current_message < number_ahead:
            assert commit_messages_ahead[current_message] == message
        else:
            assert commit_messages_behind[current_message - number_ahead] == message
        current_message += 1


@then("project at <directory> has staged <filename>")
def then_has_stage_file(tmp_path: Path, directory: str, filename: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.is_dirty
#     TODO: Add check for specific staged file


@then(parsers.parse("project at {directory} has lfs installed"))
@then("project at <directory> has lfs installed")
def then_has_lfs_installed(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert GitOffline.lfs_hooks_installed(path)
    assert GitOffline.lfs_filters_installed(path)


@then(parsers.parse("{filename} file in directory {directory} is an lfs pointer"))
@then("<filename> in <directory> is an lfs pointer")
def then_file_is_lfs_pointer(tmp_path: Path, filename: str, directory: str) -> None:
    path = tmp_path / directory
    assert GitOffline.is_lfs_file_pointer(path, filename)


@then(parsers.parse("{filename} file in directory {directory} is not an lfs pointer"))
@then("<filename> in <directory> is not an lfs pointer")
def then_file_is_not_lfs_pointer(tmp_path: Path, filename: str, directory: str) -> None:
    path = tmp_path / directory
    assert GitOffline.is_lfs_file_not_pointer(path, filename)


@then(parsers.parse("project at {directory} doesn't have lfs installed"))
@then("project at <directory> doesn't have lfs installed")
def then_has_no_lfs_installed(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert not GitOffline.lfs_hooks_installed(path)
    assert not GitOffline.lfs_filters_installed(path)


@then(parsers.parse("project at {directory} is a shallow clone"))
@then("project at <directory> is a shallow clone")
def then_is_shallow_clone(tmp_path: Path, directory: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.is_shallow


@then(parsers.parse("project at {directory} is not a shallow clone"))
@then("project at <directory> is not a shallow clone")
def then_is_not_shallow_clone(tmp_path: Path, directory: str) -> None:
    repo = Repo(tmp_path / directory)
    assert not repo.is_shallow
