"""New syntax test file"""

import copy
from typing import List

from subprocess import CompletedProcess
from pathlib import Path

from git import Repo
from .command import run_command
from .file_system import create_file, is_directory_empty


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


def git_add_file(path: Path, file: str) -> None:
    repo = Repo(path)
    assert repo.untracked_files
    repo.git.add(file)
    assert repo.index.diff("HEAD")


def has_untracked_file(path: Path, file_name: str) -> bool:
    repo = Repo(path)
    return file_name in repo.untracked_files


def has_git_directory(path: Path) -> bool:
    return Path(path / ".git").is_dir()


def is_submodule_initialized(path: Path) -> bool:
    git_path = Path(path / ".git")
    return path.is_dir() and git_path.exists() and git_path.is_file()


def is_submodule_placeholder(path: Path) -> bool:
    return path.is_dir() and is_directory_empty(path)


def has_submodule(repo_path: Path, submodule_path: Path) -> bool:
    repo = Repo(repo_path)
    submodules = repo.submodules
    for submodule in submodules:
        if submodule.name == submodule_path.stem and submodule.path == str(submodule_path):
            return True
    return False


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


def create_number_commits(path: Path, filename: str, count: int) -> List[CompletedProcess]:
    commits = copy.copy(count)
    results = []
    while commits > 0:
        result = create_commit(path, f"{commits}_{filename}")
        results += result
        commits -= 1
    assert all([r.returncode == 0 for r in results])
    return results


def create_commit(path: Path, filename: str) -> List[CompletedProcess]:
    previous_commit = current_head_commit_sha(path)
    create_file(path / filename)
    results = []
    result = run_command(f"git add {filename}", path)
    results.append(result)
    result = run_command(f"git commit -m 'Add {filename}'", path)
    results.append(result)
    new_commit = current_head_commit_sha(path)
    assert previous_commit != new_commit
    assert all([r.returncode == 0 for r in results])
    return results


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


def is_on_active_branch(path: Path, branch: str) -> bool:
    repo = Repo(str(path))
    active_branch = repo.active_branch.name
    print(f"TEST: active branch '{active_branch}' is '{branch}'")
    return active_branch == branch


def is_detached_head(path) -> bool:
    repo = Repo(str(path))
    return repo.head.is_detached


def is_on_tag(path: Path, tag: str) -> bool:
    repo = Repo(str(path))
    has_tag = tag in repo.tags
    if not has_tag:
        return False
    on_correct_commit = repo.head.commit == repo.tags[tag].commit
    return on_correct_commit


def is_on_commit(path: Path, commit: str) -> bool:
    repo = Repo(str(path))
    on_correct_commit = repo.head.commit.hexsha == commit
    return on_correct_commit


def number_of_commits_between_refs(path: Path, first: str, second: str) -> int:
    result = run_command(f"git rev-list {first}..{second} --count", path)
    stdout: str = result.stdout
    return int(stdout.strip())


def reset_back_by_number_of_commits(path: Path, number: int) -> CompletedProcess:
    sha = current_head_commit_sha(path)
    result = run_command(f"git reset --hard HEAD~{number}", path)
    assert number_of_commits_between_refs(path, "HEAD", sha) == number
    return result


def has_git_remote_with_url(path: Path, remote: str, url: str) -> bool:
    repo = Repo(path)
    if remote not in repo.remotes:
        return False
    remote_url = repo.remotes[remote].url
    return remote_url == url


def has_no_commits_between_refs(path: Path, start: str, end: str) -> bool:
    result_1 = number_of_commits_between_refs(path, start, end) == 0
    result_2 = number_of_commits_between_refs(path, end, start) == 0
    return result_1 and result_2


def is_ahead_by_number_commits(path: Path, start: str, end: str, number_commits: int) -> bool:
    result_1 = number_of_commits_between_refs(path, start, end) == 0
    result_2 = number_of_commits_between_refs(path, end, start) == number_commits
    return result_1 and result_2


def is_behind_by_number_commits(path: Path, start: str, end: str, number_commits: int) -> bool:
    result_1 = number_of_commits_between_refs(path, start, end) == number_commits
    result_2 = number_of_commits_between_refs(path, end, start) == 0
    return result_1 and result_2


def is_behind_ahead_by_number_commits(path: Path, start: str, end: str,
                                      number_commits_behind: int, number_commits_ahead: int) -> bool:
    result_1 = number_of_commits_between_refs(path, start, end) == number_commits_behind
    result_2 = number_of_commits_between_refs(path, end, start) == number_commits_ahead
    return result_1 and result_2
