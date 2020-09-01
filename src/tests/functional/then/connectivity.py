"""New syntax test file"""

# noinspection PyPackageRequirements
from pytest_bdd import scenarios, then

import tests.functional.util as util

scenarios('../../features')


@then("the network connection is re-enabled")
def then_network_connection_enabled() -> None:
    result = util.enable_network_connection()
    assert result.returncode == 0
