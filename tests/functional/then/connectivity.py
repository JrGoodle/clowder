"""New syntax test file"""

from pathlib import Path

from pytest_bdd import then

import tests.functional.util as util


@then("the network connection is enabled")
def then_network_connection_enabled(tmp_path: Path) -> None:
    util.enable_network_connection()
