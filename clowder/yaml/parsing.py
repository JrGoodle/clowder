"""Clowder yaml parsing"""

import os
import sys
import yaml

import clowder.utility.formatting as fmt


def parse_yaml(yaml_file):
    """Parse yaml file"""
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
            fmt.open_file_error(yaml_file)
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)
    else:
        print()
        print(fmt.missing_yaml_error())
        print()
        sys.exit(1)
