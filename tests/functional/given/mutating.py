"""New syntax test file"""

import os
import shutil
from pathlib import Path

from pytest_bdd import given, parsers

import tests.functional.util as util
from tests.functional.util import ScenarioInfo


@given(parsers.parse("{example} example was initialized to branch {branch}"))
def given_example_init_branch(tmp_path: Path, example: str, branch: str) -> None:
    url = util.get_url(example)
    result = util.run_command(f"clowder init {url} -b {branch}", tmp_path)
    assert result.returncode == 0


@given(parsers.parse("{example} example was initialized and herded to branch {branch}"))
def given_example_init_herd_branch(tmp_path: Path, example: str, branch: str) -> None:
    url = util.get_url(example)
    result = util.run_command(f"clowder init {url} -b {branch}", tmp_path)
    assert result.returncode == 0
    result = util.run_command(f"clowder herd", tmp_path)
    assert result.returncode == 0


@given(parsers.parse("'{command}' was run"))
def given_run_clowder_command(tmp_path: Path, command: str) -> None:
    result = util.run_command(command, tmp_path)
    assert result.returncode == 0


@given(parsers.parse("linked {version} clowder version"))
def given_did_link_clowder_version(tmp_path: Path, version: str) -> None:
    if "default" == version:
        result = util.run_command("clowder link", tmp_path, check=True)
        assert result.returncode == 0
        assert util.has_valid_clowder_symlink_default(tmp_path)
    else:
        result = util.run_command(f"clowder link {version}", tmp_path)
        assert result.returncode == 0
        assert util.has_valid_clowder_symlink_version(tmp_path, version)


@given(parsers.parse("created {name} symlink pointing to {target}"))
def given_created_symlink(tmp_path: Path, name: str, target: str) -> None:
    name_path = tmp_path / name
    target_path = tmp_path / target
    assert target_path.exists()
    resolved = target_path.resolve()
    util.link_to(name_path, resolved)


@given(parsers.parse("created {name_1} and {name_2} symlinks pointing to {target}"))
def given_created_symlinks(tmp_path: Path, name_1: str, name_2: str, target: str) -> None:
    target_path = tmp_path / target
    name_path = tmp_path / name_1
    util.link_to(name_path, target_path)
    name_path = tmp_path / name_2
    util.link_to(name_path, target_path)


@given(parsers.parse("repo at {directory} staged file {filename}"))
@given(parsers.parse("project at {directory} staged file {filename}"))
@given("project at <directory> staged <filename>")
def given_did_stage_file(tmp_path: Path, directory: str, filename: str) -> None:
    path = tmp_path / directory
    util.git_add_file(path, filename)


@given(parsers.parse("repo at {directory} created local branch {test_branch}"))
@given(parsers.parse("project at {directory} created local branch {test_branch}"))
@given("project at <directory> created local branch <test_branch>")
def given_directory_created_local_test_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    path = tmp_path / directory
    util.create_local_branch(path, test_branch)
    assert util.local_branch_exists(tmp_path / directory, test_branch)


@given("project at <directory> created local <branch>")
def given_directory_created_local_branch(tmp_path: Path, directory: str, branch: str) -> None:
    path = tmp_path / directory
    util.create_local_branch(path, branch)
    assert util.local_branch_exists(tmp_path / directory, branch)


@given("project at <directory> checked out <test_branch>")
def given_directory_checked_out_start_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    path = tmp_path / directory
    util.checkout_branch(path, test_branch)
    assert util.is_on_active_branch(path, test_branch)


@given("project at <directory> checked out detached HEAD behind <test_branch>")
def given_directory_checked_out_detached_head_behind_test_branch(tmp_path: Path, directory: str,
                                                                 test_branch: str) -> None:
    path = tmp_path / directory
    util.create_detached_head(path, test_branch)
    assert util.is_detached_head(path)


@given("project at <directory> checked out detached HEAD behind <branch>")
def given_directory_checked_out_detached_head_behind_branch(tmp_path: Path, directory: str, branch: str) -> None:
    path = tmp_path / directory
    util.create_detached_head(path, branch)
    assert util.is_detached_head(path)


@given("forall test scripts were copied to the project directories")
def given_forall_test_scripts_present(tmp_path: Path, shared_datadir: Path, scenario_info: ScenarioInfo) -> None:
    dirs = util.example_repo_dirs(scenario_info.example)
    forall_dir = shared_datadir / "forall"
    for d in dirs:
        for script in os.listdir(forall_dir):
            shutil.copy(forall_dir / script, tmp_path / d)
            assert Path(tmp_path / d / script).exists()


@given("yaml test files were copied to clowder directory")
def given_yaml_test_files_present(shared_datadir: Path, tmp_path: Path) -> None:
    yaml_dir = shared_datadir / "yaml"
    path = tmp_path
    for file in os.listdir(yaml_dir):
        existing_file = yaml_dir / file
        shutil.copy(existing_file, path)
        new_file = path / file
        assert new_file.exists()


