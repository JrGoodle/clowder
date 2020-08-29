"""
This module contains fixtures
"""

# noinspection PyPackageRequirements
from pytest import fixture

from tests.functional.util import CommandResults, TestInfo


@fixture
def command_results() -> CommandResults:
    return CommandResults()


@fixture
def test_info() -> TestInfo:
    return TestInfo()
