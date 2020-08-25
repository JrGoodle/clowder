"""New syntax test file"""

from pathlib import Path
from typing import List

# noinspection PyPackageRequirements
from pytest_bdd import scenarios, when, parsers

import tests.functional.util as util
from .util import list_str

scenarios('../features')


@when(parsers.parse("I run '{command}'"))
def when_run_clowder(tmp_path: Path, command: str) -> None:
    util.run_command(command, tmp_path)


@when(parsers.parse("I run '{command}' with exit code {code:d}"))
def when_run_clowder_exit_code(tmp_path: Path, command: str, code: int) -> None:
    result = util.run_command(command, tmp_path, exit_code=None)
    assert result.returncode == code


@when(parsers.parse("I run '{command}' and it fails"))
def when_run_clowder_fails(tmp_path: Path, command: str) -> None:
    result = util.run_command(command, tmp_path, exit_code=None)
    assert result.returncode != 0


# Groups #


@when(parsers.parse("I run '{command}' for group {group}"))
def when_run_clowder_group(tmp_path: Path, command: str, group: str) -> None:
    util.run_command(f"{command} {group}", tmp_path)


@when(parsers.parse("I run '{command}' for groups {group_1} and {group_2}"))
def when_run_clowder_groups_and(tmp_path: Path, command: str, group_1: str, group_2: str) -> None:
    util.run_command(f"{command} {group_1} {group_2}", tmp_path)


@when(parsers.cfparse("I run '{command}' for groups {groups:Groups}", extra_types=dict(Groups=list_str)))
def when_run_clowder_groups(tmp_path: Path, command: str, groups: List[str]) -> None:
    groups_command = " ".join(g for g in groups)
    util.run_command(f"{command} {groups_command}", tmp_path)


# Projects #


@when(parsers.parse("I run '{command}' for project {project}"))
def when_run_clowder_project(tmp_path: Path, command: str, project: str) -> None:
    util.run_command(f"{command} {project}", tmp_path)


@when(parsers.parse("I run '{command}' for projects {project_1} and {project_2}"))
def when_run_clowder_projects_and(tmp_path: Path, command: str, project_1: str, project_2: str) -> None:
    util.run_command(f"{command} {project_1} {project_2}", tmp_path)


@when(parsers.cfparse("I run '{command}' for projects {projects:Projects}", extra_types=dict(Projects=list_str)))
def when_run_clowder_projects(tmp_path: Path, command: str, projects: List[str]) -> None:
    project_command = " ".join(p for p in projects)
    util.run_command(f"{command} {project_command}", tmp_path)
