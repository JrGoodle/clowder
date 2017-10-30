# -*- coding: utf-8 -*-
"""clowder.yaml parsing and validation functionality

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import clowder.util.formatting as fmt
from clowder.error.clowder_error import ClowderError


def clowder_yaml_contains_value(parsed_yaml, value, yaml_file):
    """Check whether yaml file contains value

    :param dict parsed_yaml: Parsed YAML python object
    :param str value: Name of entry to check
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    if value not in parsed_yaml:
        error = fmt.missing_entry_error(value, fmt.yaml_file('clowder.yaml'), yaml_file)
        raise ClowderError(error)


def dict_contains_value(dictionary, name, value, yaml_file):
    """Check whether yaml file contains value

    :param dict dictionary: Parsed YAML python object
    :param str name: Name of entry to print if missing
    :param str value: Name of entry to check
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """
    if value not in dictionary:
        error = fmt.missing_entry_error(value, name, yaml_file)
        raise ClowderError(error)


def validate_optional_ref(dictionary, yaml_file):
    """Check whether ref type is valid

    :param dict dictionary: Parsed YAML python object
    :param str yaml_file: Path to yaml file
    :return:
    """
    if 'ref' in dictionary:
        validate_type(dictionary['ref'], 'ref', str, 'str', yaml_file)
        validate_ref_type(dictionary, yaml_file)
        del dictionary['ref']


def valid_ref_type(ref):
    """Validate that ref is formatted correctly

    :param str ref: Ref string requiring format 'refs/heads/<branch>', 'refs/tags/<tag>', or 40 character commit sha
    :return: True, if ref is properly formatted
    :rtype: bool
    """

    git_branch = "refs/heads/"
    git_tag = "refs/tags/"
    if ref.startswith(git_branch):
        return True
    elif ref.startswith(git_tag):
        return True
    elif len(ref) == 40:
        return True
    return False


def validate_ref_type(dictionary, yaml_file):
    """Check whether ref type is valid

    :param dict dictionary: Parsed YAML python object
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """
    if not valid_ref_type(dictionary['ref']):
        error = fmt.invalid_ref_error(dictionary['ref'], yaml_file)
        raise ClowderError(error)


def validate_type_depth(value, yaml_file):
    """Validate depth value

    :param int value: Integer depth value
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    error = fmt.depth_error(value, yaml_file)
    if not isinstance(value, int):
        raise ClowderError(error)
    if int(value) < 0:
        raise ClowderError(error)


def validate_type(value, name, classinfo, type_name, yaml_file):
    """Validate value type

    :param value: Value to check
    :param str name: Name of value to print if invalid
    :param type classinfo: Type to check
    :param str type_name: Name of type to print if invalid
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    if not isinstance(value, classinfo):
        error = fmt.type_error(name, yaml_file, type_name)
        raise ClowderError(error)
