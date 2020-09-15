"""
This module contains fixtures
"""

from pathlib import Path

from pytest import fixture

import tests.functional.util as util
from tests.functional.util import ScenarioInfo


@fixture
def validate_projects_init(tmp_path: Path, validate_projects_init_session: Path, scenario_info: ScenarioInfo) -> None:
    path = validate_projects_init_session / scenario_info.current_validation_test
    util.copy_directory(path, to=tmp_path)
    result = util.run_command("clowder link", tmp_path)
    assert result.returncode == 0


@fixture(scope="session")
def validate_projects_init_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(validate_projects_init_session.__name__)
    return util.create_yaml_validation_clowders(path)


@fixture
def validate_projects_init_herd(tmp_path: Path, validate_projects_init_session: Path,
                                scenario_info: ScenarioInfo) -> None:
    path = validate_projects_init_session / scenario_info.current_validation_test
    util.copy_directory(path, to=tmp_path)
    result = util.run_command("clowder link", tmp_path)
    assert result.returncode == 0
    result = util.run_command("clowder herd", tmp_path)
    assert result.returncode == 0
