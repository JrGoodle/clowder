# -*- coding: utf-8 -*-
"""clowder.yaml validation

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import os
import sys

import clowder.util.formatting as fmt
from clowder import ROOT_DIR
from clowder.error.clowder_yaml_error import ClowderYAMLError
from clowder.yaml import __MAX_IMPORT_DEPTH__
from clowder.yaml.parsing import parse_yaml
from clowder.yaml.validation.defaults import (
    validate_yaml_defaults,
    validate_yaml_defaults_import
)
from clowder.yaml.validation.groups import (
    validate_yaml_groups_import,
    validate_yaml_groups
)
from clowder.yaml.validation.sources import validate_yaml_sources
from clowder.yaml.validation.util import (
    validate_clowder_yaml_contains_value,
    validate_required_dict,
    validate_optional_dict,
    validate_type
)


def validate_yaml(yaml_file, depth=__MAX_IMPORT_DEPTH__):
    """Validate clowder.yaml

    :param str yaml_file: Yaml file path to validate
    :param Optional[int] depth: Max depth of clowder.yaml imports
    :raise ClowderYAMLError:
    """

    parsed_yaml = parse_yaml(yaml_file)
    if depth < 0:
        raise ClowderYAMLError(fmt.recursive_import_error(__MAX_IMPORT_DEPTH__))

    if 'import' not in parsed_yaml:
        _validate_yaml(yaml_file)
        return

    _validate_yaml_import(yaml_file)
    imported_clowder = parsed_yaml['import']

    try:
        if imported_clowder == 'default':
            imported_yaml_file = os.path.join(ROOT_DIR, '.clowder', 'clowder.yaml')
        else:
            imported_yaml_file = os.path.join(ROOT_DIR, '.clowder', 'versions',
                                              imported_clowder, 'clowder.yaml')
        if not os.path.isfile(imported_yaml_file):
            raise ClowderYAMLError(fmt.missing_imported_yaml_error(imported_yaml_file, yaml_file))
        yaml_file = imported_yaml_file
        validate_yaml(yaml_file, depth=depth - 1)
    except ClowderYAMLError as err:
        raise ClowderYAMLError(err)
    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)


def _validate_yaml(yaml_file):
    """Validate clowder.yaml with no import

    :param str yaml_file: Path to yaml file
    :raise ClowderYAMLError:
    """

    parsed_yaml = parse_yaml(yaml_file)
    validate_type(parsed_yaml, fmt.yaml_file('clowder.yaml'), dict, 'dict', yaml_file)

    if not parsed_yaml:
        raise ClowderYAMLError(fmt.empty_yaml_error(yaml_file))

    validate_required_dict(parsed_yaml, 'defaults', validate_yaml_defaults, yaml_file)
    validate_required_dict(parsed_yaml, 'sources', validate_yaml_sources, yaml_file)
    validate_required_dict(parsed_yaml, 'groups', validate_yaml_groups, yaml_file)

    if parsed_yaml:
        raise ClowderYAMLError(fmt.unknown_entry_error(fmt.yaml_file('clowder.yaml'), parsed_yaml, yaml_file))


def _validate_yaml_import(yaml_file):
    """Validate clowder.yaml with an import

    :param str yaml_file: Path to yaml file
    :raise ClowderYAMLError:
    """

    parsed_yaml = parse_yaml(yaml_file)
    validate_type(parsed_yaml, fmt.yaml_file('clowder.yaml'), dict, 'dict', yaml_file)

    validate_clowder_yaml_contains_value(parsed_yaml, 'import', yaml_file)
    validate_type(parsed_yaml['import'], 'import', str, 'str', yaml_file)
    del parsed_yaml['import']

    if not parsed_yaml:
        raise ClowderYAMLError(fmt.empty_yaml_error(yaml_file))

    validate_optional_dict(parsed_yaml, 'defaults', validate_yaml_defaults_import, yaml_file)
    validate_optional_dict(parsed_yaml, 'sources', validate_yaml_sources, yaml_file)
    validate_optional_dict(parsed_yaml, 'groups', validate_yaml_groups_import, yaml_file)

    if parsed_yaml:
        raise ClowderYAMLError(fmt.unknown_entry_error(fmt.yaml_file('clowder.yaml'), parsed_yaml, yaml_file))
