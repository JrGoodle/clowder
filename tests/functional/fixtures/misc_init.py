"""
This module contains fixtures
"""

from pathlib import Path

from pytest import fixture

import clowder.util.filesystem as fs

import tests.functional.util as util


@fixture
def misc_init(tmp_path: Path, misc_init_session: Path) -> None:
    fs.copy_directory(misc_init_session, to_path=tmp_path)


@fixture(scope="session")
def misc_init_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(misc_init_session.__name__)
    return util.init_clowder(path, "misc")
