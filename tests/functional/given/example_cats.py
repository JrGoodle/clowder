"""New syntax test file"""

from pathlib import Path

from pygoodle.git import LocalBranch, RemoteBranch, Repo, TrackingBranch
from pytest_bdd import given, parsers

from tests.functional.util import ScenarioInfo, CATS_REPOS_DEFAULT


@given(parsers.parse("cats example is initialized"))
def given_cats_init(tmp_path: Path, cats_init, scenario_info: ScenarioInfo) -> None:
    scenario_info.example = "cats"


@given(parsers.parse("cats example is initialized with ssh"))
def given_cats_init_ssh(tmp_path: Path, cats_init_ssh, scenario_info: ScenarioInfo) -> None:
    scenario_info.example = "cats"
    scenario_info.protocol = "ssh"


@given(parsers.parse("cats example is initialized and herded"))
def given_cats_init_herd(tmp_path: Path, cats_init_herd, scenario_info: ScenarioInfo) -> None:
    scenario_info.example = "cats"


@given(parsers.parse("cats example is initialized and herded with ssh"))
def given_cats_init_herd_ssh(tmp_path: Path, cats_init_herd_ssh, scenario_info: ScenarioInfo) -> None:
    scenario_info.example = "cats"
    scenario_info.version = "ssh"
    scenario_info.protocol = "ssh"


@given(parsers.parse("cats example non-symlink yaml file exists"))
def given_cats_non_symlink_yaml(tmp_path: Path, cats_non_symlink_yaml, scenario_info: ScenarioInfo) -> None:
    scenario_info.example = "cats"


@given(parsers.parse("cats example non-symlink yml file exists"))
def given_cats_non_symlink_yml(tmp_path: Path, cats_non_symlink_yml, scenario_info: ScenarioInfo) -> None:
    scenario_info.example = "cats"


@given(parsers.parse("cats example ambiguous non-symlink yaml and yml files exist"))
def given_cats_ambiguous_non_symlink_yaml_files(tmp_path: Path, cats_ambiguous_non_symlink_yaml_files,
                                                scenario_info: ScenarioInfo) -> None:
    scenario_info.example = "cats"


@given(parsers.parse("cats example clowder repo symlink exists"))
def given_cats_clowder_repo_symlink(tmp_path: Path, cats_clowder_repo_symlink,
                                    scenario_info: ScenarioInfo) -> None:
    scenario_info.example = "cats"


@given(parsers.parse("cats example projects have no remote branch {test_branch}"))
@given("cats example projects have no remote branch <test_branch>")
def given_cats_no_remote_branch(tmp_path: Path, scenario_info: ScenarioInfo, test_branch: str) -> None:
    scenario_info.example = "cats"
    for name, info in CATS_REPOS_DEFAULT.items():
        repo = Repo(tmp_path / info["path"])
        repo.fetch(prune=True, fetch_all=True)
        remote_branch = repo.get_remote_branch(test_branch, online=True)
        if remote_branch is None:
            return
        remote_branch.delete()
        repo.fetch(prune=True, fetch_all=True)
        assert not remote_branch.exists


@given(parsers.parse("cats example projects have remote branch {test_branch}"))
@given("cats example projects have remote branch <test_branch>")
def given_cats_remote_branch(tmp_path: Path, scenario_info: ScenarioInfo, test_branch: str) -> None:
    scenario_info.example = "cats"
    for name, info in CATS_REPOS_DEFAULT.items():
        repo_path = tmp_path / info["path"]
        repo = Repo(repo_path)
        repo.fetch(prune=True, fetch_all=True)
        remote_branch = RemoteBranch(repo_path, test_branch)
        if remote_branch.exists:
            remote_branch.delete()
            repo.fetch(prune=True, fetch_all=True)
            assert not remote_branch.exists
            assert not remote_branch.exists_online()
        remote_branch.create()
        repo.fetch(prune=True, fetch_all=True)
        assert remote_branch.exists
        assert remote_branch.exists_online()


@given(parsers.parse("cats example projects have tracking branch {test_branch}"))
@given("cats example projects have tracking branch <test_branch>")
def given_cats_tracking_branch(tmp_path: Path, scenario_info: ScenarioInfo, test_branch: str) -> None:
    scenario_info.example = "cats"
    for name, info in CATS_REPOS_DEFAULT.items():
        repo_path = tmp_path / info["path"]
        repo = Repo(repo_path)
        repo.fetch(prune=True, fetch_all=True)
        tracking_branch = TrackingBranch(repo_path, test_branch)
        # TODO: Should this delete remote branch too?
        if tracking_branch.local_branch.exists:
            tracking_branch.local_branch.delete()
            assert not tracking_branch.exists
        tracking_branch.create()
        repo.fetch(prune=True, fetch_all=True)
        assert tracking_branch.exists


@given(parsers.parse("cats example projects have local branch {test_branch}"))
@given("cats example projects have local branch <test_branch>")
def given_cats_local_branch(tmp_path: Path, scenario_info: ScenarioInfo, test_branch: str) -> None:
    scenario_info.example = "cats"
    for name, info in CATS_REPOS_DEFAULT.items():
        repo_path = tmp_path / info["path"]
        repo = Repo(repo_path)
        repo.fetch(prune=True, fetch_all=True)
        local_branch = LocalBranch(repo_path, test_branch)
        if not local_branch.exists:
            local_branch.create(track=False)
        assert local_branch.exists


@given(parsers.parse("cats example projects have no local branch {test_branch}"))
@given("cats example projects have no local branch <test_branch>")
def given_cats_no_local_branch(tmp_path: Path, scenario_info: ScenarioInfo, test_branch: str) -> None:
    scenario_info.example = "cats"
    for name, info in CATS_REPOS_DEFAULT.items():
        repo = Repo(tmp_path / info["path"])
        repo.fetch(prune=True, fetch_all=True)
        local_branch = repo.get_local_branch(test_branch)
        if local_branch is None:
            return
        local_branch.delete()
        assert not local_branch.exists
