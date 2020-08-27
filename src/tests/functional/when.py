"""New syntax test file"""

from pathlib import Path
from typing import List

# noinspection PyPackageRequirements
from pytest_bdd import scenarios, when, parsers

import tests.functional.util as util
from .util import list_str_commas, CommandResults

scenarios('../features')


@when(parsers.parse("I run '{command}'"))
def when_run_command(tmp_path: Path, command: str, command_results: CommandResults) -> None:
    result = util.run_command(command, tmp_path)
    command_results.completed_processes.append(result)


@when(parsers.parse("I run '{command}' from directory {directory}"))
def when_run_command_directory(tmp_path: Path, command: str, directory: str, command_results: CommandResults) -> None:
    result = util.run_command(command, tmp_path / directory)
    command_results.completed_processes.append(result)


# @when("I run '<command>'")
# def when_run_command_outline(tmp_path: Path, command: str, command_results: CommandResults) -> None:
#     result = util.run_command(command, tmp_path)
#     command_results.completed_processes.append(result)


@when(parsers.parse("I run '{command_1}' and '{command_2}'"))
def when_run_commands_and(tmp_path: Path, command_1: str, command_2: str, command_results: CommandResults) -> None:
    commands = [command_1, command_2]
    command_results.completed_processes += [util.run_command(c, tmp_path) for c in commands]


@when(parsers.parse("I run:\n{commands}"))
def when_run_commands(tmp_path: Path, commands: str, command_results: CommandResults) -> None:
    commands = util.list_from_string(commands, sep="\n")
    results = [util.run_command(c, tmp_path) for c in commands]
    command_results.completed_processes += results


# Groups #


@when(parsers.parse("I run '{command}' for group {group}"))
def when_run_clowder_group(tmp_path: Path, command: str, group: str) -> None:
    util.run_command(f"{command} {group}", tmp_path)


@when(parsers.parse("I run '{command}' for groups {group_1} and {group_2}"))
def when_run_clowder_groups_and(tmp_path: Path, command: str, group_1: str, group_2: str) -> None:
    util.run_command(f"{command} {group_1} {group_2}", tmp_path)


@when(parsers.cfparse("I run '{command}' for groups {groups:Groups}", extra_types=dict(Groups=list_str_commas)))
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


@when(parsers.cfparse("I run '{command}' for projects {projects:Projects}", extra_types=dict(Projects=list_str_commas)))
def when_run_clowder_projects(tmp_path: Path, command: str, projects: List[str]) -> None:
    project_command = " ".join(p for p in projects)
    util.run_command(f"{command} {project_command}", tmp_path)
