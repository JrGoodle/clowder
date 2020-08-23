"""New syntax test file"""

# noinspection PyPackageRequirements
from pytest_bdd import scenarios, when, parsers

import tests.functional.common as common

scenarios('../features')


@when(parsers.parse("I run 'clowder {command}'"))
def when_run_clowder(tmpdir, command):
    common.run_command(f"clowder {command}", tmpdir)


@when(parsers.parse("I run 'clowder {command}' with exit code {code:d}"))
def when_run_clowder(tmpdir, command, code):
    result = common.run_command(f"clowder {command}", tmpdir, check=False)
    assert result.returncode == code
