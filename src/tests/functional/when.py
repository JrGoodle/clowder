"""New syntax test file"""

from pathlib import Path

# noinspection PyPackageRequirements
from pytest_bdd import scenarios, when, parsers

import tests.functional.common as common

scenarios('../features')


@when(parsers.parse("I run 'clowder {command}'"))
def when_run_clowder(tmp_path: Path, command: str) -> None:
    common.run_command(f"clowder {command}", tmp_path)


@when(parsers.parse("I run 'clowder {command}' with exit code {code:d}"))
def when_run_clowder_exit_code(tmp_path: Path, command: str, code: int) -> None:
    result = common.run_command(f"clowder {command}", tmp_path, exit_code=None)
    assert result.returncode == code


@when(parsers.parse("I run 'clowder {command}' and it fails"))
def when_run_clowder_exit_code(tmp_path: Path, command: str) -> None:
    result = common.run_command(f"clowder {command}", tmp_path, exit_code=None)
    assert result.returncode != 0
