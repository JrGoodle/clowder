"""New syntax test file"""

import os
import shutil
from pathlib import Path

from clowder.util.git import GitOffline, HEAD, LocalBranch, RemoteBranch, Repo
from pytest_bdd import given, parsers

import clowder.util.filesystem as fs

import tests.functional.util as util
from tests.functional.util import ScenarioInfo


@given(parsers.parse("'{command}' was run"))
def given_run_clowder_command(tmp_path: Path, command: str) -> None:
    util.run_command(command, tmp_path, check=True)


@given(parsers.parse("linked {version} clowder version"))
def given_did_link_clowder_version(tmp_path: Path, version: str) -> None:
    if "default" == version:
        util.run_command("clowder link", tmp_path, check=True)
        assert util.has_valid_clowder_symlink_default(tmp_path)
    else:
        util.run_command(f"clowder link {version}", tmp_path, check=True)
        assert util.has_valid_clowder_symlink_version(tmp_path, version)


@given(parsers.parse("created {name} symlink pointing to {target}"))
def given_created_symlink(tmp_path: Path, name: str, target: str) -> None:
    symlink_path = tmp_path / name
    target_path = tmp_path / target
    assert target_path.exists()
    fs.symlink_to(symlink_path, Path(target))


@given(parsers.parse("created {name_1} and {name_2} symlinks pointing to {target}"))
def given_created_symlinks(tmp_path: Path, name_1: str, name_2: str, target: str) -> None:
    name_path = tmp_path / name_1
    fs.symlink_to(name_path, Path(target))
    name_path = tmp_path / name_2
    fs.symlink_to(name_path, Path(target))


@given(parsers.parse("repo at {directory} staged file {filename}"))
@given(parsers.parse("project at {directory} staged file {filename}"))
@given("project at <directory> staged <filename>")
def given_did_stage_file(tmp_path: Path, directory: str, filename: str) -> None:
    path = tmp_path / directory
    repo = Repo(path)
    repo.add(filename)


@given(parsers.parse("repo at {directory} created local branch {test_branch}"))
@given(parsers.parse("project at {directory} created local branch {test_branch}"))
@given("project at <directory> created local <test_branch>")
def given_directory_created_local_test_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    path = tmp_path / directory
    local_branch = LocalBranch(path, test_branch)
    local_branch.create()
    assert local_branch.exists


@given("project at <directory> created local <branch>")
def given_directory_created_local_branch(tmp_path: Path, directory: str, branch: str) -> None:
    path = tmp_path / directory
    local_branch = LocalBranch(path, branch)
    local_branch.create()
    assert local_branch.exists


@given("project at <directory> checked out <test_branch>")
def given_directory_checked_out_test_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    path = tmp_path / directory
    local_branch = LocalBranch(path, test_branch)
    local_branch.checkout()
    assert local_branch.exists
    assert local_branch.is_checked_out


@given("project at <directory> checked out <branch>")
def given_directory_checked_out_branch(tmp_path: Path, directory: str, branch: str) -> None:
    path = tmp_path / directory
    local_branch = LocalBranch(path, branch)
    local_branch.checkout()
    assert local_branch.exists
    assert local_branch.is_checked_out


@given("project at <directory> checked out detached HEAD behind <test_branch>")
def given_directory_checked_out_detached_head_behind_test_branch(tmp_path: Path, directory: str,
                                                                 test_branch: str) -> None:
    path = tmp_path / directory
    repo = Repo(path)
    repo.checkout(f'{test_branch}~1')
    assert repo.is_detached


@given("project at <directory> checked out detached HEAD behind <branch>")
def given_directory_checked_out_detached_head_behind_branch(tmp_path: Path, directory: str, branch: str) -> None:
    path = tmp_path / directory
    repo = Repo(path)
    repo.checkout(f'{branch}~1')
    assert repo.is_detached