@given(parsers.parse("created directory {directory}"))
@given("created <directory>")
def given_did_create_directory(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert not path.exists()
    path.mkdir()
    assert path.exists()
    assert path.is_dir()


# @given(parsers.parse("created file {filename}"))
# @given("created <filename>")
# def given_did_create_file(tmp_path: Path, filename: str) -> None:
#     path = tmp_path / filename
#     assert not path.exists()
#     path.touch()
#     assert path.exists()


@given(parsers.parse("created file {filename} in directory {directory}"))
@given("created <filename> in <directory>")
def given_did_create_file_in_directory(tmp_path: Path, filename: str, directory: str) -> None:
    path = tmp_path / directory / filename
    assert not path.exists()
    path.touch()
    assert path.exists()


@given(parsers.parse("repo at {directory} created a new commit"))
@given(parsers.parse("project at {directory} created a new commit"))
@given("project at <directory> created a new commit")
def given_directory_created_new_commit(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    results = util.create_commit(path, "something.txt", "something")
    assert all([r.returncode == 0 for r in results])


@given(parsers.parse("repo at {directory} created {number_commits} new commits"))
@given(parsers.parse("project at {directory} created {number_commits} new commits"))
@given("project at <directory> created <number_commits> new commits")
def given_directory_created_new_commits(tmp_path: Path, directory: str, number_commits: int) -> None:
    path = tmp_path / directory
    results = util.create_number_commits(path, number_commits, "something.txt", "something")
    assert all([r.returncode == 0 for r in results])


# TODO: Split this up into past tense mutating steps and git assertion steps
@given("project at <directory> is behind upstream <start_branch> by <number_commits>")
def given_directory_behind_upstream_num_commits_start_branch(tmp_path: Path, directory: str,
                                                             start_branch: str, number_commits: int) -> None:
    path = tmp_path / directory
    local = "HEAD"
    remote = f"origin/{start_branch}"
    assert util.has_no_commits_between_refs(path, local, remote)
    util.reset_back_by_number_of_commits(path, number_commits)
    assert util.is_behind_by_number_commits(path, local, remote, number_commits)


# TODO: Split this up into past tense mutating steps and git assertion steps
@given("project at <directory> is behind upstream <test_branch> by <number_commits>")
def given_directory_behind_upstream_num_commits_test_branch(tmp_path: Path, directory: str,
                                                            test_branch: str, number_commits: int) -> None:
    path = tmp_path / directory
    local = "HEAD"
    remote = f"origin/{test_branch}"
    assert util.has_no_commits_between_refs(path, local, remote)
    util.reset_back_by_number_of_commits(path, number_commits)
    assert util.is_behind_by_number_commits(path, local, remote, number_commits)


# TODO: Split this up into past tense mutating steps and git assertion steps
@given("project at <directory> is ahead of upstream <start_branch> by <number_commits>")
def given_directory_ahead_upstream_num_commits_start_branch(tmp_path: Path, directory: str,
                                                            start_branch: str, number_commits: int) -> None:
    path = tmp_path / directory
    local = "HEAD"
    remote = f"origin/{start_branch}"
    assert util.has_no_commits_between_refs(path, local, remote)
    util.create_number_commits(path, number_commits, "something.txt", "something")
    assert util.is_ahead_by_number_commits(path, local, remote, number_commits)


# TODO: Split this up into past tense mutating steps and git assertion steps
@given("project at <directory> is ahead of upstream <test_branch> by <number_commits>")
def given_directory_ahead_upstream_num_commits_test_branch(tmp_path: Path, directory: str,
                                                           test_branch: str, number_commits: int) -> None:
    path = tmp_path / directory
    local = "HEAD"
    remote = f"origin/{test_branch}"
    assert util.has_no_commits_between_refs(path, local, remote)
    util.create_number_commits(path, number_commits, "something.txt", "something")
    assert util.is_ahead_by_number_commits(path, local, remote, number_commits)


# TODO: Split this up into past tense mutating steps and git assertion steps
@given("project at <directory> is behind upstream <start_branch> by <number_behind> and ahead by <number_ahead>")
def given_directory_behind_ahead_upstream_num_commits_start_branch(tmp_path: Path, directory: str, start_branch: str,
                                                                   number_behind: int, number_ahead: int) -> None:
    path = tmp_path / directory
    local = "HEAD"
    remote = f"origin/{start_branch}"
    assert util.has_no_commits_between_refs(path, local, remote)
    util.reset_back_by_number_of_commits(path, number_behind)
    assert util.is_behind_by_number_commits(path, local, remote, number_behind)
    util.create_number_commits(path, number_ahead, "something.txt", "something")
    assert util.is_behind_ahead_by_number_commits(path, local, remote, number_behind, number_ahead)


# TODO: Split this up into past tense mutating steps and git assertion steps
@given("project at <directory> is behind upstream <test_branch> by <number_behind> and ahead by <number_ahead>")
def given_directory_behind_ahead_upstream_num_commits_test_branch(tmp_path: Path, directory: str, test_branch: str,
                                                                  number_behind: int, number_ahead: int) -> None:
    path = tmp_path / directory
    local = "HEAD"
    remote = f"origin/{test_branch}"
    assert util.has_no_commits_between_refs(path, local, remote)
    util.reset_back_by_number_of_commits(path, number_behind)
    assert util.is_behind_by_number_commits(path, local, remote, number_behind)
    util.create_number_commits(path, number_ahead, "something.txt", "something")
    assert util.is_behind_ahead_by_number_commits(path, local, remote, number_behind, number_ahead)


@given(parsers.parse("repo at {directory} created remote branch {test_branch}"))
@given(parsers.parse("project at {directory} created remote branch {test_branch}"))
@given("project at <directory> created remote branch <test_branch>")
def given_directory_created_remote_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    path = tmp_path / directory
    results = util.create_remote_branch(path, test_branch)
    assert all([r.returncode == 0 for r in results])


@given(parsers.parse("repo at {directory} deleted remote branch {test_branch}"))
@given(parsers.parse("project at {directory} deleted remote branch {test_branch}"))
@given("project at <directory> deleted remote branch <test_branch>")
def given_directory_deleted_remote_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    path = tmp_path / directory
    if util.remote_branch_exists(path, test_branch):
        result = util.delete_remote_branch(path, test_branch)
        assert result.returncode == 0
    assert not util.remote_branch_exists(path, test_branch)


@given(parsers.parse("repo at {directory} deleted local branch {test_branch}"))
@given(parsers.parse("project at {directory} deleted local branch {test_branch}"))
@given("project at <directory> deleted local branch <test_branch>")
def given_directory_deleted_local_test_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    path = tmp_path / directory
    if util.local_branch_exists(path, test_branch):
        result = util.delete_local_branch(path, test_branch)
        assert result.returncode == 0
    assert not util.local_branch_exists(path, test_branch)


@given("project at <directory> deleted local branch <branch>")
def given_directory_deleted_local_branch(tmp_path: Path, directory: str, branch: str) -> None:
    path = tmp_path / directory
    if util.local_branch_exists(path, branch):
        result = util.delete_local_branch(path, branch)
        assert result.returncode == 0
    assert not util.local_branch_exists(path, branch)


@given(parsers.parse("repo at {directory} created tracking branch {branch}"))
@given(parsers.parse("project at {directory} created tracking branch {branch}"))
@given("project at <directory> created tracking branch <branch>")
def given_created_tracking_branch(tmp_path: Path, directory: str, branch: str) -> None:
    path = tmp_path / directory
    results = util.create_tracking_branch(path, branch)
    assert all([r.returncode == 0 for r in results])


@given("project at <directory> created tracking branch <test_branch>")
def given_created_tracking_branch_test_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    path = tmp_path / directory
    results = util.create_tracking_branch(path, test_branch)
    assert all([r.returncode == 0 for r in results])


@given(parsers.parse("repo at {directory} created tracking branch {branch} on remote {remote}"))
@given(parsers.parse("project at {directory} created tracking branch {branch} on remote {remote}"))
@given("project at <directory> created tracking branch <branch> on remote <remote>")
def given_created_tracking_branch_remote(tmp_path: Path, directory: str, branch: str, remote: str) -> None:
    path = tmp_path / directory
    results = util.create_tracking_branch(path, branch, remote)
    assert all([r.returncode == 0 for r in results])


@given(parsers.parse("repo at {directory} has local commits and is behind remote branch {test_branch}"))
@given(parsers.parse("project at {directory} has local commits and is behind remote branch {test_branch}"))
@given("project at <directory> has local commits and is behind remote branch <test_branch>")
def given_directory_local_commits_behind_upstream(tmp_path: Path, directory: str, test_branch: str) -> None:
    path = tmp_path / directory
    beginning_sha = util.get_branch_commit_sha(path, test_branch, "origin")
    num_commits = 3
    util.create_number_commits(path, num_commits, "something", "something")
    util.push_to_remote_branch(path, test_branch)
    util.reset_back_by_number_of_commits(path, num_commits)
    util.create_number_commits(path, num_commits, "something", "something else")
    yield
    util.abort_rebase(path)
    util.reset_back_by_number_of_commits(path, num_commits)
    util.force_push_to_remote_branch(path, test_branch)
    end_sha = util.get_branch_commit_sha(path, test_branch, "origin")
    assert beginning_sha == end_sha
