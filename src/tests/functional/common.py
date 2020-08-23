"""New syntax test file"""

import os
import subprocess
from pathlib import Path

from git import Repo

TEST_REPOS = {
    "cats": {"url": "github.com", "name": "JrGoodle/cats"},
    "misc": {"url": "github.com", "name": "JrGoodle/misc-clowder-tests"},
    "swift": {"url": "github.com", "name": "JrGoodle/swift-clowder"}
}


def is_dirty(repo: Repo) -> bool:
    """Check whether repo is dirty

    :return: True, if repo is dirty
    :rtype: bool
    """

    return repo.is_dirty() or is_rebase_in_progress(repo.git_dir) or has_untracked_files(repo)


def is_rebase_in_progress(git_dir) -> bool:
    """Detect whether rebase is in progress

    :return: True, if rebase is in progress
    :rtype: bool
    """

    is_rebase_apply = Path(git_dir, 'rebase-apply').is_dir()
    is_rebase_merge = Path(git_dir, 'rebase-merge').is_dir()
    return is_rebase_apply or is_rebase_merge


def has_untracked_files(repo: Repo) -> bool:
    """Check whether untracked files exist

    :return: True, if untracked files exist
    :rtype: bool
    """

    return True if repo.untracked_files else False


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


def lfs_hooks_installed(path):
    result = run_command("grep -m 1 'git lfs pre-push' '.git/hooks/pre-push'", path)
    assert result.returncode == 0
    result = run_command("grep -m 1 'git lfs post-checkout' '.git/hooks/post-checkout'", path)
    assert result.returncode == 0
    result = run_command("grep -m 1 'git lfs post-commit' '.git/hooks/post-commit'", path)
    assert result.returncode == 0
    result = run_command("grep -m 1 'git lfs post-merge' '.git/hooks/post-merge'", path)
    assert result.returncode == 0


def lfs_filters_installed(path):
    result = run_command("git config --get filter.lfs.smudge", path)
    assert result.returncode == 0
    result = run_command("git config --get filter.lfs.smudge", path)
    assert result.returncode == 0
    result = run_command("git config --get filter.lfs.smudge", path)
    assert result.returncode == 0


def is_lfs_file_pointer(path, file):
    result = run_command(f'git lfs ls-files -I "{file}"', path, check=False)
    assert result.stdout == '-'


def is_lfs_file_not_pointer(path, file):
    result = run_command(f'git lfs ls-files -I "{file}"', path, check=False)
    assert result.stdout == '*'


def create_file(path):
    with open(path, 'w') as _:
        pass
    assert path.exists()
    assert path.is_file()
    assert not path.is_dir()
    assert not path.is_symlink()


def local_branch_exists(path: Path, branch: str):
    result = run_command(f'git rev-parse --quiet --verify "{branch}"', path, check=False)
    assert result.returncode == 0


def remote_branch_exists(path: Path, branch: str):
    result = run_command(f"git ls-remote --heads origin {branch} | wc -l | tr -d '[:space:]'", path)
    assert result.stdout != "0"


def tracking_branch_exists(path: Path, branch: str):
    result = run_command(f'git config --get branch.{branch}.merge', path, check=False)
    assert result.returncode == 0


def check_remote_url(path: Path, remote, url):
    result = run_command(f"git remote get-url {remote}", path)
    assert result.stdout == url


def rebase_in_progress(path: Path):
    rebase_merge = path / ".git" / "rebase-merge"
    rebase_apply = path / ".git" / "rebase-apply"
    assert rebase_merge.exists() or rebase_apply.exists()
    assert rebase_merge.is_dir() or rebase_apply.is_dir()


def no_rebase_in_progress(path: Path):
    rebase_merge = path / ".git/rebase-merge"
    rebase_apply = path / ".git/rebase-apply"
    assert not rebase_merge.exists() and not rebase_apply.exists()
    assert not rebase_merge.is_dir() and not rebase_apply.is_dir()


def run_command(command, path, check=True):
    print(f"TEST: {command}")
    return subprocess.run(command, shell=True, cwd=path, check=check)


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