@given("forall test scripts were copied to the project directories")
def given_forall_test_scripts_present(tmp_path: Path, shared_datadir: Path, scenario_info: ScenarioInfo) -> None:
    dirs = util.example_repo_dirs(scenario_info.example)
    forall_dir = shared_datadir / "forall"
    for d in dirs:
        for script in os.listdir(forall_dir):
            shutil.copy(forall_dir / script, tmp_path / d)
            assert Path(tmp_path / d / script).exists()


@given(parsers.parse("created directory {directory}"))
@given("created <directory>")
def given_did_create_directory(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert not path.exists()
    path.mkdir()
    assert path.exists()
    assert path.is_dir()


@given(parsers.parse("created directory {test_directory}"))
@given("created <test_directory>")
def given_did_create_test_directory(tmp_path: Path, test_directory: str) -> None:
    path = tmp_path / test_directory
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


@given(parsers.parse("created file {filename} in directory {test_directory}"))
@given("created <filename> in <test_directory>")
def given_did_create_file_in_test_directory(tmp_path: Path, filename: str, test_directory: str) -> None:
    path = tmp_path / test_directory / filename
    assert not path.exists()
    path.touch()
    assert path.exists()


@given("cloned cats repo in <directory>")
def given_created_git_dir_in_dir(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    util.run_command("git clone https://github.com/JrGoodle/cats.git", path)
    cats_dir = path / "cats"
    repo = Repo(cats_dir)
    assert repo.exists


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
def given_directory_created_new_commits(tmp_path: Path, directory: str, number_commits: str) -> None:
    number_commits = int(number_commits)
    path = tmp_path / directory
    results = util.create_number_commits(path, number_commits, "something.txt")
    assert all([r.returncode == 0 for r in results])


# TODO: Split this up into past tense mutating steps and git assertion steps
@given("project at <directory> is behind upstream <start_branch> by <number_commits>")
def given_directory_behind_upstream_num_commits_start_branch(tmp_path: Path, directory: str,
                                                             start_branch: str, number_commits: str) -> None:
    number_commits = int(number_commits)
    path = tmp_path / directory
    local = HEAD
    remote = f"origin/{start_branch}"
    assert GitOffline.has_no_commits_between_refs(path, local, remote)
    util.set_up_behind(path, local, remote, number_commits)


@given("project at <directory> is behind upstream <test_branch> by <number_commits>")
def given_directory_behind_upstream_num_commits_test_branch(tmp_path: Path, directory: str,
                                                            test_branch: str, number_commits: str) -> None:
    number_commits = int(number_commits)
    path = tmp_path / directory
    local = HEAD
    remote = f"origin/{test_branch}"
    assert GitOffline.has_no_commits_between_refs(path, local, remote)
    util.set_up_behind(path, local, remote, number_commits)


@given("project at <directory> is ahead of upstream <start_branch> by <number_commits>")
def given_directory_ahead_upstream_num_commits_start_branch(tmp_path: Path, directory: str,
                                                            start_branch: str, number_commits: str) -> None:
    number_commits = int(number_commits)
    path = tmp_path / directory
    local = HEAD
    remote = f"origin/{start_branch}"
    assert GitOffline.has_no_commits_between_refs(path, local, remote)
    util.set_up_ahead(path, local, remote, number_commits)


@given("project at <directory> is ahead of upstream <test_branch> by <number_commits>")
def given_directory_ahead_upstream_num_commits_test_branch(tmp_path: Path, directory: str,
                                                           test_branch: str, number_commits: str) -> None:
    number_commits = int(number_commits)
    path = tmp_path / directory
    local = HEAD
    remote = f"origin/{test_branch}"
    assert GitOffline.has_no_commits_between_refs(path, local, remote)
    util.set_up_ahead(path, local, remote, number_commits)


@given("project at <directory> is behind upstream <start_branch> by <number_behind> and ahead by <number_ahead>")
def given_directory_behind_ahead_upstream_num_commits_start_branch(tmp_path: Path, directory: str, start_branch: str,
                                                                   number_behind: str, number_ahead: str,
                                                                   scenario_info: ScenarioInfo) -> None:
    number_behind = int(number_behind)
    number_ahead = int(number_ahead)
    path = tmp_path / directory
    local = HEAD
    remote = f"origin/{start_branch}"
    util.set_up_behind_ahead_no_confilct(path, local, remote, number_behind, number_ahead, scenario_info)


@given("project at <directory> is behind upstream <branch> by <number_behind> and ahead by <number_ahead>")
def given_directory_behind_ahead_upstream_num_commits_branch(tmp_path: Path, directory: str, branch: str,
                                                             number_behind: str, number_ahead: str,
                                                             scenario_info: ScenarioInfo) -> None:
    number_behind = int(number_behind)
    number_ahead = int(number_ahead)
    path = tmp_path / directory
    local = HEAD
    remote = f"origin/{branch}"
    util.set_up_behind_ahead_no_confilct(path, local, remote, number_behind, number_ahead, scenario_info)


@given("project at <directory> is behind upstream <test_branch> by <number_behind> and ahead by <number_ahead>")
def given_directory_behind_ahead_upstream_num_commits_test_branch(tmp_path: Path, directory: str, test_branch: str,
                                                                  number_behind: str, number_ahead: str,
                                                                  scenario_info: ScenarioInfo) -> None:
    number_behind = int(number_behind)
    number_ahead = int(number_ahead)
    path = tmp_path / directory
    local = HEAD
    remote = f"origin/{test_branch}"
    util.set_up_behind_ahead_no_confilct(path, local, remote, number_behind, number_ahead, scenario_info)


@given("project at <directory> is behind upstream <test_branch> by <number_behind> and ahead by <number_ahead> with conflict")  # noqa
def given_directory_behind_ahead_upstream_num_commits_test_branch_conflict(tmp_path: Path, directory: str,
                                                                           test_branch: str, number_behind: str,
                                                                           number_ahead: str,
                                                                           scenario_info: ScenarioInfo) -> None:
    number_behind = int(number_behind)
    number_ahead = int(number_ahead)
    path = tmp_path / directory
    util.set_up_behind_ahead_conflict(path, test_branch, number_behind, number_ahead)


@given(parsers.parse("repo at {directory} created remote branch {test_branch}"))
@given(parsers.parse("project at {directory} created remote branch {test_branch}"))
@given("project at <directory> created remote <test_branch>")
def given_directory_created_remote_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    path = tmp_path / directory
    remote_branch = RemoteBranch(path, test_branch)
    remote_branch.create()
    assert remote_branch.exists


@given(parsers.parse("repo at {directory} deleted remote branch {test_branch}"))
@given(parsers.parse("project at {directory} deleted remote branch {test_branch}"))
@given("project at <directory> deleted remote <test_branch>")
def given_directory_deleted_remote_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    path = tmp_path / directory
    remote_branch = RemoteBranch(path, test_branch)
    if remote_branch.exists:
        remote_branch.delete()
    assert not remote_branch.exists


@given(parsers.parse("repo at {directory} deleted local branch {test_branch}"))
@given(parsers.parse("project at {directory} deleted local branch {test_branch}"))
@given("project at <directory> deleted local <test_branch>")
def given_directory_deleted_local_test_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    path = tmp_path / directory
    local_branch = LocalBranch(path, test_branch)
    if local_branch.exists:
        local_branch.delete()
    assert not local_branch.exists


@given("project at <directory> deleted local <branch>")
def given_directory_deleted_local_branch(tmp_path: Path, directory: str, branch: str) -> None:
    path = tmp_path / directory
    local_branch = LocalBranch(path, branch)
    if local_branch.exists:
        local_branch.delete()
    assert not local_branch.exists


# @given(parsers.parse("repo at {directory} created tracking branch {branch}"))
# @given(parsers.parse("project at {directory} created tracking branch {branch}"))
# @given("project at <directory> created tracking branch <branch>")
# def given_created_tracking_branch(tmp_path: Path, directory: str, branch: str) -> None:
#     path = tmp_path / directory
#     results = util.create_tracking_branch(path, branch)
#     assert all([r.returncode == 0 for r in results])
#
#
# @given("project at <directory> created tracking branch <test_branch>")
# def given_created_tracking_branch_test_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
#     path = tmp_path / directory
#     results = util.create_tracking_branch(path, test_branch)
#     assert all([r.returncode == 0 for r in results])
#
#
# @given(parsers.parse("repo at {directory} created tracking branch {branch} on remote {remote}"))
# @given(parsers.parse("project at {directory} created tracking branch {branch} on remote {remote}"))
# @given("project at <directory> created tracking branch <branch> on remote <remote>")
# def given_created_tracking_branch_remote(tmp_path: Path, directory: str, branch: str, remote: str) -> None:
#     path = tmp_path / directory
#     results = util.create_tracking_branch(path, branch, remote)
#     assert all([r.returncode == 0 for r in results])


@given(parsers.parse("repo at {directory} on branch {test_branch} failed to complete rebase"))
@given(parsers.parse("project at {directory} on branch {test_branch} failed to complete rebase"))
@given("project at <directory> on <test_branch> failed to complete rebase")
def given_directory_failed_to_complete_rebase(tmp_path: Path, directory: str, test_branch: str) -> None:
    path = tmp_path / directory
    util.set_up_behind_ahead_conflict(path, test_branch, 1, 3)
    repo = Repo(path)
    try:
        repo.pull(rebase=True)
    except Exception:  # noqa
        pass
    assert repo.is_rebase_in_progress


@given("test config was copied to clowder repo")
def given_test_config_copied_to_clowder_repo(shared_datadir: Path, tmp_path: Path) -> None:
    version = "v0.1"
    filename = "clowder.config.yml"
    test_file = shared_datadir / "config" / version / filename
    path = tmp_path / ".clowder" / "config"
    new_file = path / filename
    contents = test_file.read_text()
    contents = contents.replace("DIRECTORY_PLACEHOLDER", str(tmp_path))
    if not path.exists():
        path.mkdir(parents=True)
    with new_file.open('w') as f:
        f.write(contents)
    assert new_file.exists()


@given("clower repo has no saved versions")
def given_clowder_repo_has_no_saved_versions(tmp_path: Path) -> None:
    path = tmp_path / ".clowder" / "versions"
    shutil.rmtree(path)
    assert not path.exists()


@given("has duplicate clowder versions")
def given_clowder_repo_has_duplicate_versions(tmp_path: Path) -> None:
    symlink = util.valid_clowder_symlink(tmp_path)
    default = symlink.resolve()

    versions_dir = tmp_path / ".clowder" / "versions"
    version_name = "duplicate-version.clowder"
    for version in [f"{version_name}.yml", f"{version_name}.yaml"]:
        version_file = versions_dir / version
        fs.copy_file(default, version_file)
        assert version_file.exists()
        assert version_file.is_file()
        assert not version_file.is_symlink()


@given("has invalid clowder.yml")
def given_clowder_repo_invalid_clowder_yml(tmp_path: Path) -> None:
    clowder_repo = tmp_path / ".clowder"
    versions_dir = clowder_repo / "versions"
    shutil.rmtree(versions_dir)
    assert not versions_dir.exists()

    symlink = util.valid_clowder_symlink(tmp_path)
    default = symlink.resolve()
    default.unlink()
    symlink.unlink()
    assert not default.exists()
    assert not symlink.exists()
    assert not symlink.is_symlink()

    invalid_file = clowder_repo / "clowder.yml"
    fs.create_file(invalid_file, "this is invalid")
    util.run_command("clowder link", tmp_path, check=True)
    symlink = util.valid_clowder_symlink(tmp_path)
    assert symlink.is_symlink()
    assert symlink.exists()
