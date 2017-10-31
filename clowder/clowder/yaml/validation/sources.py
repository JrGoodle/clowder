# -*- coding: utf-8 -*-
"""clowder.yaml sources validation

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

from clowder.yaml.validation.util import (
    validate_empty,
    validate_not_empty,
    validate_required_string,
    validate_type
)


def validate_yaml_sources(sources, yaml_file):
    """Validate sources in clowder loaded from yaml file

    :param dict sources: Parsed YAML python object for sources
    :param str yaml_file: Path to yaml file
    """

    validate_type(sources, 'sources', list, 'list', yaml_file)
    validate_not_empty(sources, 'sources', yaml_file)

    for source in sources:
        validate_type(source, 'source', dict, 'dict', yaml_file)
        validate_not_empty(source, 'source', yaml_file)

        args = ['name', 'url']
        for arg in args:
            validate_required_string(source, 'source', arg, yaml_file)

        validate_empty(source, 'source', yaml_file)
