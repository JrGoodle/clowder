"""New syntax test file"""

from pathlib import Path

from pytest_bdd import then, parsers

import tests.functional.util as util
from tests.functional.util import CommandResults, ScenarioInfo


@then("the command succeeds")
def then_command_succeeded(command_results: CommandResults, scenario_info: ScenarioInfo, tmp_path: Path) -> None:
    # DEBUG
    util.list_git_config(tmp_path / "mu")
    assert len(command_results.completed_processes) == 1
    assert all([r.returncode == 0 for r in command_results.completed_processes])


@then("the commands succeed")
def then_commands_succeeded(command_results: CommandResults, scenario_info: ScenarioInfo, tmp_path: Path) -> None:
    assert len(command_results.completed_processes) > 1
    assert all([result.returncode == 0 for result in command_results.completed_processes])


@then("the command fails")
def then_command_failed(command_results: CommandResults, scenario_info: ScenarioInfo, tmp_path: Path) -> None:
    assert len(command_results.completed_processes) == 1
    assert all([result.returncode != 0 for result in command_results.completed_processes])


@then("the commands fail")
def then_commands_failed(command_results: CommandResults, scenario_info: ScenarioInfo, tmp_path: Path) -> None:
    assert len(command_results.completed_processes) > 1
    assert all([result.returncode != 0 for result in command_results.completed_processes])


@then(parsers.parse("the command exited with return code {code:d}"))
def then_command_exit_return_code(command_results: CommandResults, code: int, scenario_info: ScenarioInfo,
                                  tmp_path: Path) -> None:
    assert len(command_results.completed_processes) == 1
    assert all([result.returncode == code for result in command_results.completed_processes])
