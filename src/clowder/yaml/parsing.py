# -*- coding: utf-8 -*-
"""clowder.yaml parsing

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import os

import yaml

import clowder.util.formatting as fmt
from clowder.error.clowder_exit import ClowderExit
from clowder.error.clowder_yaml_error import ClowderYAMLError


def parse_yaml(yaml_file):
    """Parse yaml file

    :param str yaml_file: Path to yaml file
    :return: YAML python object
    :rtype: dict
    Raises:
        ClowderExit
        ClowderYAMLError
    """

    if not os.path.isfile(yaml_file):
        raise ClowderYAMLError(fmt.missing_yaml_error())

    try:
        with open(yaml_file) as raw_file:
            parsed_yaml = yaml.safe_load(raw_file)
            if parsed_yaml is None:
                raise ClowderYAMLError(fmt.empty_yaml_error(yaml_file))
            return parsed_yaml
    except yaml.YAMLError:
        raise ClowderYAMLError(fmt.open_file_error(yaml_file))
    except (KeyboardInterrupt, SystemExit):
        raise ClowderExit(1)
