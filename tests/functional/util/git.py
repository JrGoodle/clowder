"""New syntax test file"""

import copy
from typing import List, Optional

from subprocess import CompletedProcess
from pathlib import Path

from git import Repo
from .command import run_command
from .file_system import create_file, is_directory_empty
from .scenario_info import ScenarioInfo


def is_dirty(path: Path) -> bool:
    """Check whether repo is dirty

    :return: True, if repo is dirty
    :rtype: bool
    """

    repo = Repo(path)
    return repo.is_dirty() or is_rebase_in_progress(path) or has_untracked_files(path)


def is_rebase_in_progress(path: Path) -> bool:
    rebase_merge = path / ".git" / "rebase-merge"
    rebase_apply = path / ".git" / "rebase-apply"
    rebase_merge_exists = rebase_merge.exists() and rebase_merge.is_dir()
    rebase_apply_exists = rebase_apply.exists() and rebase_apply.is_dir()
    return rebase_merge_exists or rebase_apply_exists


def has_untracked_files(path: Path) -> bool:
    """Check whether untracked files exist

    :return: True, if untracked files exist
    :rtype: bool
    """
    repo = Repo(path)
    return True if repo.untracked_files else False


def git_add_file(path: Path, file: str) -> None:
    repo = Repo(path)
    assert repo.untracked_files
    repo.git.add(file)
    assert repo.index.diff("HEAD")


def has_untracked_file(path: Path, filename: str) -> bool:
    repo = Repo(path)
    return filename in repo.untracked_files


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


def get_branch_commit_sha(path: Path, branch: str, remote: Optional[str] = None) -> str:
    if remote is not None:
        result = run_command(f"git rev-parse {remote}/{branch}", path)
    else:
        result = run_command(f"git rev-parse {branch}", path)
    assert result.returncode == 0
    stdout: str = result.stdout
    return stdout.strip()


def create_number_commits(path: Path, count: int, filename: str, contents: str) -> List[CompletedProcess]:
    commits = copy.copy(count)
    results = []
    while commits > 0:
        result = create_commit(path, f"{commits}_{filename}", contents)
        results += result
        commits -= 1
    assert all([r.returncode == 0 for r in results])
    return results


def create_commit(path: Path, filename: str, contents: str) -> List[CompletedProcess]:
    previous_commit = current_head_commit_sha(path)
    create_file(path / filename, contents)
    results = []
    result = run_command(f"git add {filename}", path)
    results.append(result)
    result = run_command(f"git commit -m 'Add {filename}'", path)
    results.append(result)
    new_commit = current_head_commit_sha(path)
    assert previous_commit != new_commit
    assert all([r.returncode == 0 for r in results])
    return results


def create_local_branch(path: Path, branch: str) -> CompletedProcess:
    result = run_command(f"git branch {branch} HEAD", path)
    assert local_branch_exists(path, branch)
    return result


def delete_local_branch(path: Path, branch: str) -> CompletedProcess:
    result = run_command(f"git branch -d {branch}", path)
    assert not local_branch_exists(path, branch)
    return result


def create_remote_branch(path: Path, branch: str, remote: str = "origin") -> List[CompletedProcess]:
    results = []
    result = create_local_branch(path, branch)
    results.append(result)
    result = run_command(f"git push {remote} {branch}", path)
    results.append(result)
    result = delete_local_branch(path, branch)
    results.append(result)
    assert not local_branch_exists(path, branch)
    assert remote_branch_exists(path, branch, remote)
    return results


def delete_remote_branch(path: Path, branch: str, remote: str = "origin") -> CompletedProcess:
    result = run_command(f"git push {remote} --delete {branch}", path)
    assert not remote_branch_exists(path, branch)
    return result


def create_tracking_branch(path: Path, branch: str, remote: str = "origin") -> List[CompletedProcess]:
    results = []
    result = create_local_branch(path, branch)
    results.append(result)
    result = run_command(f"git push -u {remote} {branch}", path)
    results.append(result)
    assert local_branch_exists(path, branch)
    assert remote_branch_exists(path, branch)
    assert tracking_branch_exists(path, branch)
    return results


def checkout_branch(path: Path, branch: str) -> CompletedProcess:
    result = run_command(f"git checkout {branch}", path)
    assert is_on_active_branch(path, branch)
    return result


def local_branch_exists(path: Path, branch: str) -> bool:
    result = run_command(f"git rev-parse --quiet --verify refs/heads/{branch}", path)
    return result.returncode == 0


def remote_branch_exists(path: Path, branch: str, remote: str = "origin") -> bool:
    result = run_command(f"git ls-remote --heads {remote} {branch} | wc -l | tr -d '[:space:]'", path)
    output: str = result.stdout
    return output.strip() == "1"


