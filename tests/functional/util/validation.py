"""New syntax test file"""

import glob
import os
from pathlib import Path
from typing import List

from .file_system import copy_file
from .formatting import remove_prefix

tests_dir = Path(__file__).resolve().parent.parent.resolve()
clowder_projects = [
    "clowder.group.project",
    "clowder.group.projects",
    "clowder.project"
]
project_prefix = "project."
upstream_prefix = "upstream."
ds_store = ".DS_Store"


def yaml_property_tests(yaml_property: str) -> List[str]:
    yaml_dir = tests_dir / "data" / "yaml"
    prop = remove_prefix(yaml_property, project_prefix)
    files: List[Path] = []
    if yaml_property.startswith(project_prefix):
        for project in clowder_projects:
            project_dir = yaml_dir / project
            for project_type in ["dict", "string"]:
                type_dir = project_dir / project_type
                files += glob.glob(f"{type_dir / prop}*")
                sources_dir = type_dir / "sources"
                files += glob.glob(f"{sources_dir / prop}*")
    else:
        assert False

    names = []
    for file in files:
        relative_path = Path(file).relative_to(yaml_dir)
        name = str(relative_path).replace("/", "-")
        names.append(name)
    return names


def yaml_project_property_test_files() -> List[Path]:
    yaml_dir = tests_dir / "data" / "yaml"
    paths: List[Path] = []
    for project in clowder_projects:
        project_dir = yaml_dir / project
        for project_type in ["dict", "string"]:
            type_dir = project_dir / project_type
            files = os.listdir(type_dir)
            files.remove("sources")
            if ds_store in files:
                files.remove(ds_store)
            paths += [type_dir / f for f in files]

            sources_dir = type_dir / "sources"
            files = os.listdir(sources_dir)
            if ds_store in files:
                files.remove(ds_store)
            paths += [sources_dir / f for f in files]

    return paths


def create_yaml_validation_clowders(path: Path) -> Path:
    yaml_dir = tests_dir / "data" / "yaml"
    files = yaml_project_property_test_files()
    for file in files:
        relative_path = file.relative_to(yaml_dir)
        name = str(relative_path).replace("/", "-")
        clowder_dir = path / name
        clowder_dir.mkdir()
        clowder_repo = clowder_dir / ".clowder"
        clowder_repo.mkdir()
        clowder_yml = clowder_repo / "clowder.yml"
        copy_file(file, clowder_yml)
    return path
