"""New syntax test file"""

import copy
from pathlib import Path
from subprocess import CompletedProcess
from typing import List

import pygoodle.filesystem as fs
from pygoodle.git import GitOffline, ORIGIN, Repo

from .command import run_command
from .scenario_info import ScenarioInfo


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
    repo = Repo(path)
    previous_commit = repo.current_commit()
    fs.create_file(path / filename, contents)
    results = []
    result = run_command(f"git add {filename}", path)
    results.append(result)
    result = run_command(f"git commit -m 'Add {filename}'", path)
    results.append(result)
    new_commit = repo.current_commit()
    assert previous_commit != new_commit
    assert all([r.returncode == 0 for r in results])
    return results


# def create_detached_head(path: Path, branch: str) -> None:
#     repo = Repo(path)
#     repo.checkout(f"{branch}~1")
#     assert repo.is_detached


def set_up_behind_ahead_no_confilct(path: Path, local: str, remote: str, number_behind: int, number_ahead: int,
                                    scenario_info: ScenarioInfo) -> None:
    assert GitOffline.has_no_commits_between_refs(path, local, remote)
    GitOffline.reset_back_by_number_of_commits(path, number_behind)
    assert GitOffline.is_behind_by_number_commits(path, local, remote, number_behind)
    create_number_commits(path, number_ahead, "something.txt", "something")
    assert GitOffline.is_ahead_by_number_commits(path, local, remote, number_ahead)

    behind_messages = GitOffline.get_commit_messages_behind(path, remote, number_behind)
    scenario_info.commit_messages_behind = behind_messages
    scenario_info.number_commit_messages_behind = number_behind
    ahead_messages = GitOffline.get_commit_messages_behind(path, local, number_ahead)
    scenario_info.commit_messages_ahead = ahead_messages
    scenario_info.number_commit_messages_ahead = number_ahead


def set_up_behind_ahead_conflict(path: Path, branch: str, number_behind: int, number_ahead: int) -> None:
    beginning_remote_sha = GitOffline.get_branch_commit_sha(path, branch, ORIGIN)
    repo = Repo(path)
    beginning_sha = repo.current_commit()
    create_number_commits(path, number_behind, "something", "something")
    repo.push(branch=branch)
    GitOffline.reset_back_by_number_of_commits(path, number_behind)
    create_number_commits(path, number_ahead, "something", "something else")
    end_remote_sha = GitOffline.get_branch_commit_sha(path, branch, ORIGIN)
    end_sha = repo.current_commit()
    assert beginning_sha != end_sha
    assert beginning_remote_sha != end_remote_sha


def set_up_behind(path: Path, local: str, remote: str, number_commits: int, ) -> None:
    create_number_commits(path, number_commits, "something.txt", "something")
    assert GitOffline.is_ahead_by_number_commits(path, local, remote, number_commits)


def set_up_ahead(path: Path, local: str, remote: str, number_commits: int, ) -> None:
    GitOffline.reset_back_by_number_of_commits(path, number_commits)
    assert GitOffline.is_behind_by_number_commits(path, local, remote, number_commits)
