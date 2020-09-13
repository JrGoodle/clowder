"""New syntax test file"""

from pathlib import Path
from typing import Tuple

from pytest_bdd import given

from tests.functional.util import ScenarioInfo


@given("validating property <project_branch>")
def given_validate_project_branch(tmp_path: Path, project_branch: str, scenario_info: ScenarioInfo) -> None:
    scenario_info.current_validation_test = project_branch


@given("validation clowder is initialized")
def given_validation_initialized(tmp_path: Path, scenario_info: ScenarioInfo,
                                 validate_projects_init: Tuple[Path]) -> None:
    pass


@given("validation clowder is initialized and herded")
def given_validation_initialized(tmp_path: Path, scenario_info: ScenarioInfo,
                                 validate_projects_init_herd: Tuple[Path]) -> None:
    pass
