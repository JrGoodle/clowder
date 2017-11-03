# -*- coding: utf-8 -*-
"""clowder.yaml parsing

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import os
import sys

import yaml

import clowder.util.formatting as fmt
from clowder.error.clowder_error import ClowderError


def parse_yaml(yaml_file):
    """Parse yaml file

    :param str yaml_file: Path to yaml file
    :return: YAML python object
    :rtype: dict
    """

    if os.path.isfile(yaml_file):
        try:
            with open(yaml_file) as raw_file:
                parsed_yaml = yaml.safe_load(raw_file)
                if parsed_yaml is None:
                    print(fmt.invalid_yaml_error())
                    print(fmt.empty_yaml_error(yaml_file) + '\n')
                    sys.exit(1)
                return parsed_yaml
        except yaml.YAMLError:
            print(fmt.open_file_error(yaml_file))
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)
    else:
        raise ClowderError('\n' + fmt.missing_yaml_error() + '\n')
