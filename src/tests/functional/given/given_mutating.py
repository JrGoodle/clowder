"""New syntax test file"""

import os
import shutil
from pathlib import Path

from git import Repo
# noinspection PyPackageRequirements
from pytest_bdd import scenarios, given, parsers

import tests.functional.util as util
from tests.functional.util import TestInfo

scenarios('../../features')


@given(parsers.parse("{example} example is initialized to {branch}"))
def given_example_init_branch(tmp_path: Path, example: str, branch: str) -> None:
    url = util.get_url(example)
    result = util.run_command(f"clowder init {url} -b {branch}", tmp_path)
    assert result.returncode == 0


@given(parsers.parse("{example} example is initialized and herded to {branch}"))
def given_example_init_branch_herd(tmp_path: Path, example: str, branch: str) -> None:
    url = util.get_url(example)
    result = util.run_command(f"clowder init {url} -b {branch}", tmp_path)
    assert result.returncode == 0
    result = util.run_command(f"clowder herd", tmp_path)
    assert result.returncode == 0


@given(parsers.parse("'{command}' has been run"))
def given_run_clowder_command(tmp_path: Path, command: str) -> None:
    result = util.run_command(command, tmp_path)
    assert result.returncode == 0


@given(parsers.parse("did link {version} clowder version"))
def given_did_link_clowder_version(tmp_path: Path, version: str) -> None:
    if "default" == version:
        result = util.run_command("clowder link", tmp_path, check=True)
        assert result.returncode == 0
        assert util.has_valid_clowder_symlink_default(tmp_path)
    else:
        result = util.run_command(f"clowder link {version}", tmp_path)
        assert result.returncode == 0
        assert util.has_valid_clowder_symlink_version(tmp_path, version)


@given(parsers.parse("symlink {target} was created pointing to {source}"))
def given_created_symlink(tmp_path: Path, target: str, source: str) -> None:
    target_path = tmp_path / target
    source_path = tmp_path / source
    util.create_symlink(source_path, target_path)


@given(parsers.parse("{directory} has untracked file {name}"))
def given_untracked_file(tmp_path: Path, directory: str, name: str) -> None:
    repo_path = tmp_path / directory
    path = tmp_path / directory / name
    util.create_file(path)
    # TODO: Move most of this logic into utils
    repo = Repo(repo_path)
    assert repo.untracked_files


@given("<directory> has new staged file <test_file>")
def given_new_staged_file(tmp_path: Path, directory: str, test_file: str) -> None:
    repo_path = tmp_path / directory
    path = tmp_path / directory / test_file
    # TODO: Move most of this logic into utils
    util.create_file(path)
    repo = Repo(repo_path)
    assert repo.untracked_files
    repo.git.add(path)
    assert repo.index.diff("HEAD")


@given("project at <directory> created <test_branch>")
def given_directory_created_local_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    path = tmp_path / directory
    util.create_branch(path, test_branch)
    assert util.local_branch_exists(tmp_path / directory, test_branch)


@given("project at <directory> checked out <test_branch>")
def given_directory_checked_out_start_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    path = tmp_path / directory
    util.checkout_branch(path, test_branch)
    assert util.is_on_active_branch(path, test_branch)


@given("project at <directory> created a new commit")
def given_directory_created_new_commit(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    util.create_commit(path, "something")


@given("project at <directory> is behind upstream <start_branch> by <number_commits>")
def given_directory_behind_upstream_num_commits(tmp_path: Path, directory: str,
                                                start_branch: str, number_commits: str) -> None:
    path = tmp_path / directory
    # TODO: Move most of this logic into utils
    assert util.number_of_commits_between_refs(path, "HEAD", f"origin/{start_branch}") == 0
    assert util.number_of_commits_between_refs(path, f"origin/{start_branch}", "HEAD") == 0
    util.reset_back_by_number_of_commits(path, int(number_commits))
    num = util.number_of_commits_between_refs(path, "HEAD", f"origin/{start_branch}")
    assert num == int(number_commits)
    num = util.number_of_commits_between_refs(path, f"origin/{start_branch}", "HEAD")
    assert num == 0


@given("project at <directory> is ahead of upstream <start_branch> by <number_commits>")
def given_directory_ahead_upstream_num_commits(tmp_path: Path, directory: str,
                                               start_branch: str, number_commits: str) -> None:
    path = tmp_path / directory
    # TODO: Move most of this logic into utils
    assert util.number_of_commits_between_refs(path, "HEAD", f"origin/{start_branch}") == 0
    assert util.number_of_commits_between_refs(path, f"origin/{start_branch}", "HEAD") == 0
    util.reset_back_by_number_of_commits(path, int(number_commits))
    num = util.number_of_commits_between_refs(path, "HEAD", f"origin/{start_branch}")
    assert num == int(number_commits)
    num = util.number_of_commits_between_refs(path, f"origin/{start_branch}", "HEAD")
    assert num == 0


@given("project at <directory> is behind upstream <start_branch> by <number_behind> and ahead by <number_ahead>")
def given_directory_behind_ahead_upstream_num_commits(tmp_path: Path, directory: str, start_branch: str,
                                                      number_behind: str, number_ahead: str) -> None:
    path = tmp_path / directory
    # TODO: Move most of this logic into utils
    num = util.number_of_commits_between_refs(path, "HEAD", f"origin/{start_branch}")
    assert num == 0
    num = util.number_of_commits_between_refs(path, f"origin/{start_branch}", "HEAD")
    assert num == 0

    util.reset_back_by_number_of_commits(path, int(number_behind))

    num = util.number_of_commits_between_refs(path, "HEAD", f"origin/{start_branch}")
    assert num == int(number_behind)
    num = util.number_of_commits_between_refs(path, f"origin/{start_branch}", "HEAD")
    assert num == 0

    commits = int(number_ahead)
    while commits > 0:
        results = util.create_commit(path, f"something_{commits}")
        assert all([r.returncode == 0 for r in results])
        commits -= 1

    num = util.number_of_commits_between_refs(path, "HEAD", f"origin/{start_branch}")
    assert num == int(number_behind)
    num = util.number_of_commits_between_refs(path, f"origin/{start_branch}", "HEAD")
    assert num == int(number_ahead)


@given("forall test scripts are in the project directories")
def given_forall_test_scripts_present(tmp_path: Path, shared_datadir: Path, test_info: TestInfo) -> None:
    dirs = util.example_repo_dirs(test_info.example)
    forall_dir = shared_datadir / "forall"
    for d in dirs:
        for script in os.listdir(forall_dir):
            shutil.copy(forall_dir / script, tmp_path / d)
            assert Path(tmp_path / d / script).exists()


@given("yaml test files are in clowder directory")
def given_yaml_test_files_present(tmp_path: Path, shared_datadir: Path) -> None:
    yaml_dir = shared_datadir / "yaml"
    for file in os.listdir(yaml_dir):
        shutil.copy(yaml_dir / file, tmp_path)
        assert Path(tmp_path / file).exists()
