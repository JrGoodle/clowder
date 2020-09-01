"""
This module contains fixtures
"""

# noinspection PyPackageRequirements
from pytest import fixture

import tests.functional.util as util


@fixture(scope="session")
def offline(cats_init_session, cats_init_herd_session) -> None:
    util.disable_network_connection()
    yield None
    util.enable_network_connection()
