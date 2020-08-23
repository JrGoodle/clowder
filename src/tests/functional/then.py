"""New syntax test file"""

from git import Repo
# noinspection PyPackageRequirements
from pytest_bdd import scenarios, then, parsers

from .common import *

scenarios('../features')


@then("project at <directory> exists")
@then(parsers.parse("project at {directory} exists"))
def then_has_project_directory(tmpdir, directory):
    path = Path(tmpdir / directory)
    assert path.exists()
    assert path.is_dir()


@then("project at <directory> is a git repository")
@then(parsers.parse("project at {directory} is a git repository"))
def then_is_git_repo(tmpdir, directory):
    path = Path(tmpdir / directory)
    assert path.exists()
    assert has_git_directory(path)


@then("project at <directory> is on <branch>")
def then_check_directory_branch(tmpdir, directory, branch):
    path = Path(tmpdir / directory)
    repo = Repo(str(path))
    active_branch = repo.active_branch.name
    print(f"TEST: active brach '{active_branch}' is '{branch}'")
    assert active_branch == branch


@then("project at <directory> is on <tag>")
def then_check_directory_tag(tmpdir, directory, tag):
    path = Path(tmpdir / directory)
    repo = Repo(str(path))
    assert repo.head.is_detached
    assert tag in repo.tags
    assert repo.head.commit == repo.tags[tag].commit


@then("project at <directory> is on <commit>")
def then_check_directory_commit(tmpdir, directory, commit):
    path = Path(tmpdir / directory)
    repo = Repo(str(path))
    assert repo.head.is_detached
    assert repo.head.commit.hexsha == commit


@then("project at <directory> is clean")
def then_check_directory_clean(tmpdir, directory):
    path = Path(tmpdir / directory)
    repo = Repo(str(path))
    print(f"TEST: Project at {directory} is clean")
    assert not is_dirty(repo)


@then(parsers.parse("{directory} has untracked file {name}"))
def then_has_untracked_file(tmpdir, directory, name):
    repo_path = Path(tmpdir / directory)
    path = Path(tmpdir / directory / name)
    repo = Repo(repo_path)
    assert f"{path.stem}{path.suffix}" in repo.untracked_files
