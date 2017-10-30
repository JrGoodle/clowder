# -*- coding: utf-8 -*-
"""clowder.yaml sources validation

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import clowder.util.formatting as fmt
from clowder.error.clowder_error import ClowderError
from clowder.yaml.util import (
    dict_contains_value,
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
    if not sources:
        error = fmt.missing_entries_error('sources', yaml_file)
        raise ClowderError(error)

    for source in sources:
        validate_type(source, 'source', dict, 'dict', yaml_file)
        if not source:
            error = fmt.missing_entries_error('source', yaml_file)
            raise ClowderError(error)

        dict_contains_value(source, 'source', 'name', yaml_file)
        validate_type(source['name'], 'name', str, 'str', yaml_file)
        del source['name']

        dict_contains_value(source, 'source', 'url', yaml_file)
        validate_type(source['url'], 'url', str, 'str', yaml_file)
        del source['url']

        if source:
            error = fmt.unknown_entry_error('source', source, yaml_file)
            raise ClowderError(error)
