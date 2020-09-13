"""test_features"""

import pytest
from pathlib import Path
from typing import List, Tuple

from pytest_bdd import scenario

from tests.functional.util import yaml_property_tests


def get_test_params(name: str) -> List[Tuple[str]]:
    return [(f,) for f in yaml_property_tests(name)]


@pytest.mark.parametrize(["project_branch"], get_test_params("project.branch"))
@scenario(
    "../features/yaml_validation.feature",
    "validate project.branch",
)
def test_validate_project_branch(project_branch: Path):
    pass


@pytest.mark.parametrize(["project_implicit"], get_test_params("project.implicit"))
@scenario(
    "../features/yaml_validation.feature",
    "validate implicit project.branch",
)
def test_validate_project_branch_implicit(project_implicit: Path):
    pass


@pytest.mark.parametrize(["project_commit"], get_test_params("project.commit"))
@scenario(
    "../features/yaml_validation.feature",
    "validate project.commit",
)
def test_validate_project_commit(project_commit: Path):
    pass


@pytest.mark.parametrize(["project_implicit"], get_test_params("project.implicit"))
@scenario(
    "../features/yaml_validation.feature",
    "validate implicit project.commit",
)
def test_validate_project_commit_implicit(project_implicit: Path):
    pass


@pytest.mark.parametrize(["project_git_config"], get_test_params("project.git.config"))
@scenario(
    "../features/yaml_validation.feature",
    "validate project.git.config",
)
def test_validate_project_git_config(project_git_config: Path):
    pass


@pytest.mark.parametrize(["project_implicit"], get_test_params("project.implicit"))
@scenario(
    "../features/yaml_validation.feature",
    "validate implicit project.git.config",
)
def test_validate_project_git_config_implicit(project_implicit: Path):
    pass


# @pytest.mark.parametrize(["project_git_depth"], get_test_params("project.git.depth"))
# @scenario(
#     "../features/yaml_validation.feature",
#     "validate project.git.depth",
# )
# def test_validate_project_git_depth(project_git_depth: Path):
#     pass
#
#
# @pytest.mark.parametrize(["project_implicit"], get_test_params("project.implicit"))
# @scenario(
#     "../features/yaml_validation.feature",
#     "validate implicit project.git.depth",
# )
# def test_validate_project_git_depth_implicit(project_implicit: Path):
#     pass


@pytest.mark.parametrize(["project_git_lfs"], get_test_params("project.git.lfs"))
@scenario(
    "../features/yaml_validation.feature",
    "validate project.git.lfs",
)
def test_validate_project_git_lfs(project_git_lfs: Path):
    pass


@pytest.mark.parametrize(["project_implicit"], get_test_params("project.implicit"))
@scenario(
    "../features/yaml_validation.feature",
    "validate implicit project.git.lfs",
)
def test_validate_project_git_lfs_implicit(project_implicit: Path):
    pass


@pytest.mark.parametrize(["project_git_submodules"], get_test_params("project.git.submodules"))
@scenario(
    "../features/yaml_validation.feature",
    "validate project.git.submodules",
)
def test_validate_project_git_submodules(project_git_submodules: Path):
    pass


@pytest.mark.parametrize(["project_implicit"], get_test_params("project.implicit"))
@scenario(
    "../features/yaml_validation.feature",
    "validate implicit project.git.submodules",
)
def test_validate_project_git_submodules_implicit(project_implicit: Path):
    pass


@pytest.mark.parametrize(["project_groups"], get_test_params("project.groups"))
@scenario(
    "../features/yaml_validation.feature",
    "validate project.groups",
)
def test_validate_project_groups(project_groups: Path):
    pass


@pytest.mark.parametrize(["project_implicit"], get_test_params("project.implicit"))
@scenario(
    "../features/yaml_validation.feature",
    "validate implicit project.groups",
)
def test_validate_project_groups_implicit(project_implicit: Path):
    pass


@pytest.mark.parametrize(["project_path"], get_test_params("project.path"))
@scenario(
    "../features/yaml_validation.feature",
    "validate project.path",
)
def test_validate_project_path(project_path: Path):
    pass


@pytest.mark.parametrize(["project_implicit"], get_test_params("project.implicit"))
@scenario(
    "../features/yaml_validation.feature",
    "validate implicit project.path",
)
def test_validate_project_path_implicit(project_implicit: Path):
    pass


@pytest.mark.parametrize(["project_remote"], get_test_params("project.remote"))
@scenario(
    "../features/yaml_validation.feature",
    "validate project.remote",
)
def test_validate_project_remote(project_remote: Path):
    pass


@pytest.mark.parametrize(["project_implicit"], get_test_params("project.implicit"))
@scenario(
    "../features/yaml_validation.feature",
    "validate implicit project.remote",
)
def test_validate_project_remote_implicit(project_implicit: Path):
    pass


@pytest.mark.parametrize(["project_source_protocol"], get_test_params("project.source.protocol"))
@scenario(
    "../features/yaml_validation.feature",
    "validate project.source.protocol",
)
def test_validate_project_source_protocol(project_source_protocol: Path):
    pass


@pytest.mark.parametrize(["project_implicit"], get_test_params("project.implicit"))
@scenario(
    "../features/yaml_validation.feature",
    "validate implicit project.source.protocol",
)
def test_validate_project_source_protocol_implicit(project_implicit: Path):
    pass


@pytest.mark.parametrize(["project_source_url"], get_test_params("project.source.url"))
@scenario(
    "../features/yaml_validation.feature",
    "validate project.source.url",
)
def test_validate_project_source_url(project_source_url: Path):
    pass


@pytest.mark.parametrize(["project_implicit"], get_test_params("project.implicit"))
@scenario(
    "../features/yaml_validation.feature",
    "validate implicit project.source.url",
)
def test_validate_project_source_url_implicit(project_implicit: Path):
    pass


@pytest.mark.parametrize(["project_tag"], get_test_params("project.tag"))
@scenario(
    "../features/yaml_validation.feature",
    "validate project.tag",
)
def test_validate_project_tag(project_tag: Path):
    pass


@pytest.mark.parametrize(["project_implicit"], get_test_params("project.implicit"))
@scenario(
    "../features/yaml_validation.feature",
    "validate implicit project.tag",
)
def test_validate_project_tag_implicit(project_implicit: Path):
    pass
