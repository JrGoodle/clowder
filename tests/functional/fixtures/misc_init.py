"""
This module contains fixtures
"""

import os
from pathlib import Path

from pytest import fixture

import tests.functional.util as util


@fixture
def misc_init(tmp_path: Path, misc_init_session: Path) -> None:
    util.copy_directory(misc_init_session, to=tmp_path)


@fixture(scope="session")
def misc_init_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(misc_init_session.__name__)
    return util.init_clowder(path, "misc")
