# -*- coding: utf-8 -*-
"""clowder.yaml defaults validation

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import clowder.util.formatting as fmt
from clowder.error.clowder_error import ClowderError
from clowder.yaml.util import (
    validate_optional_bool,
    validate_optional_string,
    dict_contains_value,
    validate_ref_type,
    validate_optional_ref,
    validate_required_string,
    validate_type,
    validate_type_depth
)


def validate_yaml_import_defaults(defaults, yaml_file):
    """Validate clowder.yaml defaults with an import

    :param dict defaults: Parsed YAML python object for defaults
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    validate_type(defaults, 'defaults', dict, 'dict', yaml_file)
    validate_optional_ref(defaults, yaml_file)
    validate_optional_bool(defaults, 'recursive', yaml_file)
    validate_optional_string(defaults, 'remote', yaml_file)
    validate_optional_string(defaults, 'source', yaml_file)
    validate_optional_string(defaults, 'timestamp_author', yaml_file)

    if 'depth' in defaults:
        validate_type_depth(defaults['depth'], yaml_file)
        del defaults['depth']

    if defaults:
        error = fmt.unknown_entry_error('defaults', defaults, yaml_file)
        raise ClowderError(error)


def validate_yaml_defaults(defaults, yaml_file):
    """Validate defaults in clowder loaded from yaml file

    :param dict defaults: Parsed YAML python object for defaults
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    validate_type(defaults, 'defaults', dict, 'dict', yaml_file)
    if not defaults:
        error = fmt.missing_entries_error('defaults', yaml_file)
        raise ClowderError(error)

    dict_contains_value(defaults, 'defaults', 'ref', yaml_file)
    validate_type(defaults['ref'], 'ref', str, 'str', yaml_file)
    validate_ref_type(defaults, yaml_file)
    del defaults['ref']

    validate_required_string(defaults, 'defaults', 'remote', yaml_file)
    validate_required_string(defaults, 'defaults', 'source', yaml_file)

    if 'depth' in defaults:
        validate_type_depth(defaults['depth'], yaml_file)
        del defaults['depth']

    validate_optional_bool(defaults, 'recursive', yaml_file)
    validate_optional_string(defaults, 'timestamp_author', yaml_file)

    if defaults:
        error = fmt.unknown_entry_error('defaults', defaults, yaml_file)
        raise ClowderError(error)
