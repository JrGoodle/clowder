# -*- coding: utf-8 -*-
"""clowder.yaml validation

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import clowder.util.formatting as fmt
from clowder.error.clowder_error import ClowderError
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


def validate_yaml(yaml_file):
    """Validate clowder.yaml with no import

    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    parsed_yaml = parse_yaml(yaml_file)
    validate_type(parsed_yaml, fmt.yaml_file('clowder.yaml'), dict, 'dict', yaml_file)

    if not parsed_yaml:
        error = fmt.empty_yaml_error(yaml_file)
        raise ClowderError(error)

    validate_required_dict(parsed_yaml, 'defaults', validate_yaml_defaults, yaml_file)
    validate_required_dict(parsed_yaml, 'sources', validate_yaml_sources, yaml_file)
    validate_required_dict(parsed_yaml, 'groups', validate_yaml_groups, yaml_file)

    if parsed_yaml:
        error = fmt.unknown_entry_error(fmt.yaml_file('clowder.yaml'), parsed_yaml, yaml_file)
        raise ClowderError(error)


def validate_yaml_import(yaml_file):
    """Validate clowder.yaml with an import

    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    parsed_yaml = parse_yaml(yaml_file)
    validate_type(parsed_yaml, fmt.yaml_file('clowder.yaml'), dict, 'dict', yaml_file)

    validate_clowder_yaml_contains_value(parsed_yaml, 'import', yaml_file)
    validate_type(parsed_yaml['import'], 'import', str, 'str', yaml_file)
    del parsed_yaml['import']

    if not parsed_yaml:
        error = fmt.empty_yaml_error(yaml_file)
        raise ClowderError(error)

    validate_optional_dict(parsed_yaml, 'defaults', validate_yaml_defaults_import, yaml_file)
    validate_optional_dict(parsed_yaml, 'sources', validate_yaml_sources, yaml_file)
    validate_optional_dict(parsed_yaml, 'groups', validate_yaml_groups_import, yaml_file)

    if parsed_yaml:
        error = fmt.unknown_entry_error(fmt.yaml_file('clowder.yaml'), parsed_yaml, yaml_file)
        raise ClowderError(error)
