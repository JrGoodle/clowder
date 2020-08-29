"""New syntax test file"""

import os
import shutil
from pathlib import Path

from git import Repo
# noinspection PyPackageRequirements
from pytest_bdd import scenarios, given, parsers

import tests.functional.util as util
from .util import TestInfo

scenarios('../features')


@given(parsers.parse("test directory is empty"))
def given_test_dir_empty(tmp_path: Path) -> None:
    assert util.is_directory_empty(tmp_path)


@given(parsers.parse("cats example is initialized"))
def given_cats_init(tmp_path: Path, cats_init, test_info: TestInfo) -> None:
    test_info.example = "cats"


@given(parsers.parse("cats example is initialized and herded"))
def given_cats_init_herd(tmp_path: Path, cats_init_herd, test_info: TestInfo) -> None:
    test_info.example = "cats"


@given(parsers.parse("misc example is initialized"))
def given_misc_init(tmp_path: Path, misc_init, test_info: TestInfo) -> None:
    test_info.example = "misc"


@given(parsers.parse("cats example is initialized to yaml-validation"))
def given_cats_init_branch_yaml_validation(tmp_path: Path, cats_init_yaml_validation, test_info: TestInfo) -> None:
    test_info.example = "misc"
    test_info.branch = "yaml-validation"


# @given(parsers.parse("cats example is initialized to yaml-validation and herded to test-empty-project"))
# def given_cats_init_yaml_validation_herd_test_empty_project(tmp_path: Path,
#                                                             cats_init_yaml_validation_herd_test_empty_project,
#                                                             test_info: TestInfo) -> None:
#     test_info.example = "misc"
#     test_info.branch = "yaml-validation"
#     test_info.version = "test-empty-project"


@given(parsers.parse("cats example is initialized to extension"))
def given_cats_init_branch_extension(tmp_path: Path, cats_init_extension, test_info: TestInfo) -> None:
    test_info.example = "misc"
    test_info.branch = "extension"


@given(parsers.parse("misc example is initialized and herded"))
def given_misc_init_herd(tmp_path: Path, misc_init_herd, test_info: TestInfo) -> None:
    test_info.example = "misc"


@given(parsers.parse("misc example is initialized and herded with https"))
def given_misc_init_herd(tmp_path: Path, misc_init_herd_version_https, test_info: TestInfo) -> None:
    test_info.example = "misc"
    test_info.version = "https"


@given(parsers.parse("{example} example is initialized to {branch}"))
def given_example_init_branch(tmp_path: Path, example: str, branch: str) -> None:
    url = util.get_url(example)
    command = f"clowder init {url} -b {branch}"
    util.run_command(command, tmp_path)


@given(parsers.parse("{example} example is initialized and herded to {branch}"))
def given_example_init_branch_herd(tmp_path: Path, example: str, branch: str) -> None:
    url = util.get_url(example)
    command = f"clowder init {url} -b {branch}"
    util.run_command(command, tmp_path, check=True)
    command = f"clowder herd"
    util.run_command(command, tmp_path, check=True)


@given(parsers.parse("'{command}' has been run"))
def given_run_clowder_command(tmp_path: Path, command: str) -> None:
    command = f"{command}"
    util.run_command(command, tmp_path)


@given(parsers.parse("{version} clowder version is linked"))
def given_is_clowder_version_linked(tmp_path: Path, version: str) -> None:
    if "default" == version:
        assert util.has_valid_clowder_symlink_default(tmp_path)
    else:
        assert util.has_valid_clowder_symlink_version(tmp_path, version)


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


@given(parsers.parse("{version} clowder version exists"))
def given_clowder_version_present(tmp_path: Path, version: str) -> None:
    assert util.has_clowder_version(tmp_path, version)


@given(parsers.parse("{version} clowder version doesn't exist"))
def given_clowder_version_not_present(tmp_path: Path, version: str) -> None:
    assert not util.has_clowder_version(tmp_path, version)


@given("I'm in an empty directory")
def given_is_empty_directory(tmp_path: Path) -> None:
    print(f"tmp_path: {tmp_path}")
    assert util.is_directory_empty(tmp_path)


