"""New syntax test file"""

from pathlib import Path

from pytest_bdd import given

import tests.functional.util as util


@given("the network connection is enabled")
def given_network_connection_enabled(tmp_path: Path) -> None:
    util.enable_network_connection()
