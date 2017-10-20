"""Clowder yaml saving"""

import os
import sys
import yaml

import clowder.utility.formatting as fmt


def save_yaml(yaml_output, yaml_file):
    """Save yaml file to disk"""
    if not os.path.isfile(yaml_file):
        try:
            with open(yaml_file, 'w') as raw_file:
                print(" - Save yaml to file")
                yaml.safe_dump(yaml_output, raw_file, default_flow_style=False, indent=4)
        except yaml.YAMLError:
            fmt.save_file_error(yaml_file)
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)
    else:
        fmt.file_exists_error(yaml_file)
        print()
        sys.exit(1)
