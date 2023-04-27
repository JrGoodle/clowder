"""New syntax test file"""

import glob
import os
from pathlib import Path
from typing import List

import pygoodle.filesystem as fs
from pygoodle.format import Format

tests_dir = Path(__file__).resolve().parent.parent.resolve()
clowder_project_tests = [
    "clowder.group.project",
    "clowder.group.projects.project",
    "clowder.project"
]
clowder_upstream_tests = [
    "clowder.group.project.upstream",
    "clowder.group.projects.project.upstream",
    "clowder.project.upstream"
]
project_prefix = "project."
upstream_prefix = "upstream."
base_suffix = "-base"
ds_store = ".DS_Store"


def should_remove_base(prop: str) -> bool:
    return prop == "upstream.source.protocol"


def should_remove_non_base(prop: str) -> bool:
    return prop == "upstream.source.protocol-base"


def yaml_property_tests(yaml_property: str) -> List[str]:
    if yaml_property.startswith(project_prefix):
        tests = clowder_project_tests
        prop = Format.remove_prefix(yaml_property, project_prefix)
    elif yaml_property.startswith(upstream_prefix):
        tests = clowder_upstream_tests
        prop = Format.remove_prefix(yaml_property, upstream_prefix)
    else:
        assert False
    prop = Format.remove_suffix(prop, base_suffix)

    files: List[Path] = []
    yaml_dir = tests_dir / "data" / "yaml"
    for test in tests:
        test_dir = yaml_dir / test
        for test_type in ["dict", "string"]:
            type_dir = test_dir / test_type
            files += glob.glob(f"{type_dir / prop}*")
            sources_dir = type_dir / "sources"
            files += glob.glob(f"{sources_dir / prop}*")

    names = []
    for file in files:
        relative_path = Path(file).relative_to(yaml_dir)
        name = str(relative_path).replace("/", "-")
        if should_remove_base(yaml_property) and "base" in name:
            continue
        if should_remove_non_base(yaml_property) and "base" not in name:
            continue
        names.append(name)

    return names


def yaml_property_test_files() -> List[Path]:
    yaml_dir = tests_dir / "data" / "yaml"
    paths: List[Path] = []
    clowder_tests = clowder_project_tests + clowder_upstream_tests
    for test in clowder_tests:
        test_dir = yaml_dir / test
        for test_type in ["dict", "string"]:
            type_dir = test_dir / test_type
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
    files = yaml_property_test_files()
    for file in files:
        relative_path = file.relative_to(yaml_dir)
        name = str(relative_path).replace("/", "-")
        clowder_dir = path / name
        clowder_dir.mkdir()
        clowder_repo = clowder_dir / ".clowder"
        clowder_repo.mkdir()
        clowder_yml = clowder_repo / "clowder.yml"
        fs.copy_file(file, clowder_yml)
    return path
