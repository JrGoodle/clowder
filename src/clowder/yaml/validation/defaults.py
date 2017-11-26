# -*- coding: utf-8 -*-
"""clowder.yaml defaults validation

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

from clowder.yaml.validation.util import (
    validate_depth,
    validate_empty,
    validate_not_empty,
    validate_optional_bool,
    validate_optional_string,
    validate_optional_protocol,
    validate_optional_ref,
    validate_required_protocol,
    validate_required_ref,
    validate_required_string,
    validate_type
)


def validate_yaml_defaults_import(defaults, yaml_file):
    """Validate clowder.yaml defaults with an import

    :param dict defaults: Parsed YAML python object for defaults
    :param str yaml_file: Path to yaml file
    """

    validate_type(defaults, 'defaults', dict, 'dict', yaml_file)
    validate_depth(defaults, yaml_file)
    validate_optional_ref(defaults, yaml_file)
    validate_optional_protocol(defaults, yaml_file)
    validate_optional_bool(defaults, 'recursive', yaml_file)
    args = ['remote', 'source', 'timestamp_author']
    for arg in args:
        validate_optional_string(defaults, arg, yaml_file)

    validate_empty(defaults, 'defaults', yaml_file)


def validate_yaml_defaults(defaults, yaml_file):
    """Validate defaults in clowder loaded from yaml file

    :param dict defaults: Parsed YAML python object for defaults
    :param str yaml_file: Path to yaml file
    """

    validate_type(defaults, 'defaults', dict, 'dict', yaml_file)
    validate_not_empty(defaults, 'defaults', yaml_file)
    validate_required_ref(defaults, yaml_file)
    validate_required_protocol(defaults, yaml_file)
    validate_required_string(defaults, 'defaults', 'remote', yaml_file)
    validate_required_string(defaults, 'defaults', 'source', yaml_file)

    validate_depth(defaults, yaml_file)
    validate_optional_bool(defaults, 'recursive', yaml_file)
    validate_optional_string(defaults, 'timestamp_author', yaml_file)

    validate_empty(defaults, 'defaults', yaml_file)
