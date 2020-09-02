"""New syntax test file"""

from pathlib import Path

# noinspection PyPackageRequirements
from pytest_bdd import scenarios, then

import tests.functional.util as util

scenarios('../../features')


@then("the network connection is enabled")
def then_network_connection_enabled(tmp_path: Path) -> None:
    util.enable_network_connection()
