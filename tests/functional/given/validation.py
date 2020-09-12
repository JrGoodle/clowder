"""New syntax test file"""

from pathlib import Path

from pytest_bdd import given

from tests.functional.util import ScenarioInfo


@given("<project_property> validation clowders are initialized")
def given_project_property_validation_initialized(tmp_path: Path, project_property: str,
                                                  scenario_info: ScenarioInfo) -> None:
    assert False
