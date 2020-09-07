"""New syntax test file"""

from pathlib import Path

from pytest_bdd import given, parsers

import tests.functional.util as util
from tests.functional.util import ScenarioInfo, CATS_REPOS_DEFAULT


@given(parsers.parse("cats example is initialized"))
def given_cats_init(tmp_path: Path, cats_init, scenario_info: ScenarioInfo) -> None:
    scenario_info.example = "cats"


@given(parsers.parse("cats example is initialized with ssh"))
def given_cats_init_ssh(tmp_path: Path, cats_init_ssh, scenario_info: ScenarioInfo) -> None:
    scenario_info.example = "cats"
    scenario_info.protocol = "ssh"


@given(parsers.parse("cats example is initialized and herded"))
def given_cats_init_herd(tmp_path: Path, cats_init_herd, scenario_info: ScenarioInfo) -> None:
    scenario_info.example = "cats"


@given(parsers.parse("cats example is initialized and herded with ssh"))
def given_cats_init_herd_ssh(tmp_path: Path, cats_init_herd_ssh, scenario_info: ScenarioInfo) -> None:
    scenario_info.example = "cats"
    scenario_info.version = "ssh"
    scenario_info.protocol = "ssh"


@given(parsers.parse("cats example is initialized to branch yaml-validation"))
def given_cats_init_branch_yaml_validation(tmp_path: Path, cats_init_yaml_validation,
                                           scenario_info: ScenarioInfo) -> None:
    scenario_info.example = "cats"
    scenario_info.branch = "yaml-validation"


# @given(parsers.parse("cats example is initialized and herded to branch yaml-validation and version test-empty-project")) # noqa
# def given_cats_init_yaml_validation_herd_test_empty_project(tmp_path: Path,
#                                                             cats_init_yaml_validation_herd_test_empty_project,
#                                                             test_info: TestInfo) -> None:
#     test_info.example = "misc"
#     test_info.branch = "yaml-validation"
#     test_info.version = "test-empty-project"


@given(parsers.parse("cats example is initialized to branch extension"))
def given_cats_init_branch_extension(tmp_path: Path, cats_init_extension, scenario_info: ScenarioInfo) -> None:
    scenario_info.example = "cats"
    scenario_info.branch = "extension"


@given(parsers.parse("cats example non-symlink yaml file exists"))
def given_cats_non_symlink_yaml(tmp_path: Path, cats_non_symlink_yaml, scenario_info: ScenarioInfo) -> None:
    scenario_info.example = "cats"


@given(parsers.parse("cats example non-symlink yml file exists"))
def given_cats_non_symlink_yml(tmp_path: Path, cats_non_symlink_yml, scenario_info: ScenarioInfo) -> None:
    scenario_info.example = "cats"


@given(parsers.parse("cats example ambiguous non-symlink yaml and yml files exist"))
def given_cats_ambiguous_non_symlink_yaml_files(tmp_path: Path, cats_ambiguous_non_symlink_yaml_files,
                                                scenario_info: ScenarioInfo) -> None:
    scenario_info.example = "cats"


@given(parsers.parse("cats example clowder repo symlink exists"))
def given_cats_clowder_repo_symlink(tmp_path: Path, cats_clowder_repo_symlink,
                                    scenario_info: ScenarioInfo) -> None:
    scenario_info.example = "cats"


@given(parsers.parse("cats example projects have no remote branch {test_branch}"))
@given("cats example projects have no remote branch <test_branch>")
def given_cats_no_remote_branch(tmp_path: Path, scenario_info: ScenarioInfo, test_branch: str) -> None:
    scenario_info.example = "cats"
    for name, repo in CATS_REPOS_DEFAULT.items():
        path = tmp_path / repo["path"]
        util.delete_remote_branch(path, test_branch)
        assert not util.remote_branch_exists(path, test_branch)


@given(parsers.parse("cats example projects have remote branch {test_branch}"))
@given("cats example projects have remote branch <test_branch>")
def given_cats_remote_branch(tmp_path: Path, scenario_info: ScenarioInfo, test_branch: str) -> None:
    scenario_info.example = "cats"
    for name, repo in CATS_REPOS_DEFAULT.items():
        path = tmp_path / repo["path"]
        if util.remote_branch_exists(path, test_branch):
            util.delete_remote_branch(path, test_branch)
        util.create_remote_branch(path, test_branch)
        assert util.remote_branch_exists(path, test_branch)


@given(parsers.parse("cats example projects have tracking branch {test_branch}"))
@given("cats example projects have tracking branch <test_branch>")
def given_cats_tracking_branch(tmp_path: Path, scenario_info: ScenarioInfo, test_branch: str) -> None:
    scenario_info.example = "cats"
    for name, repo in CATS_REPOS_DEFAULT.items():
        path = tmp_path / repo["path"]
        if util.remote_branch_exists(path, test_branch):
            util.delete_remote_branch(path, test_branch)
        util.create_tracking_branch(path, test_branch)
        assert util.tracking_branch_exists(path, test_branch)


@given(parsers.parse("cats example projects have local branch {test_branch}"))
@given("cats example projects have local branch <test_branch>")
def given_cats_local_branch(tmp_path: Path, scenario_info: ScenarioInfo, test_branch: str) -> None:
    scenario_info.example = "cats"
    for name, repo in CATS_REPOS_DEFAULT.items():
        path = tmp_path / repo["path"]
        util.create_local_branch(path, test_branch)
        assert util.local_branch_exists(path, test_branch)


@given(parsers.parse("cats example projects have no local branch {test_branch}"))
@given("cats example projects have no local branch <test_branch>")
def given_cats_no_local_branch(tmp_path: Path, scenario_info: ScenarioInfo, test_branch: str) -> None:
    scenario_info.example = "cats"
    for name, repo in CATS_REPOS_DEFAULT.items():
        path = tmp_path / repo["path"]
        util.delete_local_branch(path, test_branch)
        assert not util.local_branch_exists(path, test_branch)
