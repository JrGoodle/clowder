"""
This module contains fixtures
"""

import os
from pathlib import Path

from pytest import fixture

import tests.functional.util as util
from tests.functional.util import ScenarioInfo


@fixture
def misc_init_herd(tmp_path: Path, misc_init_herd_session: Path, scenario_info: ScenarioInfo) -> None:
    util.copy_directory(misc_init_herd_session, to=tmp_path)
    # TODO: Remove once clowder.yml is relative symlink
    symlink = util.valid_clowder_symlink(tmp_path)
    os.unlink(symlink)
    result = util.run_command("clowder link", tmp_path)
    assert result.returncode == 0


@fixture(scope="session")
def misc_init_herd_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(misc_init_herd_session.__name__)
    return util.init_herd_clowder(path, "misc")


@fixture
def misc_init_herd_version_https(tmp_path: Path, misc_init_herd_version_https_session: Path) -> None:
    util.copy_directory(misc_init_herd_version_https_session, to=tmp_path)
    # TODO: Remove once clowder.yml is relative symlink
    symlink = util.valid_clowder_symlink(tmp_path)
    os.unlink(symlink)
    result = util.run_command("clowder link https", tmp_path)
    assert result.returncode == 0


@fixture(scope="session")
def misc_init_herd_version_https_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(misc_init_herd_version_https_session.__name__)
    return util.init_herd_clowder(path, "misc", version="https")
