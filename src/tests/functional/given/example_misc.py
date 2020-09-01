"""New syntax test file"""

from pathlib import Path

# noinspection PyPackageRequirements
from pytest_bdd import scenarios, given, parsers

from tests.functional.util import ScenarioInfo

scenarios('../../features')


@given(parsers.parse("misc example is initialized"))
def given_misc_init(tmp_path: Path, misc_init, scenario_info) -> None:
    scenario_info.example = "misc"


@given(parsers.parse("misc example is initialized and herded"))
def given_misc_init_herd(tmp_path: Path, misc_init_herd, scenario_info) -> None:
    scenario_info.example = "misc"


@given(parsers.parse("misc example is initialized and herded with https"))
def given_misc_init_herd(tmp_path: Path, misc_init_herd_version_https, scenario_info) -> None:
    scenario_info.example = "misc"
    scenario_info.version = "https"