@given(parsers.parse("file {file_name} doesn't exist"))
def given_has_no_file(tmp_path: Path, file_name: str) -> None:
    path = tmp_path / file_name
    assert not path.exists()


@given(parsers.parse("file {file_name} exists"))
def given_has_file(tmp_path: Path, file_name: str) -> None:
    path = tmp_path / file_name
    assert path.exists()
    assert not path.is_dir()


@given(parsers.parse("symlink {file_name} doesn't exist"))
def given_has_no_symlink(tmp_path: Path, file_name: str) -> None:
    path = tmp_path / file_name
    assert not path.exists()


@given(parsers.parse("symlink {file_name} exists"))
def given_has_symlink(tmp_path: Path, file_name: str) -> None:
    path = tmp_path / file_name
    assert util.is_valid_symlink(path)


@given(parsers.parse("symlinks {file_name_1} and {file_name_2} exist"))
def given_has_two_symlinks(tmp_path: Path, file_name_1: str, file_name_2: str) -> None:
    path = tmp_path / file_name_1
    assert util.is_valid_symlink(path)
    path = tmp_path / file_name_2
    assert util.is_valid_symlink(path)


@given(parsers.parse("symlink {target} was created pointing to {source}"))
def given_created_symlink(tmp_path: Path, target: str, source: str) -> None:
    target_path = tmp_path / target
    source_path = tmp_path / source
    util.create_symlink(source_path, target_path)


@given("<directory> doesn't exist")
def given_has_no_directory(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert not path.exists()


@given("clowder versions directory doesn't exist")
def given_has_no_clowder_versions_directory(tmp_path: Path) -> None:
    path = tmp_path / ".clowder" / "versions"
    assert not path.exists()


@given(parsers.parse("{directory} has untracked file {name}"))
def given_untracked_file(tmp_path: Path, directory: str, name: str) -> None:
    repo_path = tmp_path / directory
    path = tmp_path / directory / name
    util.create_file(path)
    repo = Repo(repo_path)
    assert repo.untracked_files


@given("<directory> has new staged file <test_file>")
def given_new_staged_file(tmp_path: Path, directory: str, test_file: str) -> None:
    repo_path = tmp_path / directory
    path = tmp_path / directory / test_file
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


@given("project at <directory> is on <start_branch>")
def given_directory_on_start_branch(tmp_path: Path, directory: str, start_branch: str) -> None:
    path = tmp_path / directory
    assert util.is_on_active_branch(path, start_branch)


@given("project at <directory> has local branch <test_branch>")
def given_directory_has_local_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    assert util.local_branch_exists(tmp_path / directory, test_branch)


@given("project at <directory> has no local branch <test_branch>")
def given_directory_has_no_local_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    assert not util.local_branch_exists(tmp_path / directory, test_branch)


@given("project at <directory> has no remote branch <test_branch>")
def given_directory_has_no_remote_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    assert not util.remote_branch_exists(tmp_path / directory, test_branch)


@given("project at <directory> is on <branch>")
def given_directory_branch(tmp_path: Path, directory: str, branch: str) -> None:
    path = tmp_path / directory
    assert util.is_on_active_branch(path, branch)


@given("project at <directory> is on <tag>")
def given_directory_tag(tmp_path: Path, directory: str, tag: str) -> None:
    path = tmp_path / directory
    assert util.is_detached_head_on_tag(path, tag)


@given("project at <directory> is on <commit>")
def given_directory_commit(tmp_path: Path, directory: str, commit: str) -> None:
    path = tmp_path / directory
    assert util.is_detached_head_on_commit(path, commit)


@given("project at <directory> is clean")
def given_directory_clean(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert not util.is_dirty(path)


@given("project at <directory> created a new commit")
def given_directory_created_new_commit(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    util.create_commit(path, "something")


@given("project at <directory> is behind upstream <start_branch> by <number_commits>")
def given_directory_behind_upstream_num_commits(tmp_path: Path, directory: str,
                                                start_branch: str, number_commits: str) -> None:
    path = tmp_path / directory
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
