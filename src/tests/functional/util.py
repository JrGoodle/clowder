"""New syntax test file"""

from typing import Dict, List, Optional

import os
import shutil
import subprocess
from subprocess import CompletedProcess, STDOUT, PIPE
from pathlib import Path

from git import Repo
from parse_type import TypeBuilder

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


def parse_string(text) -> str:
    return str(text)


list_str_commas = TypeBuilder.with_many(parse_string, listsep=",")
list_str_newlines = TypeBuilder.with_many(parse_string, listsep="\n")


def list_from_string(text: str, sep: Optional[str] = None) -> List[str]:
    return text.split(sep=sep)


class CommandResults:
    def __init__(self):
        self.completed_processes: List[CompletedProcess] = []


class TestInfo:
    def __init__(self):
        self.example: Optional[str] = None
        self.branch: Optional[str] = None
        self.protocol: str = "https"
        self.version: Optional[str] = None


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
    run_command("grep -m 1 'git lfs pre-push' '.git/hooks/pre-push'", path)
    run_command("grep -m 1 'git lfs post-checkout' '.git/hooks/post-checkout'", path)
    run_command("grep -m 1 'git lfs post-commit' '.git/hooks/post-commit'", path)
    run_command("grep -m 1 'git lfs post-merge' '.git/hooks/post-merge'", path)


def lfs_filters_installed(path: Path) -> None:
    result = run_command("git config --get filter.lfs.smudge", path)
    assert result.returncode == 0
    result = run_command("git config --get filter.lfs.smudge", path)
    assert result.returncode == 0
    result = run_command("git config --get filter.lfs.smudge", path)
    assert result.returncode == 0


def is_lfs_file_pointer(path: Path, file: str) -> None:
    result = run_command(f'git lfs ls-files -I "{file}"', path)
    assert result.stdout == '-'


def is_lfs_file_not_pointer(path: Path, file: str) -> None:
    result = run_command(f'git lfs ls-files -I "{file}"', path)
    assert result.stdout == '*'


def current_head_commit_sha(path: Path) -> str:
    result = run_command("git rev-parse HEAD", path)
    assert result.returncode == 0
    stdout: str = result.stdout
    return stdout.strip()


def create_file(path: Path) -> None:
    with open(path, 'w') as _:
        pass
    assert path.exists()
    assert path.is_file()
    assert not path.is_dir()
    assert not path.is_symlink()


def create_symlink(source: Path, target: Path) -> None:
    assert source.exists()
    assert not target.exists()
    os.symlink(source, target)
    assert is_symlink_from_to(target, source)


def create_commit(path: Path, filename: str) -> List[CompletedProcess]:
    previous_commit = current_head_commit_sha(path)
    create_file(path / filename)
    result_1 = run_command(f"git add {filename}", path)
    result_2 = run_command(f"git commit -m 'Add {filename}'", path)
    new_commit = current_head_commit_sha(path)
    assert previous_commit != new_commit
    return [result_1, result_2]


def create_branch(path: Path, branch: str) -> CompletedProcess:
    result = run_command(f"git branch {branch} HEAD", path)
    assert local_branch_exists(path, branch)
    return result


def checkout_branch(path: Path, branch: str) -> CompletedProcess:
    result = run_command(f"git checkout {branch}", path)
    assert is_on_active_branch(path, branch)
    return result


def local_branch_exists(path: Path, branch: str) -> bool:
    result = run_command(f'git rev-parse --quiet --verify "{branch}"', path)
    return result.returncode == 0


def remote_branch_exists(path: Path, branch: str) -> bool:
    git = Repo(path)
    if branch in git.remote().refs:
        return True
    return False


def tracking_branch_exists(path: Path, branch: str) -> bool:
    result = run_command(f'git config --get branch.{branch}.merge', path)
    return result.returncode == 0


def check_remote_url(path: Path, remote, url) -> None:
    result = run_command(f"git remote get-url {remote}", path)
    assert result.stdout == url


