"""New syntax test file"""

from pathlib import Path

from pygoodle.git import GitOffline, Repo
from pytest_bdd import given, parsers


@given(parsers.parse("repo at {directory} is on {start_branch}"))
@given(parsers.parse("project at {directory} is on {start_branch}"))
@given("project at <directory> is on <start_branch>")
def given_directory_on_start_branch(tmp_path: Path, directory: str, start_branch: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.current_branch == start_branch


@given("project at <directory> is on <test_branch>")
def given_directory_on_test_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.current_branch == test_branch


@given(parsers.parse("repo at {directory} has local branch {test_branch}"))
@given(parsers.parse("project at {directory} has local branch {test_branch}"))
@given("project at <directory> has local <test_branch>")
def given_directory_has_local_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.has_local_branch(test_branch)


@given(parsers.parse("repo at {directory} has no local branch {test_branch}"))
@given(parsers.parse("project at {directory} has no local branch {test_branch}"))
@given("project at <directory> has no local <test_branch>")
def given_directory_has_no_local_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    repo = Repo(tmp_path / directory)
    assert not repo.has_local_branch(test_branch)


@given(parsers.parse("repo at {directory} has no remote branch {test_branch}"))
@given(parsers.parse("project at {directory} has no remote branch {test_branch}"))
@given("project at <directory> has no remote <test_branch>")
def given_directory_has_no_remote_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    repo = Repo(tmp_path / directory)
    assert not repo.has_remote_branch(test_branch)


@given(parsers.parse("repo at {directory} has remote branch {test_branch}"))
@given(parsers.parse("project at {directory} has remote branch {test_branch}"))
@given("project at <directory> has remote <test_branch>")
def given_directory_has_remote_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.has_remote_branch(test_branch)


@given(parsers.parse("repo at {directory} is on branch {branch}"))
@given(parsers.parse("project at {directory} is on branch {branch}"))
@given("project at <directory> is on <branch>")
def given_directory_branch(tmp_path: Path, directory: str, branch: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.current_branch == branch


@given(parsers.parse("repo at {directory} is on tag {tag}"))
@given(parsers.parse("project at {directory} is on tag {tag}"))
@given("project at <directory> is on <tag>")
def given_directory_tag(tmp_path: Path, directory: str, tag: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.sha() == repo.get_local_tag(tag).sha


@given(parsers.parse("repo at {directory} is on commit {commit}"))
@given(parsers.parse("project at {directory} is on commit {commit}"))
@given("project at <directory> is on <commit>")
def given_directory_commit(tmp_path: Path, directory: str, commit: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.sha() == commit


@given(parsers.parse("repo at {directory} has detached HEAD"))
@given(parsers.parse("project at {directory} has detached HEAD"))
@given("project at <directory> has detached HEAD")
def given_directory_detached_head(tmp_path: Path, directory: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.is_detached


@given(parsers.parse("repo at {directory} has remote tag {tag}"))
@given(parsers.parse("project at {directory} has remote tag {tag}"))
@given("project at <directory> has remote <tag>")
def given_directory_tag(tmp_path: Path, directory: str, tag: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.sha() == repo.get_remote_tag(tag).sha


@given(parsers.parse("repo at {directory} is clean"))
@given(parsers.parse("project at {directory} is clean"))
@given("project at <directory> is clean")
def given_directory_clean(tmp_path: Path, directory: str) -> None:
    repo = Repo(tmp_path / directory)
    assert not repo.is_dirty


@given(parsers.parse("repo at {directory} is dirty"))
@given(parsers.parse("project at {directory} is dirty"))
@given("project at <directory> is dirty")
def given_directory_dirty(tmp_path: Path, directory: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.is_dirty


@given(parsers.parse("repo at {directory} has untracked files"))
@given(parsers.parse("project at {directory} has untracked files"))
@given("project at <directory> has untracked files")
def given_directory_has_untracked_files(tmp_path: Path, directory: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.has_untracked_files


@given(parsers.parse("repo at {directory} has no untracked files"))
@given(parsers.parse("project at {directory} has no untracked files"))
@given("project at <directory> has no untracked files")
def given_directory_has_no_untracked_files(tmp_path: Path, directory: str) -> None:
    repo = Repo(tmp_path / directory)
    assert not repo.has_untracked_files


@given(parsers.parse("repo at {directory} has rebase in progress"))
@given(parsers.parse("project at {directory} has rebase in progress"))
@given("project at <directory> has rebase in progress")
def given_directory_has_rebase_in_progress(tmp_path: Path, directory: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.is_rebase_in_progress


@given(parsers.parse("repo at {directory} has no rebase in progress"))
@given(parsers.parse("project at {directory} has no rebase in progress"))
@given("project at <directory> has no rebase in progress")
def given_directory_has_no_rebase_in_progress(tmp_path: Path, directory: str) -> None:
    repo = Repo(tmp_path / directory)
    assert not repo.is_rebase_in_progress


@given(parsers.parse("repo at {directory} has untracked file {filename}"))
@given(parsers.parse("project at {directory} has untracked file {filename}"))
@given("project at <directory> has untracked file <filename>")
def given_has_untracked_file(tmp_path: Path, directory: str, filename: str) -> None:
    repo = Repo(tmp_path / directory)
    assert Path(filename) in repo.untracked_files


@given(parsers.parse("repo at {directory} has tracking branch {test_branch}"))
@given(parsers.parse("project at {directory} has tracking branch {test_branch}"))
@given("project at <directory> has tracking <test_branch>")
def given_directory_has_tracking_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    repo = Repo(tmp_path / directory)
    assert repo.has_tracking_branch(test_branch)


@given(parsers.parse("repo at {directory} has no tracking branch {test_branch}"))
@given(parsers.parse("project at {directory} has no tracking branch {test_branch}"))
@given("project at <directory> has no tracking <test_branch>")
def given_directory_has_no_tracking_branch(tmp_path: Path, directory: str, test_branch: str) -> None:
    repo = Repo(tmp_path / directory)
    assert not repo.has_tracking_branch(test_branch)


@given(parsers.parse("GitHub {repo} has remote tag {tag}"))
@given("GitHub <repo> has remote <tag>")
def given_github_repo_has_remote_tag(tmp_path: Path, repo: str, tag: str) -> None:
    url = f"https://github.com/{repo}"
    repo = Repo(tmp_path)
    assert repo.has_remote_tag(tag, url=url)


@given(parsers.parse("GitHub {repo} has no remote tag {tag}"))
@given("GitHub <repo> has no remote <tag>")
def given_github_repo_has_no_remote_tag(tmp_path: Path, repo: str, tag: str) -> None:
    url = f"https://github.com/{repo}"
    repo = Repo(tmp_path)
    assert not repo.has_remote_tag(tag, url=url)


@given("<test_directory> is a git repository")
def given_test_dir_is_git_repo(tmp_path: Path, test_directory: str) -> None:
    repo = Repo(tmp_path / test_directory)
    assert repo.exists


@given("project at <directory> doesn't have lfs installed")
def given_has_no_lfs_installed(tmp_path: Path, directory: str) -> None:
    path = tmp_path / directory
    repo = Repo(path)
    repo.uninstall_lfs()
    assert not GitOffline.lfs_hooks_installed(path)
    assert not GitOffline.lfs_filters_installed(path)


@given("lfs is not installed")
def given_has_no_lfs_installed(tmp_path: Path) -> None:
    path = tmp_path
    repo = Repo(path)
    repo.uninstall_lfs()
    assert not GitOffline.lfs_hooks_installed(path)
    assert not GitOffline.lfs_filters_installed(path)


@given(parsers.parse("{filename} file doesn't exist in directory {directory}"))
@given("<filename> doesn't exist in <directory>")
def given_has_no_file_in_directory(tmp_path: Path, filename: str, directory: str) -> None:
    path = tmp_path / directory / filename
    assert not path.exists()


@given("<filename> in <directory> is an lfs pointer")
def given_file_is_lfs_pointer(tmp_path: Path, filename: str, directory: str) -> None:
    path = tmp_path / directory
    assert GitOffline.is_lfs_file_pointer(path, filename)


@given("<filename> in <directory> is not an lfs pointer")
def given_file_is_not_lfs_pointer(tmp_path: Path, filename: str, directory: str) -> None:
    path = tmp_path / directory
    assert GitOffline.is_lfs_file_not_pointer(path, filename)
