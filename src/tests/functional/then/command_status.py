"""New syntax test file"""

# noinspection PyPackageRequirements
from pytest_bdd import scenarios, then, parsers

import tests.functional.util as util
from tests.functional.util import CommandResults, ScenarioInfo

scenarios('../../features')


@then("the command succeeds")
def then_command_succeeded(command_results: CommandResults, scenario_info: ScenarioInfo) -> None:
    assert len(command_results.completed_processes) == 1
    assert all([result.returncode == 0 for result in command_results.completed_processes])
    # if scenario_info.offline:
    #     util.enable_network_connection()


@then("the commands succeed")
def then_commands_succeeded(command_results: CommandResults, scenario_info: ScenarioInfo) -> None:
    assert len(command_results.completed_processes) > 1
    assert all([result.returncode == 0 for result in command_results.completed_processes])
    # if scenario_info.offline:
    #     util.enable_network_connection()


@then("the command fails")
def then_command_failed(command_results: CommandResults, scenario_info: ScenarioInfo) -> None:
    assert len(command_results.completed_processes) == 1
    assert all([result.returncode != 0 for result in command_results.completed_processes])
    # if scenario_info.offline:
    #     util.enable_network_connection()


@then("the commands fail")
def then_commands_failed(command_results: CommandResults, scenario_info: ScenarioInfo) -> None:
    assert len(command_results.completed_processes) > 1
    assert all([result.returncode != 0 for result in command_results.completed_processes])
    # if scenario_info.offline:
    #     util.enable_network_connection()


@then(parsers.parse("the command exited with return code {code:d}"))
def then_command_exit_return_code(command_results: CommandResults, code: int, scenario_info: ScenarioInfo) -> None:
    assert len(command_results.completed_processes) == 1
    assert all([result.returncode == code for result in command_results.completed_processes])
    # if scenario_info.offline:
    #     util.enable_network_connection()
