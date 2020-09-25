"""New syntax test file"""

import shutil
from pathlib import Path
from typing import Dict, List, Optional

from git import Repo

from .command import run_command
from .file_system import is_relative_symlink_from_to
from .git import has_git_directory, is_dirty, is_on_active_branch


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
    print(f"TEST: {url}")
    return url


def validate_clowder_repo_with_symlink(clowder_repo: Path) -> None:
    assert clowder_repo.exists()
    assert clowder_repo.is_dir()
    assert has_git_directory(clowder_repo)
    assert valid_clowder_symlink(clowder_repo.parent) is not None


def create_non_symlink_clowder_yml(path: Path, example: str, protocol: str = "https",
                                   branch: Optional[str] = None, version: Optional[str] = None) -> Path:
    path = init_clowder(path, example, protocol=protocol, branch=branch, version=version)
    symlink = valid_clowder_symlink(path)
    file = symlink.resolve()
    symlink.unlink()
    shutil.copy(file, path)
    clowder_repo = path / ".clowder"
    shutil.rmtree(clowder_repo)
    assert not clowder_repo.exists()
    return path


def init_clowder(path: Path, example: str, protocol: str = "https",
                 branch: Optional[str] = None, version: Optional[str] = None) -> Path:

    if branch is not None:
        result = run_command(f"clowder init {get_url(example, protocol)} -b {branch}", path)
        assert result.returncode == 0
    else:
        result = run_command(f"clowder init {get_url(example, protocol)}", path)
        assert result.returncode == 0

    if version is not None:
        result = run_command(f"clowder link {version}", path)
        assert result.returncode == 0
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
        result = run_command(f"clowder init {get_url(example, protocol)} -b {branch}", path)
        assert result.returncode == 0
    else:
        result = run_command(f"clowder init {get_url(example, protocol)}", path)
        assert result.returncode == 0

    if version is not None:
        result = run_command(f"clowder link {version}", path)
        assert result.returncode == 0
        has_valid_clowder_symlink_version(path, version)

    result = run_command("clowder herd", path)
    assert result.returncode == 0

    validate_clowder_repo_with_symlink(path / ".clowder")

    repos = example_repo_projects(example)
    for repo in repos:
        repo_path = path / repo["path"]
        branch = repo["branch"]
        assert repo_path.exists()
        assert repo_path.is_dir()
        assert has_git_directory(repo_path)
        assert is_on_active_branch(repo_path, branch)
        assert not is_dirty(repo_path)
        ssh_version = True if version is not None and "ssh" in version else False
        if protocol == "ssh" or ssh_version:
            git_repo = Repo(repo_path)
            origin = git_repo.remotes.origin
            refs = origin.refs
            for r in refs:
                head: str = r.remote_head.strip()
                if head.startswith("pytest"):
                    try:
                        origin.push(refspec=f':{head}', force=True)
                    except Exception as err:
                        print(err)
                        pass

    return path


def has_valid_clowder_symlink_version(path: Path, version: str) -> bool:
    symlink = valid_clowder_symlink(path)
    if symlink is None:
        return False

    version_path = f".clowder/versions/{version}.{symlink.stem}{symlink.suffix}"
    return is_relative_symlink_from_to(symlink, version_path)


def has_valid_clowder_symlink_default(path: Path) -> bool:
    symlink = valid_clowder_symlink(path)
    if symlink is None:
        return False

    destination_path = f"{symlink.stem}{symlink.suffix}"
    return is_relative_symlink_from_to(symlink, destination_path)


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