def rebase_in_progress(path: Path) -> None:
    rebase_merge = path / ".git" / "rebase-merge"
    rebase_apply = path / ".git" / "rebase-apply"
    assert rebase_merge.exists() or rebase_apply.exists()
    assert rebase_merge.is_dir() or rebase_apply.is_dir()


def run_command(command: str, path: Path, check: bool = False, clowder_debug: bool = True) -> CompletedProcess:
    print(f"TEST: {command}")
    cmd_env = os.environ.copy()
    if clowder_debug:
        cmd_env.update({"CLOWDER_DEBUG": "true"})
    else:
        cmd_env.pop('CLOWDER_DEBUG', None)
    # TODO: Replace universal_newlines with text when Python 3.6 support is dropped
    result = subprocess.run(command, cwd=path, shell=True, check=check,
                            stdout=PIPE, stderr=STDOUT, universal_newlines=True, env=cmd_env)
    print(result.stdout)
    return result


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


def has_clowder_yaml_file_or_symlink(path: Path) -> bool:
    yaml = Path(path / "clowder.yaml").exists()
    yml = Path(path / "clowder.yml").exists()
    return yaml or yml


def is_valid_symlink(path: Path) -> bool:
    return path.is_symlink() and path.exists() and path.is_file()


def is_symlink_from_to(symlink: Path, destination: Path) -> bool:
    return is_valid_symlink(symlink) and destination.samefile(symlink.resolve())


def has_valid_clowder_symlink_version(path: Path, version: str) -> bool:
    symlink = valid_clowder_symlink(path)
    if symlink is None:
        return False

    version_path = path / ".clowder" / "versions" / f"{version}.{symlink.stem}{symlink.suffix}"
    return is_symlink_from_to(symlink, version_path)


def has_valid_clowder_symlink_default(path: Path) -> bool:
    symlink = valid_clowder_symlink(path)
    if symlink is None:
        return False

    destination_path = path / f"{symlink.stem}{symlink.suffix}"
    return is_symlink_from_to(symlink, destination_path)


def has_clowder_version(path: Path, version: str) -> bool:
    for suffix in ["yaml", "yml"]:
        version_path = path / ".clowder" / "versions" / f"{version}.clowder.{suffix}"
        if version_path.exists():
            return True
    return False


def enable_network_connection() -> None:
    path = Path()
    from sys import platform
    if platform == "linux":
        run_command("nmcli nm enable true", path)
    elif platform == "darwin":
        run_command("networksetup -setairportpower airport on", path)
    elif platform == "win32":
        assert False


def disable_network_connection() -> None:
    path = Path()
    from sys import platform
    if platform == "linux":
        run_command("nmcli nm enable false", path)
    elif platform == "darwin":
        run_command("networksetup -setairportpower airport off", path)
    elif platform == "win32":
        assert False


def number_of_commits_between_refs(path: Path, first: str, second: str) -> int:
    result = run_command(f"git rev-list {first}..{second} --count", path)
    stdout: str = result.stdout
    return int(stdout.strip())


def reset_back_by_number_of_commits(path: Path, number: int) -> CompletedProcess:
    sha = current_head_commit_sha(path)
    result = run_command(f"git reset --hard HEAD~{number}", path)
    assert number_of_commits_between_refs(path, "HEAD", sha) == number
    return result


def init_clowder(path: Path, example: str, protocol: str = "https",
                 branch: Optional[str] = None, version: Optional[str] = None):

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
                      branch: Optional[str] = None, version: Optional[str] = None):

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
        assert repo_path.exists()
        assert repo_path.is_dir()
        assert has_git_directory(repo_path)
        assert is_on_active_branch(repo_path, branch)
        assert not is_dirty(repo_path)

    return path


def validate_clowder_repo_with_symlink(clowder_repo: Path) -> None:
    assert clowder_repo.exists()
    assert clowder_repo.is_dir()
    assert has_git_directory(clowder_repo)
    assert valid_clowder_symlink(clowder_repo.parent) is not None


def copy_directory(from_dir: Path, to: Path):
    # TODO: Replace rmdir() with copytree(dirs_exist_ok=True) when support for Python 3.7 is dropped
    to.rmdir()
    shutil.copytree(from_dir, to, symlinks=True)
