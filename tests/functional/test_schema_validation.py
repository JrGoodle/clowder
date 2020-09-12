"""test_features"""

import pytest
from pathlib import Path
from pytest import fixture
from typing import List, Tuple

from pytest_bdd import given, scenario, then, when, parsers

import tests.functional.util as util
from tests.functional.util import CommandResults, yaml_property_tests, ScenarioInfo


branch_tests: List[Tuple[str]] = [(f,) for f in yaml_property_tests("project.branch")]


@pytest.mark.parametrize(["branch_test_file"], branch_tests)
@scenario(
    "../features/yaml_validation.feature",
    "validate project.branch",
)
def test_validate_project_branch(branch_test_file: Path):
    pass


@when("I run 'clowder herd' for <branch_test_file>")
def when_run_validate_branch_herd(tmp_path: Path, branch_test_file: str, command_results: CommandResults,
                                  scenario_info: ScenarioInfo) -> None:
    scenario_info.current_validation_test = branch_test_file
    command = "clowder herd"
    path = tmp_path / branch_test_file
    result = util.run_command(command, path)
    command_results.completed_processes.append(result)


@given("validation clowders are initialized")
def given__validation_initialized(tmp_path: Path, scenario_info: ScenarioInfo,
                                  validate_projects_init: Tuple[Path]) -> None:
    pass


@given(parsers.parse("for validation clowders: directory {directory} doesn't exist"))
def given_validation_has_no_directory(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    assert not path.exists()


@fixture
def validate_projects_init(tmp_path: Path, validate_projects_init_session: Path) -> None:
    util.copy_directory(validate_projects_init_session, to=tmp_path)
    # TODO: Remove once clowder.yml is relative symlink
    for test in branch_tests:
        result = util.run_command("clowder link", tmp_path / test[0])
        assert result.returncode == 0


@fixture(scope="session")
def validate_projects_init_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(validate_projects_init_session.__name__)
    return util.create_yaml_validation_clowders(path)


@then(parsers.parse("for validation clowders: project at {directory} has tracking branch {branch}"))
def then_validation_directory_has_tracking_branch(tmp_path: Path, directory: str, branch: str,
                                                  scenario_info: ScenarioInfo) -> None:
    path = tmp_path / scenario_info.current_validation_test / directory
    assert util.tracking_branch_exists(path, branch)


@then(parsers.parse("for validation clowders: project at {directory} is a git repository"))
def then_validation_project_dir_is_git_repo(tmp_path: Path, directory: str,
                                            scenario_info: ScenarioInfo) -> None:
    path = tmp_path / scenario_info.current_validation_test / directory
    assert path.exists()
    assert path.is_dir()
    assert util.has_git_directory(path)


@then(parsers.parse("for validation clowders: project at {directory} is on branch {branch}"))
def then_validation_directory_on_branch(tmp_path: Path, directory: str, branch: str,
                                        scenario_info: ScenarioInfo) -> None:
    path = tmp_path / scenario_info.current_validation_test / directory
    assert util.is_on_active_branch(path, branch)
