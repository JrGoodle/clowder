"""New syntax test file"""

from pathlib import Path
from pytest_bdd import when, parsers

from clowder.util.connectivity import get_gateway_ip_address, disable_network_connection, enable_network_connection
from tests.functional.util import CommandResults, ScenarioInfo, run_command


@when("the network connection is disabled")
def when_network_connection_disabled(scenario_info: ScenarioInfo) -> None:
    scenario_info.gateway_address = get_gateway_ip_address()
    scenario_info.offline = True
    disable_network_connection()


@when("the network connection is enabled")
def when_network_connection_enabled(scenario_info: ScenarioInfo) -> None:
    enable_network_connection(scenario_info.gateway_address)


@when(parsers.parse("I change to directory {subdirectory}"))
def when_change_subdirectory(subdirectory: str, scenario_info: ScenarioInfo) -> None:
    scenario_info.relative_dir = subdirectory


@when("I change to <directory>")
def when_change_directory(directory: str, scenario_info: ScenarioInfo) -> None:
    scenario_info.relative_dir = directory


@when(parsers.parse("I run '{command}'"))
def when_run_command(tmp_path: Path, command: str, command_results: CommandResults,
                     scenario_info: ScenarioInfo) -> None:
    path = scenario_info.cmd_dir
    result = run_command(command, path)
    command_results.completed_processes.append(result)


@when(parsers.parse("I run '{command_1}' and '{command_2}'"))
def when_run_command_and_command(command_1: str, command_2: str,
                                 command_results: CommandResults, scenario_info: ScenarioInfo) -> None:
    path = scenario_info.cmd_dir
    commands = [command_1, command_2]
    command_results.completed_processes += [run_command(c, path) for c in commands]
