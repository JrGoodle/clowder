"""New syntax test file"""

from pathlib import Path
from typing import Tuple

from pytest_bdd import given

from tests.functional.util import ScenarioInfo


@given("validation clowder is initialized")
def given_validation_initialized(tmp_path: Path, scenario_info: ScenarioInfo,
                                 validate_projects_init: Tuple[Path]) -> None:
    pass


@given("validation clowder is initialized and herded")
def given_validation_initialized_herded(tmp_path: Path, scenario_info: ScenarioInfo,
                                        validate_projects_init_herd: Tuple[Path]) -> None:
    pass


@given("validating property <project_implicit>")
def given_validate_project_implicit(tmp_path: Path, project_implicit: str, scenario_info: ScenarioInfo) -> None:
    scenario_info.current_validation_test = project_implicit


@given("validating property <project_branch>")
def given_validate_project_branch(tmp_path: Path, project_branch: str, scenario_info: ScenarioInfo) -> None:
    scenario_info.current_validation_test = project_branch


@given("validating property <project_commit>")
def given_validate_project_commit(tmp_path: Path, project_commit: str, scenario_info: ScenarioInfo) -> None:
    scenario_info.current_validation_test = project_commit


@given("validating property <project_git_config>")
def given_validate_project_git_config(tmp_path: Path, project_git_config: str, scenario_info: ScenarioInfo) -> None:
    scenario_info.current_validation_test = project_git_config


@given("validating property <project_git_depth>")
def given_validate_project_git_depth(tmp_path: Path, project_git_depth: str, scenario_info: ScenarioInfo) -> None:
    scenario_info.current_validation_test = project_git_depth


@given("validating property <project_git_lfs>")
def given_validate_project_git_lfs(tmp_path: Path, project_git_lfs: str, scenario_info: ScenarioInfo) -> None:
    scenario_info.current_validation_test = project_git_lfs


@given("validating property <project_git_submodules>")
def given_validate_project_git_submodules(tmp_path: Path, project_git_submodules: str,
                                          scenario_info: ScenarioInfo) -> None:
    scenario_info.current_validation_test = project_git_submodules


@given("validating property <project_groups>")
def given_validate_project_groups(tmp_path: Path, project_groups: str, scenario_info: ScenarioInfo) -> None:
    scenario_info.current_validation_test = project_groups


@given("validating property <project_path>")
def given_validate_project_path(tmp_path: Path, project_path: str, scenario_info: ScenarioInfo) -> None:
    scenario_info.current_validation_test = project_path


@given("validating property <project_remote>")
def given_validate_project_remote(tmp_path: Path, project_remote: str, scenario_info: ScenarioInfo) -> None:
    scenario_info.current_validation_test = project_remote


@given("validating property <project_source_protocol>")
def given_validate_project_source_protocol(tmp_path: Path, project_source_protocol: str,
                                           scenario_info: ScenarioInfo) -> None:
    scenario_info.current_validation_test = project_source_protocol


@given("validating property <project_source_url>")
def given_validate_project_source_url(tmp_path: Path, project_source_url: str,
                                      scenario_info: ScenarioInfo) -> None:
    scenario_info.current_validation_test = project_source_url


@given("validating property <project_tag>")
def given_validate_project_tag(tmp_path: Path, project_tag: str, scenario_info: ScenarioInfo) -> None:
    scenario_info.current_validation_test = project_tag
