# -*- coding: utf-8 -*-
"""clowder.yaml sources validation

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

from clowder.yaml.util import (
    validate_empty,
    validate_not_empty,
    validate_required_string,
    validate_type
)


def load_yaml_import_sources(imported_sources, sources):
    """Load clowder sources from imported yaml

    :param dict imported_sources: Parsed YAML python object for imported sources
    :param dict sources: Parsed YAML python object for sources
    :return:
    """

    source_names = [s['name'] for s in sources]
    for imported_source in imported_sources:
        if imported_source['name'] not in source_names:
            sources.append(imported_source)
            continue
        combined_sources = []
        for source in sources:
            if source.name == imported_source['name']:
                combined_sources.append(imported_source)
            else:
                combined_sources.append(source)
        sources = combined_sources


def validate_yaml_sources(sources, yaml_file):
    """Validate sources in clowder loaded from yaml file

    :param dict sources: Parsed YAML python object for sources
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
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
