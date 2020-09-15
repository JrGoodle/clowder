"""
This module contains fixtures
"""

from pytest import fixture

from tests.functional.util import CommandResults, ScenarioInfo


@fixture
def command_results() -> CommandResults:
    return CommandResults()


@fixture
def scenario_info(tmp_path) -> ScenarioInfo:
    return ScenarioInfo(tmp_path)
