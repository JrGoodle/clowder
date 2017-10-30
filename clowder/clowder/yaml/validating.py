# -*- coding: utf-8 -*-
"""clowder.yaml validation

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import os
import sys

import clowder.util.formatting as fmt
from clowder.error.clowder_error import ClowderError
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


def validate_yaml(yaml_file, root_directory, depth=__MAX_IMPORT_DEPTH__):
    """Validate clowder.yaml

    :param str yaml_file: Yaml file path to validate
    :param str root_directory: Clowder projects root directory
    :param Optional[int] depth: Max depth of clowder.yaml imports
    :return:
    """

    parsed_yaml = parse_yaml(yaml_file)
    if depth < 0:
        print(fmt.invalid_yaml_error())
        print(fmt.recursive_import_error(__MAX_IMPORT_DEPTH__) + '\n')
        sys.exit(1)

    if 'import' not in parsed_yaml:
        _validate_yaml(yaml_file)
        return

    _validate_yaml_import(yaml_file)
    imported_clowder = parsed_yaml['import']

    try:
        if imported_clowder == 'default':
            imported_yaml_file = os.path.join(root_directory, '.clowder', 'clowder.yaml')
        else:
            imported_yaml_file = os.path.join(root_directory, '.clowder', 'versions',
                                              imported_clowder, 'clowder.yaml')
        if not os.path.isfile(imported_yaml_file):
            error = fmt.missing_imported_yaml_error(imported_yaml_file, yaml_file)
            raise ClowderError(error)
        yaml_file = imported_yaml_file
        validate_yaml(yaml_file, root_directory, depth=depth - 1)
    except ClowderError as err:
        print(fmt.invalid_yaml_error())
        print(fmt.error(err))
        sys.exit(1)
    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)


def _validate_yaml(yaml_file):
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


def _validate_yaml_import(yaml_file):
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