def tracking_branch_exists(path: Path, branch: str) -> bool:
    result = run_command(f'git config --get branch.{branch}.merge', path)
    return result.returncode == 0


def check_remote_url(path: Path, remote, url) -> None:
    result = run_command(f"git remote get-url {remote}", path)
    assert result.stdout == url


def is_on_active_branch(path: Path, branch: str) -> bool:
    repo = Repo(path)
    active_branch = repo.active_branch.name
    print(f"TEST: active branch '{active_branch}' is '{branch}'")
    return active_branch == branch


def is_detached_head(path: Path) -> bool:
    repo = Repo(path)
    return repo.head.is_detached


def create_detached_head(path: Path, branch: str) -> None:
    repo = Repo(path)
    repo.git.checkout(f"{branch}~1")
    assert is_detached_head(path)


def is_on_tag(path: Path, tag: str) -> bool:
    repo = Repo(path)
    has_tag = tag in repo.tags
    if not has_tag:
        return False
    on_correct_commit = repo.head.commit == repo.tags[tag].commit
    return on_correct_commit


def is_on_commit(path: Path, commit: str) -> bool:
    repo = Repo(path)
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
    return number_commits_ahead(path, start, end) == number_commits


def is_behind_by_number_commits(path: Path, start: str, end: str, number_commits: int) -> bool:
    return number_commits_behind(path, start, end) == number_commits


def number_commits_ahead(path: Path, start: str, end: str) -> int:
    return number_of_commits_between_refs(path, end, start)


def number_commits_behind(path: Path, start: str, end: str) -> int:
    return number_of_commits_between_refs(path, start, end)


def push_to_remote_branch(path: Path, branch: str, remote: str = "origin") -> None:
    repo = Repo(path)
    repo.git.push(remote, f"refs/heads/{branch}:refs/heads/{branch}")


def force_push_to_remote_branch(path: Path, branch: str, remote: str = "origin") -> None:
    repo = Repo(path)
    repo.git.push(remote, f"refs/heads/{branch}:refs/heads/{branch}", force=True)


def abort_rebase(path: Path) -> None:
    repo = Repo(path)
    repo.git.rebase(abort=True)


def get_commit_messages_behind(path: Path, ref: str, count: int = 1) -> List[str]:
    results = []
    commit = 0
    while commit < count:
        result = get_commit_message(path, f"{ref}~{commit}")
        results.append(result)
        commit += 1
    return results


def get_commit_message(path: Path, ref: str) -> str:
    result = run_command(f"git log --format=%B -n 1 {ref}", path)
    assert result.returncode == 0
    return result.stdout


def set_up_behind_ahead_no_confilct(path: Path, local: str, remote: str, number_behind: int, number_ahead: int,
                                    scenario_info: ScenarioInfo) -> None:
    assert has_no_commits_between_refs(path, local, remote)
    reset_back_by_number_of_commits(path, number_behind)
    assert is_behind_by_number_commits(path, local, remote, number_behind)
    create_number_commits(path, number_ahead, "something.txt", "something")
    assert is_ahead_by_number_commits(path, local, remote, number_ahead)

    behind_messages = get_commit_messages_behind(path, remote, number_behind)
    scenario_info.commit_messages_behind = behind_messages
    scenario_info.number_commit_messages_behind = number_behind
    ahead_messages = get_commit_messages_behind(path, local, number_ahead)
    scenario_info.commit_messages_ahead = ahead_messages
    scenario_info.number_commit_messages_ahead = number_ahead


def set_up_behind_ahead_confilct(path: Path, branch: str, number_behind: int, number_ahead: int) -> None:
    beginning_remote_sha = get_branch_commit_sha(path, branch, "origin")
    beginning_sha = current_head_commit_sha(path)
    create_number_commits(path, number_behind, "something", "something")
    push_to_remote_branch(path, branch)
    reset_back_by_number_of_commits(path, number_behind)
    create_number_commits(path, number_ahead, "something", "something else")
    end_remote_sha = get_branch_commit_sha(path, branch, "origin")
    end_sha = current_head_commit_sha(path)
    assert beginning_sha != end_sha
    assert beginning_remote_sha != end_remote_sha


def set_up_behind(path: Path, local: str, remote: str, number_commits: int, ) -> None:
    create_number_commits(path, number_commits, "something.txt", "something")
    assert is_ahead_by_number_commits(path, local, remote, number_commits)


def set_up_ahead(path: Path, local: str, remote: str, number_commits: int, ) -> None:
    reset_back_by_number_of_commits(path, number_commits)
    assert is_behind_by_number_commits(path, local, remote, number_commits)
