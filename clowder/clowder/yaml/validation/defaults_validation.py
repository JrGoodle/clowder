# -*- coding: utf-8 -*-
"""clowder.yaml parsing and validation functionality

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import clowder.util.formatting as fmt
from clowder.error.clowder_error import ClowderError
from clowder.yaml.util import (
    dict_contains_value,
    validate_ref_type,
    validate_optional_ref,
    validate_type,
    validate_type_depth
)


def load_yaml_import_defaults(imported_defaults, defaults):
    """Load clowder projects from imported group

    :param dict imported_defaults: Parsed YAML python object for imported defaults
    :param dict defaults: Parsed YAML python object for defaults
    :return:
    """

    if 'recursive' in imported_defaults:
        defaults['recursive'] = imported_defaults['recursive']
    if 'ref' in imported_defaults:
        defaults['ref'] = imported_defaults['ref']
    if 'remote' in imported_defaults:
        defaults['remote'] = imported_defaults['remote']
    if 'source' in imported_defaults:
        defaults['source'] = imported_defaults['source']
    if 'depth' in imported_defaults:
        defaults['depth'] = imported_defaults['depth']
    if 'timestamp_author' in imported_defaults:
        defaults['timestamp_author'] = imported_defaults['timestamp_author']


def validate_yaml_import_defaults(defaults, yaml_file):
    """Validate clowder.yaml defaults with an import

    :param dict defaults: Parsed YAML python object for defaults
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    validate_type(defaults, 'defaults', dict, 'dict', yaml_file)
    if 'recursive' in defaults:
        validate_type(defaults['recursive'], 'recursive', bool, 'bool', yaml_file)
        del defaults['recursive']

    validate_optional_ref(defaults, yaml_file)

    if 'remote' in defaults:
        validate_type(defaults['remote'], 'remote', str, 'str', yaml_file)
        del defaults['remote']

    if 'source' in defaults:
        validate_type(defaults['source'], 'source', str, 'str', yaml_file)
        del defaults['source']

    if 'depth' in defaults:
        validate_type_depth(defaults['depth'], yaml_file)
        del defaults['depth']

    if 'timestamp_author' in defaults:
        validate_type(defaults['timestamp_author'], 'timestamp_author', str, 'str', yaml_file)
        del defaults['timestamp_author']

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

    dict_contains_value(defaults, 'defaults', 'remote', yaml_file)
    validate_type(defaults['remote'], 'remote', str, 'str', yaml_file)
    del defaults['remote']

    dict_contains_value(defaults, 'defaults', 'source', yaml_file)
    validate_type(defaults['source'], 'source', str, 'str', yaml_file)
    del defaults['source']

    validate_yaml_defaults_optional(defaults, yaml_file)

    if defaults:
        error = fmt.unknown_entry_error('defaults', defaults, yaml_file)
        raise ClowderError(error)


def validate_yaml_defaults_optional(defaults, yaml_file):
    """Validate defaults optional args in clowder loaded from yaml file

    :param dict defaults: Parsed YAML python object for defaults
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    if 'depth' in defaults:
        validate_type_depth(defaults['depth'], yaml_file)
        del defaults['depth']

    if 'recursive' in defaults:
        validate_type(defaults['recursive'], 'recursive', bool, 'bool', yaml_file)
        del defaults['recursive']

    if 'timestamp_author' in defaults:
        validate_type(defaults['timestamp_author'], 'timestamp_author', str, 'str', yaml_file)
        del defaults['timestamp_author']
