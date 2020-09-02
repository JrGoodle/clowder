"""New syntax test file"""

from pathlib import Path

# noinspection PyPackageRequirements
from pytest_bdd import scenarios, given

import tests.functional.util as util

scenarios('../../features')


@given("the network connection is enabled")
def given_network_connection_enabled(tmp_path: Path) -> None:
    util.enable_network_connection()
