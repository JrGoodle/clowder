# -*- coding: utf-8 -*-
"""clowder.yaml validation

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import clowder.util.formatting as fmt
from clowder.error.clowder_error import ClowderError
from clowder.yaml.parsing import parse_yaml
from clowder.yaml.util import (
    clowder_yaml_contains_value,
    validate_type
)
from clowder.yaml.validation.defaults import (
    validate_yaml_defaults,
    validate_yaml_import_defaults
)
from clowder.yaml.validation.groups import (
    validate_yaml_import_groups,
    validate_yaml_groups
)
from clowder.yaml.validation.sources import validate_yaml_sources


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

    clowder_yaml_contains_value(parsed_yaml, 'defaults', yaml_file)
    validate_yaml_defaults(parsed_yaml['defaults'], yaml_file)
    del parsed_yaml['defaults']

    clowder_yaml_contains_value(parsed_yaml, 'sources', yaml_file)
    validate_yaml_sources(parsed_yaml['sources'], yaml_file)
    del parsed_yaml['sources']

    clowder_yaml_contains_value(parsed_yaml, 'groups', yaml_file)
    validate_yaml_groups(parsed_yaml['groups'], yaml_file)
    del parsed_yaml['groups']

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

    clowder_yaml_contains_value(parsed_yaml, 'import', yaml_file)
    validate_type(parsed_yaml['import'], 'import', str, 'str', yaml_file)
    del parsed_yaml['import']

    if not parsed_yaml:
        error = fmt.empty_yaml_error(yaml_file)
        raise ClowderError(error)

    if 'defaults' in parsed_yaml:
        validate_yaml_import_defaults(parsed_yaml['defaults'], yaml_file)
        del parsed_yaml['defaults']

    if 'sources' in parsed_yaml:
        validate_yaml_sources(parsed_yaml['sources'], yaml_file)
        del parsed_yaml['sources']

    if 'groups' in parsed_yaml:
        validate_yaml_import_groups(parsed_yaml['groups'], yaml_file)
        del parsed_yaml['groups']

    if parsed_yaml:
        error = fmt.unknown_entry_error(fmt.yaml_file('clowder.yaml'), parsed_yaml, yaml_file)
        raise ClowderError(error)
