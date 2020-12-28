"""New syntax test file"""

import shutil
from pathlib import Path
from typing import Dict, List, Optional

import pygoodle.filesystem as fs
from pygoodle.git import Repo

from .command import run_command


TestRepoInfo = Dict[str, Dict[str, str]]

TEST_REPOS: TestRepoInfo = {
    "cats": {"url": "github.com", "name": "JrGoodle/cats"},
    "misc": {"url": "github.com", "name": "JrGoodle/misc-clowder-tests"},
    "swift": {"url": "github.com", "name": "JrGoodle/swift-clowder"}
}

CATS_REPOS_DEFAULT: TestRepoInfo = {
    "mu": {"path": "mu", "branch": "knead"},
    "duke": {"path": "duke", "branch": "purr"},
    "kit": {"path": "black-cats/kit", "branch": "master"},
    "kishka": {"path": "black-cats/kishka", "branch": "master"},
    "sasha": {"path": "black-cats/sasha", "branch": "master"},
    "june": {"path": "black-cats/june", "branch": "master"}
}

MISC_REPOS_DEFAULT: TestRepoInfo = {
    "djinni": {"path": "djinni", "branch": "master"},
    "gyp": {"path": "gyp", "branch": "fork-branch"},
    "sox": {"path": "sox", "branch": "master"}
}

# TODO: Add project info
SWIFT_REPOS_DEFAULT: TestRepoInfo = {}


def example_repo_dirs(example: str) -> List[str]:
    if example == "cats":
        return [info["path"] for name, info in CATS_REPOS_DEFAULT.items()]
    elif example == "misc":
        return [info["path"] for name, info in MISC_REPOS_DEFAULT.items()]
    elif example == "swift":
        return [info["path"] for name, info in SWIFT_REPOS_DEFAULT.items()]
    else:
        assert False


def example_repo_projects(example: str) -> List[Dict[str, str]]:
    if example == "cats":
        return [info for name, info in CATS_REPOS_DEFAULT.items()]
    elif example == "misc":
        return [info for name, info in MISC_REPOS_DEFAULT.items()]
    elif example == "swift":
        return [info for name, info in SWIFT_REPOS_DEFAULT.items()]
    else:
        assert False


def get_url(example: str, protocol: str = "https") -> str:
    source_url = TEST_REPOS[example]["url"]
    name = TEST_REPOS[example]["name"]
    if protocol == "ssh":
        url = f"git@{source_url}:{name}.git"
    elif protocol == "https":
        url = f"https://{source_url}/{name}.git"
    else:
        raise Exception
    print(f"url: {url}")
    return url


def validate_clowder_repo_with_symlink(clowder_repo: Path) -> None:
    repo = Repo(clowder_repo)
    assert repo.exists
    assert valid_clowder_symlink(clowder_repo.parent) is not None


def create_non_symlink_clowder_yml(path: Path, example: str, protocol: str = "https",
                                   branch: Optional[str] = None, version: Optional[str] = None) -> Path:
    path = init_clowder(path, example, protocol=protocol, branch=branch, version=version)
    symlink = valid_clowder_symlink(path)
    file = symlink.resolve()
    symlink.unlink()
    shutil.copy(file, path)
    clowder_repo = path / ".clowder"
    fs.remove_dir(clowder_repo)
    assert not clowder_repo.exists()
    return path


def init_clowder(path: Path, example: str, protocol: str = "https",
                 branch: Optional[str] = None, version: Optional[str] = None) -> Path:

    if branch is not None:
        run_command(f"clowder init {get_url(example, protocol)} -b {branch}", path, check=True)
    else:
        run_command(f"clowder init {get_url(example, protocol)}", path, check=True)

    if version is not None:
        run_command(f"clowder link {version}", path, check=True)
        assert has_valid_clowder_symlink_version(path, version)
    else:
        assert has_valid_clowder_symlink_default(path)

    validate_clowder_repo_with_symlink(path / ".clowder")

    repos = example_repo_projects(example)
    for repo in repos:
        repo_path = path / repo["path"]
        assert not repo_path.exists()

    return path


def init_herd_clowder(path: Path, example: str, protocol: str = "https",
                      branch: Optional[str] = None, version: Optional[str] = None) -> Path:

    if branch is not None:
        run_command(f"clowder init {get_url(example, protocol)} -b {branch}", path, check=True)
    else:
        run_command(f"clowder init {get_url(example, protocol)}", path, check=True)

    if version is not None:
        run_command(f"clowder link {version}", path, check=True)
        has_valid_clowder_symlink_version(path, version)

    run_command("clowder herd", path, check=True)

    validate_clowder_repo_with_symlink(path / ".clowder")

    repos = example_repo_projects(example)
    for repo in repos:
        repo_path = path / repo["path"]
        branch = repo["branch"]
        git_repo = Repo(repo_path)
        assert git_repo.exists
        assert git_repo.current_branch == branch
        assert not git_repo.is_dirty
        ssh_version = True if version is not None and "ssh" in version else False
        if protocol == "ssh" or ssh_version:
            remote_branches = git_repo.remote_branches
            remote_branches = [b for b in remote_branches if b.name.startswith('pytest')]
            for remote_branch in remote_branches:
                remote_branch.delete()
    return path


def has_valid_clowder_symlink_version(path: Path, version: str) -> bool:
    symlink = valid_clowder_symlink(path)
    if symlink is None:
        return False

    version_path = f".clowder/versions/{version}.{symlink.stem}{symlink.suffix}"
    return fs.is_relative_symlink_from_to(symlink, version_path)


def has_valid_clowder_symlink_default(path: Path) -> bool:
    symlink = valid_clowder_symlink(path)
    if symlink is None:
        return False

    destination_path = f"{symlink.stem}{symlink.suffix}"
    return fs.is_relative_symlink_from_to(symlink, destination_path)


def has_clowder_version(path: Path, version: str) -> bool:
    for suffix in ["yaml", "yml"]:
        version_path = path / ".clowder" / "versions" / f"{version}.clowder.{suffix}"
        if version_path.exists():
            return True
    return False


def valid_clowder_symlink(path: Path) -> Optional[Path]:
    yaml = valid_clowder_yaml_symlink(path)
    yml = valid_clowder_yml_symlink(path)
    if yaml is not None:
        return yaml
    if yml is not None:
        return yml
    return None


def valid_clowder_yaml_symlink(path: Path) -> Optional[Path]:
    yaml = path / "clowder.yaml"
    if yaml.is_symlink() and yaml.exists():
        return yaml
    return None


def valid_clowder_yml_symlink(path: Path) -> Optional[Path]:
    yml = path / "clowder.yml"
    if yml.is_symlink() and yml.exists():
        return yml
    return None


def has_clowder_yaml_file_or_symlink(path: Path) -> bool:
    yaml = Path(path / "clowder.yaml").exists()
    yml = Path(path / "clowder.yml").exists()
    return yaml or yml


def has_clowder_yaml_file(path: Path) -> bool:
    yaml = path / "clowder.yaml"
    yml = path / "clowder.yml"
    yaml_exists = yaml.exists() and not yaml.is_dir() and not yaml.is_symlink()
    yml_exists = yml.exists() and not yml.is_dir() and not yml.is_symlink()
    return yaml_exists or yml_exists
