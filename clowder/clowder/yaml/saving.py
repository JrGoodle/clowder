# -*- coding: utf-8 -*-
"""clowder.yaml parsing and validation functionality

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import os
import sys

import yaml

import clowder.util.formatting as fmt


def save_yaml(yaml_output, yaml_file):
    """Save yaml file to disk

    :param dict yaml_output: Parsed YAML python object
    :param str yaml_file: Path to save yaml file
    :return:
    """

    if os.path.isfile(yaml_file):
        print(fmt.file_exists_error(yaml_file) + '\n')
        sys.exit(1)

    try:
        with open(yaml_file, 'w') as raw_file:
            print(" - Save yaml to file")
            yaml.safe_dump(yaml_output, raw_file, default_flow_style=False, indent=4)
    except yaml.YAMLError:
        print(fmt.save_file_error(yaml_file))
        sys.exit(1)
    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)
