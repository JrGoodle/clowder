"""New syntax test file"""

import os
import shutil
from pathlib import Path

from git import Repo
# noinspection PyPackageRequirements
from pytest_bdd import scenarios, given, parsers

import tests.functional.util as util
from tests.functional.util import TestInfo

scenarios('../../features')


@given(parsers.parse("cats example is initialized"))
def given_cats_init(tmp_path: Path, cats_init, test_info: TestInfo) -> None:
    test_info.example = "cats"


@given(parsers.parse("cats example is initialized and herded"))
def given_cats_init_herd(tmp_path: Path, cats_init_herd, test_info: TestInfo) -> None:
    test_info.example = "cats"


@given(parsers.parse("cats example is initialized to yaml-validation"))
def given_cats_init_branch_yaml_validation(tmp_path: Path, cats_init_yaml_validation, test_info: TestInfo) -> None:
    test_info.example = "misc"
    test_info.branch = "yaml-validation"


# @given(parsers.parse("cats example is initialized to yaml-validation and herded to test-empty-project"))
# def given_cats_init_yaml_validation_herd_test_empty_project(tmp_path: Path,
#                                                             cats_init_yaml_validation_herd_test_empty_project,
#                                                             test_info: TestInfo) -> None:
#     test_info.example = "misc"
#     test_info.branch = "yaml-validation"
#     test_info.version = "test-empty-project"


@given(parsers.parse("cats example is initialized to extension"))
def given_cats_init_branch_extension(tmp_path: Path, cats_init_extension, test_info: TestInfo) -> None:
    test_info.example = "misc"
    test_info.branch = "extension"

