"""
This module contains fixtures
"""

from pytest import fixture

import tests.functional.util as util


@fixture(scope="session")
def offline(cats_init_session, cats_init_herd_session) -> None:
    util.disable_network_connection()
    yield
    util.enable_network_connection()
