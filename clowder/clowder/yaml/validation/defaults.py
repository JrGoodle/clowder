# -*- coding: utf-8 -*-
"""clowder.yaml defaults validation

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import clowder.util.formatting as fmt
from clowder.error.clowder_error import ClowderError
from clowder.yaml.util import (
    override_import_value,
    validate_optional_value,
    dict_contains_value,
    validate_ref_type,
    validate_optional_ref,
    validate_required_value,
    validate_type,
    validate_type_depth
)


def load_yaml_import_defaults(imported_defaults, defaults):
    """Load clowder projects from imported group

    :param dict imported_defaults: Parsed YAML python object for imported defaults
    :param dict defaults: Parsed YAML python object for defaults
    :return:
    """

    override_import_value(defaults, imported_defaults, 'recursive')
    override_import_value(defaults, imported_defaults, 'ref')
    override_import_value(defaults, imported_defaults, 'remote')
    override_import_value(defaults, imported_defaults, 'source')
    override_import_value(defaults, imported_defaults, 'depth')
    override_import_value(defaults, imported_defaults, 'timestamp_author')


def validate_yaml_import_defaults(defaults, yaml_file):
    """Validate clowder.yaml defaults with an import

    :param dict defaults: Parsed YAML python object for defaults
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    validate_type(defaults, 'defaults', dict, 'dict', yaml_file)
    validate_optional_ref(defaults, yaml_file)
    validate_optional_value(defaults, 'recursive', bool, 'bool', yaml_file)
    validate_optional_value(defaults, 'remote', str, 'str', yaml_file)
    validate_optional_value(defaults, 'source', str, 'str', yaml_file)
    validate_optional_value(defaults, 'timestamp_author', str, 'str', yaml_file)

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

    validate_required_value(defaults, 'defaults', 'remote', str, 'str', yaml_file)
    validate_required_value(defaults, 'defaults', 'source', str, 'str', yaml_file)

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

    validate_optional_value(defaults, 'recursive', bool, 'bool', yaml_file)
    validate_optional_value(defaults, 'timestamp_author', str, 'str', yaml_file)
