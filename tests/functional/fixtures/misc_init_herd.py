"""
This module contains fixtures
"""

from pathlib import Path

from pytest import fixture

import clowder.util.filesystem as fs

import tests.functional.util as util
from tests.functional.util import ScenarioInfo


@fixture
def misc_init_herd(tmp_path: Path, misc_init_herd_session: Path, scenario_info: ScenarioInfo) -> None:
    fs.copy_directory(misc_init_herd_session, to_path=tmp_path)


@fixture(scope="session")
def misc_init_herd_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(misc_init_herd_session.__name__)
    return util.init_herd_clowder(path, "misc")


@fixture
def misc_init_herd_version_https(tmp_path: Path, misc_init_herd_version_https_session: Path) -> None:
    fs.copy_directory(misc_init_herd_version_https_session, to_path=tmp_path)


@fixture(scope="session")
def misc_init_herd_version_https_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(misc_init_herd_version_https_session.__name__)
    return util.init_herd_clowder(path, "misc", version="https")
