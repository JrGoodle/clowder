"""New syntax test file"""

import os
import subprocess
from pathlib import Path

TEST_REPOS = {
    "cats": {"url": "github.com", "name": "JrGoodle/cats"},
    "misc": {"url": "github.com", "name": "JrGoodle/misc-clowder-tests"},
    "swift": {"url": "github.com", "name": "JrGoodle/swift-clowder"}
}


def is_dirty(repo) -> bool:
    """Check whether repo is dirty

    :return: True, if repo is dirty
    :rtype: bool
    """

    # if not self.repo_path.is_dir():
    #     return False

    return repo.is_dirty()  # or self._is_rebase_in_progress() or self._has_untracked_files()


def is_directory_empty(dir_name):
    if os.path.exists(dir_name) and os.path.isdir(dir_name):
        if not os.listdir(dir_name):
            print("Directory is empty")
            return True
        else:
            print("Directory is not empty")
            return False
    else:
        print("Given Directory don't exists")
        raise Exception


def has_git_directory(dir_name):
    path = Path(dir_name / ".git")
    return path.is_dir()


def create_file(path):
    with open(path, 'w') as f:
        pass
    assert path.exists()
    assert path.is_file()
    assert not path.is_dir()
    assert not path.is_symlink()


def run_command(command, path, exit_code=None):
    print(f"TEST: {command}")
    if exit_code is None:
        subprocess.run(command, shell=True, cwd=path, check=True)
        return
    result = subprocess.run(command, shell=True, cwd=path)
    assert result.returncode == exit_code


def get_url(example, protocol="ssh"):
    source_url = TEST_REPOS[example]["url"]
    name = TEST_REPOS[example]["name"]
    if protocol == "ssh":
        url = f"git@{source_url}:{name}.git"
    elif protocol == "https":
        url = f"https://{source_url}/{name}.git"
    else:
        raise Exception
    print(f"TEST: {url}")
    return url
