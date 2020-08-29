"""
This module contains fixtures
"""

import os
from pathlib import Path

# noinspection PyPackageRequirements
from pytest import fixture

import tests.functional.util.util as util
from tests.functional.util.util import TestInfo


@fixture
def misc_init_herd(tmp_path: Path, misc_init_herd_session: Path, test_info: TestInfo) -> None:
    util.copy_directory(misc_init_herd_session, to=tmp_path)
    # TODO: Remove once clowder.yml is relative symlink
    symlink = util.valid_clowder_symlink(tmp_path)
    os.unlink(symlink)
    util.run_command("clowder link", tmp_path, check=True)


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
    util.run_command("clowder link https", tmp_path, check=True)


@fixture(scope="session")
def misc_init_herd_version_https_session(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp(misc_init_herd_version_https_session.__name__)
    return util.init_herd_clowder(path, "misc", version="https")
