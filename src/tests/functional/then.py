"""New syntax test file"""

from git import Repo
# noinspection PyPackageRequirements
from pytest_bdd import scenarios, then

from .common import *

scenarios('../features')


@then("project at <directory> exists")
def has_directory(tmpdir, directory):
    path = Path(tmpdir / directory)
    assert path.exists()


@then("project at <directory> is a git repository")
def is_git_repo(tmpdir, directory):
    path = Path(tmpdir / directory)
    assert path.exists()
    assert has_git_directory(path)


@then("project at <directory> is on <branch>")
def check_directory_branch(tmpdir, directory, branch):
    path = Path(tmpdir / directory)
    repo = Repo(str(path))
    active_branch = repo.active_branch.name
    print(f"TEST: active brach '{active_branch}' is '{branch}'")
    assert active_branch == branch


@then("project at <directory> is on <tag>")
def check_directory_tag(tmpdir, directory, tag):
    path = Path(tmpdir / directory)
    repo = Repo(str(path))
    assert repo.head.is_detached
    assert tag in repo.tags
    assert repo.head.commit == repo.tags[tag].commit


@then("project at <directory> is clean")
def check_directory_clean(tmpdir, directory):
    path = Path(tmpdir / directory)
    repo = Repo(str(path))
    print(f"TEST: Project at {directory} is clean")
    assert not is_dirty(repo)
