"""New syntax test file"""

# noinspection PyPackageRequirements
from pytest_bdd import scenarios, when, parsers

from .common import *

scenarios('../features')


@when(parsers.parse("I run 'clowder {command}'"))
def run_clowder(tmpdir, command):
    run_command(f"clowder {command}", tmpdir)
