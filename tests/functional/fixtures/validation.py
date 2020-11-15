"""
This module contains fixtures
"""

from pathlib import Path

from pytest import fixture

import tests.functional.util as util
from tests.functional.util import ScenarioInfo


@fixture
def validation_init(tmp_path: Path, validation_init_session: Path, scenario_info: ScenarioInfo) -> None:
    path = validation_init_session / scenario_info.current_validation_test
    util.copy_directory(path, to=tmp_path)
    util.run_command("clowder link", tmp_path, check=True)


@fixture(scope="session")
def validation_init_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(validation_init_session.__name__)
    return util.create_yaml_validation_clowders(path)


@fixture
def validation_init_herd(tmp_path: Path, validation_init_session: Path,
                         scenario_info: ScenarioInfo) -> None:
    path = validation_init_session / scenario_info.current_validation_test
    util.copy_directory(path, to=tmp_path)
    util.run_command("clowder link", tmp_path, check=True)
    util.run_command("clowder herd", tmp_path, check=True)
