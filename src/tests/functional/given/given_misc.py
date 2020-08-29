"""New syntax test file"""

from pathlib import Path

# noinspection PyPackageRequirements
from pytest_bdd import scenarios, given, parsers

from tests.functional.util import TestInfo

scenarios('../../features')


@given(parsers.parse("misc example is initialized"))
def given_misc_init(tmp_path: Path, misc_init, test_info: TestInfo) -> None:
    test_info.example = "misc"


@given(parsers.parse("misc example is initialized and herded"))
def given_misc_init_herd(tmp_path: Path, misc_init_herd, test_info: TestInfo) -> None:
    test_info.example = "misc"


@given(parsers.parse("misc example is initialized and herded with https"))
def given_misc_init_herd(tmp_path: Path, misc_init_herd_version_https, test_info: TestInfo) -> None:
    test_info.example = "misc"
    test_info.version = "https"
