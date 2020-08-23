"""New syntax test file"""

from typing import Optional

import os
import subprocess
from subprocess import CompletedProcess
from pathlib import Path

from git import Repo

TEST_REPOS = {
    "cats": {"url": "github.com", "name": "JrGoodle/cats"},
    "misc": {"url": "github.com", "name": "JrGoodle/misc-clowder-tests"},
    "swift": {"url": "github.com", "name": "JrGoodle/swift-clowder"}
}

CATS_REPOS_DEFAULT = {
    "mu": {"path": "mu", "branch": "knead"},
    "duke": {"path": "duke", "branch": "purr"},
    "kit": {"path": "black-cats/kit", "branch": "master"},
    "kishka": {"path": "black-cats/kishka", "branch": "master"},
    "sasha": {"path": "black-cats/sasha", "branch": "master"},
    "june": {"path": "black-cats/june", "branch": "master"}
}


def is_dirty(path: Path) -> bool:
    """Check whether repo is dirty

    :return: True, if repo is dirty
    :rtype: bool
    """

    repo = Repo(str(path))
    return repo.is_dirty() or is_rebase_in_progress(repo.git_dir) or has_untracked_files(repo)


def is_rebase_in_progress(git_dir: Path) -> bool:
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


def is_directory_empty(path: Path) -> bool:
    if path.exists() and path.is_dir():
        if not os.listdir(path):
            print("Directory is empty")
            return True
        else:
            print("Directory is not empty")
            return False
    else:
        print("Given Directory don't exists")
        raise Exception


def has_git_directory(path: Path) -> bool:
    return Path(path / ".git").is_dir()


def lfs_hooks_installed(path: Path) -> None:
    result = run_command("grep -m 1 'git lfs pre-push' '.git/hooks/pre-push'", path)
    assert result.returncode == 0
    result = run_command("grep -m 1 'git lfs post-checkout' '.git/hooks/post-checkout'", path)
    assert result.returncode == 0
    result = run_command("grep -m 1 'git lfs post-commit' '.git/hooks/post-commit'", path)
    assert result.returncode == 0
    result = run_command("grep -m 1 'git lfs post-merge' '.git/hooks/post-merge'", path)
    assert result.returncode == 0


def lfs_filters_installed(path: Path) -> None:
    result = run_command("git config --get filter.lfs.smudge", path)
    assert result.returncode == 0
    result = run_command("git config --get filter.lfs.smudge", path)
    assert result.returncode == 0
    result = run_command("git config --get filter.lfs.smudge", path)
    assert result.returncode == 0


def is_lfs_file_pointer(path: Path, file: str) -> None:
    result = run_command(f'git lfs ls-files -I "{file}"', path, check=False)
    assert result.stdout == '-'


def is_lfs_file_not_pointer(path: Path, file: str) -> None:
    result = run_command(f'git lfs ls-files -I "{file}"', path, check=False)
    assert result.stdout == '*'


def create_file(path: Path) -> None:
    with open(path, 'w') as _:
        pass
    assert path.exists()
    assert path.is_file()
    assert not path.is_dir()
    assert not path.is_symlink()


def local_branch_exists(path: Path, branch: str) -> None:
    result = run_command(f'git rev-parse --quiet --verify "{branch}"', path, check=False)
    assert result.returncode == 0


def remote_branch_exists(path: Path, branch: str) -> None:
    result = run_command(f"git ls-remote --heads origin {branch} | wc -l | tr -d '[:space:]'", path)
    assert result.stdout != "0"


def tracking_branch_exists(path: Path, branch: str) -> None:
    result = run_command(f'git config --get branch.{branch}.merge', path, check=False)
    assert result.returncode == 0


def check_remote_url(path: Path, remote, url) -> None:
    result = run_command(f"git remote get-url {remote}", path)
    assert result.stdout == url


def rebase_in_progress(path: Path) -> None:
    rebase_merge = path / ".git" / "rebase-merge"
    rebase_apply = path / ".git" / "rebase-apply"
    assert rebase_merge.exists() or rebase_apply.exists()
    assert rebase_merge.is_dir() or rebase_apply.is_dir()


def run_command(command: str, path: Path, check: bool = True) -> CompletedProcess:
    print(f"TEST: {command}")
    return subprocess.run(command, shell=True, cwd=path, check=check)


def get_url(example: str, protocol: str = "ssh") -> str:
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


def is_on_active_branch(path: Path, branch: str) -> bool:
    repo = Repo(str(path))
    active_branch = repo.active_branch.name
    print(f"TEST: active branch '{active_branch}' is '{branch}'")
    return active_branch == branch


def is_detached_head_on_tag(path: Path, tag: str) -> bool:
    repo = Repo(str(path))
    has_tag = tag in repo.tags
    on_correct_commit = repo.head.commit == repo.tags[tag].commit
    return repo.head.is_detached and has_tag and on_correct_commit


def is_detached_head_on_commit(path: Path, commit: str) -> bool:
    repo = Repo(str(path))
    on_correct_commit = repo.head.commit.hexsha == commit
    return repo.head.is_detached and on_correct_commit


def valid_clowder_symlink(path: Path) -> Optional[Path]:
    yaml = path / "clowder.yaml"
    yml = path / "clowder.yml"
    if is_valid_symlink(yaml):
        return yaml
    if is_valid_symlink(yml):
        return yml
    return None


def is_valid_symlink(path: Path) -> bool:
    return path.is_symlink() and path.exists() and path.is_file()


def is_symlink_from_to(symlink: Path, destination: Path) -> bool:
    return is_valid_symlink(symlink) and destination.samefile(symlink.resolve())


def has_valid_clowder_version_symlink(path: Path, version: str) -> bool:
    symlink = valid_clowder_symlink(path)
    if symlink is None:
        return False

    version_path = path / ".clowder" / "versions" / f"{version}.{symlink.stem}{symlink.suffix}"
    return is_symlink_from_to(symlink, version_path)
