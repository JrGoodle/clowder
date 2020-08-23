"""New syntax test file"""

from git import Repo
# noinspection PyPackageRequirements
from pytest_bdd import scenarios, given, parsers

from .common import *

scenarios('../features')


@given(parsers.parse("{example} example is initialized"))
def given_example_init(tmpdir, example):
    url = get_url(example)
    command = f"clowder init {url}"
    run_command(command, tmpdir)


@given(parsers.parse("{example} example is initialized to {branch}"))
def given_example_init_branch(tmpdir, example, branch):
    url = get_url(example)
    command = f"clowder init {url} -b {branch}"
    run_command(command, tmpdir)


@given(parsers.parse("{example} example is initialized with {protocol}"))
def given_example_init_branch_protocol(tmpdir, example, protocol):
    url = get_url(example, protocol=protocol)
    command = f"clowder init {url}"
    run_command(command, tmpdir)


@given(parsers.parse("{example} example is initialized to {branch} with {protocol}"))
def given_example_init_branch_protocol(tmpdir, example, branch, protocol):
    url = get_url(example, protocol=protocol)
    command = f"clowder init {url} -b {branch}"
    run_command(command, tmpdir)


@given(parsers.parse("{example} example is initialized to {branch} with {protocol}"))
def given_example_init_branch_protocol(tmpdir, example, branch, protocol):
    url = get_url(example, protocol=protocol)
    command = f"clowder init {url} -b {branch}"
    run_command(command, tmpdir)


@given(parsers.parse("'clowder {command}' has been run"))
def given_run_clowder_command(tmpdir, command):
    command = f"clowder {command}"
    run_command(command, tmpdir)


@given(parsers.parse("{version} yaml version is linked"))
def given_link_yaml_version(tmpdir, version):
    versions_dir = Path(tmpdir / ".clowder" / "versions")
    yaml_version = versions_dir/ f"{version}.clowder.yaml"
    yml_version = versions_dir / f"{version}.clowder.yml"
    if yaml_version.exists():
        version_file = yaml_version
        path = Path(tmpdir / "clowder.yaml")
    elif yml_version.exists():
        version_file = yml_version
        path = Path(tmpdir / "clowder.yml")
    else:
        assert False

    command = f"clowder link {version}"
    run_command(command, tmpdir)
    assert path.exists()
    assert path.is_file()
    assert path.is_symlink()
    assert version_file.samefile(path.resolve())


@given("I'm in an empty directory")
def given_is_empty_directory(tmpdir):
    print(f"tmpdir: {tmpdir}")
    assert is_directory_empty(tmpdir)


@given("<directory> doesn't exist")
def given_has_no_directory(tmpdir, directory):
    path = Path(tmpdir / directory)
    assert not path.exists()


@given(parsers.parse("{directory} has untracked file {name}"))
def given_untracked_file(tmpdir, directory, name):
    repo_path = Path(tmpdir / directory)
    path = Path(tmpdir / directory / name)
    create_file(path)
    repo = Repo(repo_path)
    assert repo.untracked_files
