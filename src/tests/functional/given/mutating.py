"""New syntax test file"""

import os
import shutil
from pathlib import Path

# noinspection PyPackageRequirements
from pytest_bdd import scenarios, given, parsers

import tests.functional.util as util
from tests.functional.util import ScenarioInfo

scenarios('../../features')


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


@given(parsers.parse("repo at {directory} staged file {file_name}"))
@given(parsers.parse("project at {directory} staged file {file_name}"))
@given("project at <directory> staged <file_name>")
def given_did_stage_file(tmp_path: Path, directory: str, file_name: str) -> None:
    path = tmp_path / directory
    util.git_add_file(path, file_name)


@given("project at <directory> created <test_branch>")
def given_directory_created_local_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    path = tmp_path / directory
    util.create_local_branch(path, test_branch)
    assert util.local_branch_exists(tmp_path / directory, test_branch)


@given("project at <directory> checked out <test_branch>")
def given_directory_checked_out_start_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    path = tmp_path / directory
    util.checkout_branch(path, test_branch)
    assert util.is_on_active_branch(path, test_branch)


@given("forall test scripts were copied to the project directories")
def given_forall_test_scripts_present(tmp_path: Path, shared_datadir: Path, scenario_info) -> None:
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


# @given(parsers.parse("created file {file_name}"))
# @given("created <file_name>")
# def given_did_create_file(tmp_path: Path, file_name: str) -> None:
#     path = tmp_path / file_name
#     assert not path.exists()
#     path.touch()
#     assert path.exists()


@given(parsers.parse("created file {file_name} in directory {directory}"))
@given("created <file_name> in <directory>")
def given_did_create_file_in_directory(tmp_path: Path, file_name: str, directory: str) -> None:
    path = tmp_path / directory / file_name
    assert not path.exists()
    path.touch()
    assert path.exists()


@given(parsers.parse("repo at {directory} created a new commit"))
@given(parsers.parse("project at {directory} created a new commit"))
@given("project at <directory> created a new commit")
def given_directory_created_new_commit(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    util.create_commit(path, "something")


@given(parsers.parse("repo at {directory} created {number_commits} new commits"))
@given(parsers.parse("project at {directory} created {number_commits} new commits"))
@given("project at <directory> created <number_commits> new commits")
def given_directory_created_new_commits(tmp_path: Path, directory: str, number_commits: str) -> None:
    path = tmp_path / directory
    commits = int(number_commits)
    while commits > 0:
        results = util.create_commit(path, f"something_{commits}")
        assert all([r.returncode == 0 for r in results])
        commits -= 1


# TODO: Split this up into past tense mutating steps and git assertion steps
@given("project at <directory> is behind upstream <start_branch> by <number_commits>")
def given_directory_behind_upstream_num_commits(tmp_path: Path, directory: str,
                                                start_branch: str, number_commits: str) -> None:
    number_commits = int(number_commits)
    path = tmp_path / directory
    local = "HEAD"
    remote = f"origin/{start_branch}"
    assert util.has_no_commits_between_refs(path, local, remote)
    util.reset_back_by_number_of_commits(path, number_commits)
    assert util.is_behind_by_number_commits(path, local, remote, number_commits)


# TODO: Split this up into past tense mutating steps and git assertion steps
@given("project at <directory> is ahead of upstream <start_branch> by <number_commits>")
def given_directory_ahead_upstream_num_commits(tmp_path: Path, directory: str,
                                               start_branch: str, number_commits: str) -> None:
    number_commits = int(number_commits)
    path = tmp_path / directory
    local = "HEAD"
    remote = f"origin/{start_branch}"
    assert util.has_no_commits_between_refs(path, local, remote)
    util.create_number_commits(path, "something.txt", number_commits)
    assert util.is_ahead_by_number_commits(path, local, remote, number_commits)


# TODO: Split this up into past tense mutating steps and git assertion steps
@given("project at <directory> is behind upstream <start_branch> by <number_behind> and ahead by <number_ahead>")
def given_directory_behind_ahead_upstream_num_commits(tmp_path: Path, directory: str, start_branch: str,
                                                      number_behind: str, number_ahead: str) -> None:
    number_behind = int(number_behind)
    number_ahead = int(number_ahead)
    path = tmp_path / directory
    local = "HEAD"
    remote = f"origin/{start_branch}"
    assert util.has_no_commits_between_refs(path, local, remote)
    util.reset_back_by_number_of_commits(path, number_behind)
    assert util.is_behind_by_number_commits(path, local, remote, number_behind)
    util.create_number_commits(path, "something.txt", number_ahead)
    assert util.is_behind_ahead_by_number_commits(path, local, remote, number_behind, number_ahead)
