"""test_features"""

import pytest
from pathlib import Path
from pytest import fixture
from typing import List, Tuple

from pytest_bdd import given, scenario

import tests.functional.util as util
from tests.functional.util import yaml_property_tests, ScenarioInfo


branch_tests: List[Tuple[str]] = [(f,) for f in yaml_property_tests("project.branch")]


@pytest.mark.parametrize(["project_branch"], branch_tests)
@scenario(
    "../features/yaml_validation.feature",
    "validate project.branch",
)
def test_validate_project_branch(project_branch: Path):
    pass


@given("validating property <project_branch>")
def given_validate_project_branch(tmp_path: Path, project_branch: str, scenario_info: ScenarioInfo) -> None:
    scenario_info.current_validation_test = project_branch


@given("validation clowder is initialized")
def given_validation_initialized(tmp_path: Path, scenario_info: ScenarioInfo,
                                 validate_projects_init: Tuple[Path]) -> None:
    pass


@fixture
def validate_projects_init(tmp_path: Path, validate_projects_init_session: Path, scenario_info: ScenarioInfo) -> None:
    path = validate_projects_init_session / scenario_info.current_validation_test
    util.copy_directory(path, to=tmp_path)
    # TODO: Remove once clowder.yml is relative symlink
    result = util.run_command("clowder link", tmp_path)
    assert result.returncode == 0


@fixture(scope="session")
def validate_projects_init_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(validate_projects_init_session.__name__)
    return util.create_yaml_validation_clowders(path)
