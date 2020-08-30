"""New syntax test file"""

from pathlib import Path

# noinspection PyPackageRequirements
from pytest_bdd import scenarios, given, parsers

from tests.functional.util import ScenarioInfo

scenarios('../../features')


@given(parsers.parse("cats example is initialized"))
def given_cats_init(tmp_path: Path, cats_init, test_info: ScenarioInfo) -> None:
    test_info.example = "cats"


@given(parsers.parse("cats example is initialized and herded"))
def given_cats_init_herd(tmp_path: Path, cats_init_herd, test_info: ScenarioInfo) -> None:
    test_info.example = "cats"


@given(parsers.parse("cats example is initialized to branch yaml-validation"))
def given_cats_init_branch_yaml_validation(tmp_path: Path, cats_init_yaml_validation, test_info: ScenarioInfo) -> None:
    test_info.example = "cats"
    test_info.branch = "yaml-validation"


# @given(parsers.parse("cats example is initialized and herded to branch yaml-validation and version test-empty-project")) # noqa
# def given_cats_init_yaml_validation_herd_test_empty_project(tmp_path: Path,
#                                                             cats_init_yaml_validation_herd_test_empty_project,
#                                                             test_info: TestInfo) -> None:
#     test_info.example = "misc"
#     test_info.branch = "yaml-validation"
#     test_info.version = "test-empty-project"


@given(parsers.parse("cats example is initialized to branch extension"))
def given_cats_init_branch_extension(tmp_path: Path, cats_init_extension, test_info: ScenarioInfo) -> None:
    test_info.example = "cats"
    test_info.branch = "extension"


@given(parsers.parse("cats example non-symlink yaml file exists"))
def given_cats_non_symlink_yaml(tmp_path: Path, cats_non_symlink_yaml, test_info: ScenarioInfo) -> None:
    test_info.example = "cats"
