"""New syntax test file"""

from pathlib import Path

# noinspection PyPackageRequirements
from pytest_bdd import scenarios, when, parsers

import tests.functional.util as util
from tests.functional.util import CommandResults, ScenarioInfo

scenarios('../../features')


@when("the network connection is disabled")
def when_network_connection_disabled(scenario_info: ScenarioInfo, offline) -> None:
    scenario_info.offline = True
    util.disable_network_connection()


@when(parsers.parse("I run '{command}'"))
def when_run_command(tmp_path: Path, command: str, command_results: CommandResults) -> None:
    result = util.run_command(command, tmp_path)
    command_results.completed_processes.append(result)


@when(parsers.parse("I run '{command}' without debug output"))
def when_run_command(tmp_path: Path, command: str, command_results: CommandResults) -> None:
    result = util.run_command(command, tmp_path, clowder_debug=False)
    command_results.completed_processes.append(result)


@when(parsers.parse("I run '{command}' in directory {directory}"))
def when_run_command_directory(tmp_path: Path, command: str, directory: str, command_results: CommandResults) -> None:
    result = util.run_command(command, tmp_path / directory)
    command_results.completed_processes.append(result)


@when(parsers.parse("I run '{command_1}' and '{command_2}'"))
def when_run_commands_and(tmp_path: Path, command_1: str, command_2: str, command_results: CommandResults) -> None:
    commands = [command_1, command_2]
    command_results.completed_processes += [util.run_command(c, tmp_path) for c in commands]


# NOTE: This works, but PyCharm doesn't support parsing it
# @when(parsers.parse("I run:\n{commands}"))
# def when_run_commands(tmp_path: Path, commands: str, command_results: CommandResults) -> None:
#     commands = util.list_from_string(commands, sep="\n")
#     results = [util.run_command(c, tmp_path) for c in commands]
#     command_results.completed_processes += results


# Comma separated list example:
# @when(parsers.cfparse("I run '{command}' for groups {groups:Groups}", extra_types=dict(Groups=list_str_commas)))
# def when_run_clowder_groups(tmp_path: Path, command: str, groups: List[str]) -> None:
#     groups_command = " ".join(g for g in groups)
#     util.run_command(f"{command} {groups_command}", tmp_path)
