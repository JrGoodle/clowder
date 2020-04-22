# -*- coding: utf-8 -*-
"""clowder.yaml forks validation

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from clowder.yaml.validation.util import (
    validate_empty,
    validate_not_empty,
    validate_optional_ref,
    validate_optional_string,
    validate_required_string,
    validate_type
)


def validate_yaml_fork(fork: dict, yaml_file: str) -> None:
    """Validate fork in clowder loaded from yaml file

    :param dict fork: Parsed YAML python object for fork
    :param str yaml_file: Path to yaml file
    """

    validate_type(fork, 'fork', dict, 'dict', yaml_file)
    validate_not_empty(fork, 'fork', yaml_file)

    args = ['name', 'remote']
    for arg in args:
        validate_required_string(fork, 'fork', arg, yaml_file)

    validate_optional_string(fork, 'source', yaml_file)
    validate_optional_ref(fork, yaml_file)

    validate_empty(fork, 'fork', yaml_file)
