"""New syntax test file"""

import os
import shutil
from pathlib import Path

from git import Repo
# noinspection PyPackageRequirements
from pytest_bdd import scenarios, given, parsers

import tests.functional.util as util
from .util import CATS_REPOS_DEFAULT, MISC_REPOS_DEFAULT, SWIFT_REPOS_DEFAULT, TestInfo

scenarios('../features')


@given(parsers.parse("test directory is empty"))
def given_test_dir_empty() -> None:
    pass


@given(parsers.parse("cats example is initialized"))
def given_cats_example_init(tmp_path: Path, cats_init_default, test_info: TestInfo) -> None:
    test_info.example = "cats"


@given(parsers.parse("cats example is initialized and herded"))
def given_cats_example_init_herd(tmp_path: Path, cats_init_herd_default, test_info: TestInfo) -> None:
    test_info.example = "cats"


@given(parsers.parse("misc example is initialized"))
def given_misc_example_init(tmp_path: Path, misc_init_default, test_info: TestInfo) -> None:
    test_info.example = "misc"


@given(parsers.parse("misc example is initialized and herded"))
def given_misc_example_init_herd(tmp_path: Path, misc_init_herd_default, test_info: TestInfo) -> None:
    test_info.example = "misc"


@given(parsers.parse("{example} example is initialized to {branch}"))
def given_example_init_branch(tmp_path: Path, example: str, branch: str) -> None:
    url = util.get_url(example)
    command = f"clowder init {url} -b {branch}"
    util.run_command(command, tmp_path)


@given(parsers.parse("{example} example is initialized with {protocol}"))
def given_example_init_protocol(tmp_path: Path, example: str, protocol: str) -> None:
    url = util.get_url(example, protocol=protocol)
    command = f"clowder init {url}"
    util.run_command(command, tmp_path)


@given(parsers.parse("{example} example is initialized to {branch} with {protocol}"))
def given_example_init_branch_protocol(tmp_path: Path, example: str, branch, protocol: str) -> None:
    url = util.get_url(example, protocol=protocol)
    command = f"clowder init {url} -b {branch}"
    util.run_command(command, tmp_path)


@given(parsers.parse("'clowder {command}' has been run"))
def given_run_clowder_command(tmp_path: Path, command: str) -> None:
    command = f"clowder {command}"
    util.run_command(command, tmp_path)


@given(parsers.parse("{version} clowder.yaml version is linked"))
@given(parsers.parse("{version} clowder.yml version is linked"))
@given(parsers.parse("{version} yaml version is linked"))
def given_link_yaml_version(tmp_path: Path, version: str) -> None:
    command = f"clowder link {version}"
    util.run_command(command, tmp_path)
    assert util.has_valid_clowder_version_symlink(tmp_path, version)


@given("I'm in an empty directory")
def given_is_empty_directory(tmp_path: Path) -> None:
    print(f"tmp_path: {tmp_path}")
    assert util.is_directory_empty(tmp_path)


@given("<directory> doesn't exist")
def given_has_no_directory(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert not path.exists()


@given(parsers.parse("{directory} has untracked file {name}"))
def given_untracked_file(tmp_path: Path, directory: str, name: str) -> None:
    repo_path = tmp_path / directory
    path = tmp_path / directory / name
    util.create_file(path)
    repo = Repo(repo_path)
    assert repo.untracked_files


@given("project at <directory> is on <start_branch>")
def given_check_directory_start_branch(tmp_path: Path, directory: str, start_branch: str) -> None:
    path = tmp_path / directory
    assert util.is_on_active_branch(path, start_branch)


@given("project at <directory> is on <branch>")
def given_check_directory_branch(tmp_path: Path, directory: str, branch: str) -> None:
    path = tmp_path / directory
    assert util.is_on_active_branch(path, branch)


@given("project at <directory> is on <tag>")
def given_check_directory_tag(tmp_path: Path, directory: str, tag: str) -> None:
    path = tmp_path / directory
    assert util.is_detached_head_on_tag(path, tag)


@given("project at <directory> is on <commit>")
def given_check_directory_commit(tmp_path: Path, directory: str, commit: str) -> None:
    path = tmp_path / directory
    assert util.is_detached_head_on_commit(path, commit)


@given("project at <directory> is clean")
def given_check_directory_clean(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert not util.is_dirty(path)


@given("forall test scripts are in the project directories")
def forall_test_scripts_present(tmp_path: Path, shared_datadir: Path, test_info: TestInfo) -> None:
    if test_info.example == "cats":
        dirs = [info["path"] for name, info in CATS_REPOS_DEFAULT.items()]
    elif test_info.example == "misc":
        dirs = [info["path"] for name, info in MISC_REPOS_DEFAULT.items()]
    elif test_info.example == "swift":
        dirs = [info["path"] for name, info in SWIFT_REPOS_DEFAULT.items()]
    else:
        assert False

    forall_dir = shared_datadir / "forall"
    for d in dirs:
        for script in os.listdir(forall_dir):
            shutil.copy(forall_dir / script, tmp_path / d)
            assert Path(tmp_path / d / script).exists()
