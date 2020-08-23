"""New syntax test file"""

from pathlib import Path

from git import Repo
# noinspection PyPackageRequirements
from pytest_bdd import scenarios, given, parsers

import tests.functional.common as common

scenarios('../features')


@given(parsers.parse("{example} example is initialized"))
def given_example_init(tmp_path: Path, example: str) -> None:
    url = common.get_url(example)
    command = f"clowder init {url}"
    common.run_command(command, tmp_path)


@given(parsers.parse("{example} example is initialized and herded"))
def given_example_init_herd(tmp_path: Path, example: str, cats_init_herd_default) -> None:
    pass


@given(parsers.parse("{example} example is initialized to {branch}"))
def given_example_init_branch(tmp_path: Path, example: str, branch: str) -> None:
    url = common.get_url(example)
    command = f"clowder init {url} -b {branch}"
    common.run_command(command, tmp_path)


@given(parsers.parse("{example} example is initialized with {protocol}"))
def given_example_init_protocol(tmp_path: Path, example: str, protocol: str) -> None:
    url = common.get_url(example, protocol=protocol)
    command = f"clowder init {url}"
    common.run_command(command, tmp_path)


@given(parsers.parse("{example} example is initialized to {branch} with {protocol}"))
def given_example_init_branch_protocol(tmp_path: Path, example: str, branch, protocol: str) -> None:
    url = common.get_url(example, protocol=protocol)
    command = f"clowder init {url} -b {branch}"
    common.run_command(command, tmp_path)


@given(parsers.parse("'clowder {command}' has been run"))
def given_run_clowder_command(tmp_path: Path, command: str) -> None:
    command = f"clowder {command}"
    common.run_command(command, tmp_path)


@given(parsers.parse("{version} yaml version is linked"))
def given_link_yaml_version(tmp_path: Path, version: str) -> None:
    command = f"clowder link {version}"
    common.run_command(command, tmp_path)
    assert common.has_valid_clowder_version_symlink(tmp_path, version)


@given("I'm in an empty directory")
def given_is_empty_directory(tmp_path: Path) -> None:
    print(f"tmp_path: {tmp_path}")
    assert common.is_directory_empty(tmp_path)


@given("<directory> doesn't exist")
def given_has_no_directory(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert not path.exists()


@given(parsers.parse("{directory} has untracked file {name}"))
def given_untracked_file(tmp_path: Path, directory: str, name: str) -> None:
    repo_path = tmp_path / directory
    path = tmp_path / directory / name
    common.create_file(path)
    repo = Repo(repo_path)
    assert repo.untracked_files
