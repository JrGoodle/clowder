"""New syntax test file"""

from pathlib import Path
from typing import List

# noinspection PyPackageRequirements
from pytest_bdd import scenarios, when, parsers

import tests.functional.util as util

scenarios('../features')


@when(parsers.parse("I run 'clowder {command}'"))
def when_run_clowder(tmp_path: Path, command: str) -> None:
    util.run_command(f"clowder {command}", tmp_path)


@when(parsers.parse("I run 'clowder {command}' with exit code {code:d}"))
def when_run_clowder_exit_code(tmp_path: Path, command: str, code: int) -> None:
    result = util.run_command(f"clowder {command}", tmp_path, exit_code=None)
    assert result.returncode == code


@when(parsers.parse("I run 'clowder {command}' and it fails"))
def when_run_clowder_fails(tmp_path: Path, command: str) -> None:
    result = util.run_command(f"clowder {command}", tmp_path, exit_code=None)
    assert result.returncode != 0


@when(parsers.cfparse("I run 'clowder {command}' for groups {groups:Groups}",
                      extra_types=dict(Groups=util.parse_list_string)))
@when(parsers.cfparse("I run 'clowder {command}' for group {groups:Groups}",
                      extra_types=dict(Groups=util.parse_list_string)))
def when_run_clowder_groups(tmp_path: Path, command: str, groups: List[str]) -> None:
    print("JOE TEST")
    print(groups)
    groups_command = " ".join(g for g in groups)
    util.run_command(f"clowder {command} {groups_command}", tmp_path)
