"""New syntax test file"""

from pathlib import Path

# noinspection PyPackageRequirements
from pytest_bdd import scenarios, given

import tests.functional.util as util

scenarios('../../features')


@given("the network connection is disabled")
def given_network_connection_disabled(tmp_path: Path) -> None:
    result = util.disable_network_connection()
    assert result.returncode == 0
