"""
This module contains fixtures
"""

import shutil
from pathlib import Path

# noinspection PyPackageRequirements
import pytest

import tests.functional.common as common


# https://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth
@pytest.fixture
def cats_init_herd_default(tmp_path: Path, clone_clowder_cats_init_herd_default) -> None:
    snapshot = clone_clowder_cats_init_herd_default
    shutil.copytree(snapshot, tmp_path, symlinks=True, dirs_exist_ok=True)


@pytest.fixture(scope="session")
def clone_clowder_cats_init_herd_default(tmp_path_factory) -> Path:
    name = "clowder_cats_init_herd_default"
    tmp_path = tmp_path_factory.mktemp(name)

    command = f"clowder init {common.get_url('cats', 'https')}"
    common.run_command(command, tmp_path)
    command = "clowder herd"
    common.run_command(command, tmp_path)

    clowder_repo = tmp_path / ".clowder"
    assert clowder_repo.exists()
    assert clowder_repo.is_dir()
    assert not common.is_directory_empty(clowder_repo)
    assert common.valid_clowder_symlink(tmp_path) is not None

    for example, repo in common.CATS_REPOS_DEFAULT.items():
        path = tmp_path / repo["path"]
        branch = repo["branch"]
        assert path.exists()
        assert path.is_dir()
        assert common.has_git_directory(path)
        assert common.is_on_active_branch(path, branch)
        assert not common.is_dirty(path)

    return tmp_path
