# -*- coding: utf-8 -*-
"""clowder.yaml utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import Any, Callable, List, Optional

import clowder.util.formatting as fmt
from clowder.error.clowder_yaml_error import ClowderYAMLError, ClowderYAMLYErrorType


def validate_required_dict(dictionary: dict, value: str, func: Callable, yaml_file: str) -> None:
    """Check whether yaml file contains required value

    :param dict dictionary: Parsed YAML python object
    :param str value: Name of entry to check
    :param callable func: Function to call to validate dict entries
    :param str yaml_file: Path to yaml file
    """

    _validate_clowder_yaml_contains_value(dictionary, value, yaml_file)
    func(dictionary[value], yaml_file)
    del dictionary[value]


def validate_type(value: Any, name: str, classinfo: type, type_name: str, yaml_file: str) -> None:
    """Validate value type

    :param value: Value to check
    :param str name: Name of value to print if invalid
    :param type classinfo: Type to check
    :param str type_name: Name of type to print if invalid
    :param str yaml_file: Path to yaml file
    :raise ClowderYAMLError:
    """

    if not isinstance(value, classinfo):
        raise ClowderYAMLError(fmt.type_error(name, yaml_file, type_name), ClowderYAMLYErrorType.TYPE)


def validate_yaml_contents(yaml: dict, yaml_file: str) -> None:
    """Validate contents in clowder loaded from yaml file

    :param dict yaml: Parsed YAML python object
    :param str yaml_file: Path to yaml file
    """

    sources = []
    for source in yaml['sources']:
        sources.append(source['name'])

    defaults = yaml['defaults']
    # Validate default source is defined in sources
    if defaults['source'] not in sources:
        raise ClowderYAMLError(fmt.source_default_not_found_error(defaults['source'], yaml_file),
                               ClowderYAMLYErrorType.SOURCE_NOT_FOUND)

    projects = []
    projects_with_forks = []
    for p in yaml['projects']:
        project = {'name': p['name'],
                   'path': p['path'] if 'path' in p else p['name']}
        if 'remote' in p:
            project['remote'] = p['remote']
        if 'source' in p:
            # Validate custom project source is defined in sources
            if p['source'] not in sources:
                raise ClowderYAMLError(fmt.source_not_found_error(p['source'], yaml_file, project['name']),
                                       ClowderYAMLYErrorType.SOURCE_NOT_FOUND)
        projects.append(project)
        if 'fork' in p:
            f = p['fork']
            fork = {'name': f['name']}
            if 'remote' in f:
                fork['remote'] = f['remote']
            if 'source' in f:
                # Validate custom fork source is defined in sources
                if f['source'] not in sources:
                    raise ClowderYAMLError(fmt.source_not_found_error(f['source'], yaml_file, project['name']),
                                           ClowderYAMLYErrorType.SOURCE_NOT_FOUND)
            project['fork'] = fork
            projects_with_forks.append(project)

    # Validate projects and forks have different remote names
    for project in projects_with_forks:
        fork = project['fork']
        default_remote = defaults['remote']
        if 'remote' in project and 'remote' in fork:
            if project['remote'] == fork['remote']:
                message = fmt.remote_name_error(fork['name'], project['name'], project['remote'], yaml_file)
                raise ClowderYAMLError(message, ClowderYAMLYErrorType.REMOTE_NAME)
        elif 'remote' in project:
            if project['remote'] == default_remote:
                message = fmt.remote_name_error(fork['name'], project['name'], default_remote, yaml_file)
                raise ClowderYAMLError(message, ClowderYAMLYErrorType.REMOTE_NAME)
        elif 'remote' in fork:
            if fork['remote'] == default_remote:
                message = fmt.remote_name_error(fork['name'], project['name'], default_remote, yaml_file)
                raise ClowderYAMLError(message, ClowderYAMLYErrorType.REMOTE_NAME)
        else:
            message = fmt.remote_name_error(fork['name'], project['name'], default_remote, yaml_file)
            raise ClowderYAMLError(message, ClowderYAMLYErrorType.REMOTE_NAME)

    # Validate projects don't share share directories
    paths = [p['path'] for p in projects]
    duplicate = _check_for_duplicates(paths)
    if duplicate is not None:
        message = fmt.duplicate_project_path_error(duplicate, yaml_file)
        raise ClowderYAMLError(message, ClowderYAMLYErrorType.DUPLICATE_PATH)

    # TODO: Validate projects have unique name/alias


def validate_yaml_defaults(defaults: dict, yaml_file: str) -> None:
    """Validate defaults in clowder loaded from yaml file

    :param dict defaults: Parsed YAML python object for defaults
    :param str yaml_file: Path to yaml file
    """

    validate_type(defaults, 'defaults', dict, 'dict', yaml_file)
    _validate_not_empty(defaults, 'defaults', yaml_file)
    _validate_required_ref(defaults, yaml_file)
    _validate_required_protocol(defaults, yaml_file)
    _validate_required_string(defaults, 'defaults', 'remote', yaml_file)
    _validate_required_string(defaults, 'defaults', 'source', yaml_file)

    _validate_depth(defaults, yaml_file)
    _validate_optional_bool(defaults, 'recursive', yaml_file)
    _validate_optional_string(defaults, 'timestamp_author', yaml_file)

    _validate_empty(defaults, 'defaults', yaml_file)


def validate_yaml_fork(fork: dict, yaml_file: str) -> None:
    """Validate fork in clowder loaded from yaml file

    :param dict fork: Parsed YAML python object for fork
    :param str yaml_file: Path to yaml file
    """

    validate_type(fork, 'fork', dict, 'dict', yaml_file)
    _validate_not_empty(fork, 'fork', yaml_file)

    _validate_required_string(fork, 'fork', 'name', yaml_file)

    args = ['source', 'remote']
    for arg in args:
        _validate_optional_string(fork, arg, yaml_file)

    _validate_optional_ref(fork, yaml_file)

    _validate_empty(fork, 'fork', yaml_file)


def validate_yaml_projects(projects: dict, yaml_file: str) -> None:
    """Validate projects in clowder loaded from yaml file

    :param dict projects: Parsed YAML python object for projects
    :param str yaml_file: Path to yaml file
    """

    validate_type(projects, 'projects', list, 'list', yaml_file)
    _validate_not_empty(projects, 'projects', yaml_file)

    for project in projects:
        validate_type(project, 'project', dict, 'dict', yaml_file)
        _validate_not_empty(project, 'project', yaml_file)

        _validate_required_string(project, 'project', 'name', yaml_file)
        _validate_required_string(project, 'project', 'path', yaml_file)

        args = ['remote', 'source', 'timestamp_author']
        for arg in args:
            _validate_optional_string(project, arg, yaml_file)

        _validate_optional_bool(project, 'recursive', yaml_file)
        _validate_optional_ref(project, yaml_file)
        _validate_optional_groups(project, yaml_file)

        _validate_depth(project, yaml_file)

        if 'fork' in project:
            validate_yaml_fork(project['fork'], yaml_file)
            del project['fork']

        _validate_empty(project, 'project', yaml_file)


def validate_yaml_sources(sources: dict, yaml_file: str) -> None:
    """Validate sources in clowder loaded from yaml file

    :param dict sources: Parsed YAML python object for sources
    :param str yaml_file: Path to yaml file
    """

    validate_type(sources, 'sources', list, 'list', yaml_file)
    _validate_not_empty(sources, 'sources', yaml_file)

    for source in sources:
        validate_type(source, 'source', dict, 'dict', yaml_file)
        _validate_not_empty(source, 'source', yaml_file)

        args = ['name', 'url']
        for arg in args:
            _validate_required_string(source, 'source', arg, yaml_file)

        _validate_optional_protocol(source, yaml_file)

        _validate_empty(source, 'source', yaml_file)


def _check_for_duplicates(list_of_elements: List[str]) -> Optional[str]:
    """Check if given list contains any duplicates

    :param List[str] list_of_elements: List of strings to check for duplicates
    :return: First duplicate encountered, or None if no duplicates found
    :rtype: Optional[str]
    """

    set_of_elements = set()
    for elem in list_of_elements:
        if elem in set_of_elements:
            return elem
        else:
            set_of_elements.add(elem)
    return None


def _is_valid_protocol_type(protocol: str) -> bool:
    """Validate that protocol is formatted correctly

    :param str protocol: Protocol can only take on the values of 'ssh' or 'https'
    :return: True, if protocol is properly formatted
    :rtype: bool
    """

    if protocol == 'ssh' or protocol == 'https':
        return True

    return False


def _is_valid_ref_type(ref: str) -> bool:
    """Validate that ref is formatted correctly

    :param str ref: Ref string requiring format 'refs/heads/<branch>', 'refs/tags/<tag>', or 40 character commit sha
    :return: True, if ref is properly formatted
    :rtype: bool
    """

    git_branch = "refs/heads/"
    git_tag = "refs/tags/"
    if ref.startswith(git_branch) or ref.startswith(git_tag) or len(ref) == 40:
        return True
    return False


def _validate_clowder_yaml_contains_value(parsed_yaml: dict, value: str, yaml_file: str) -> None:
    """Check whether yaml file contains value

    :param dict parsed_yaml: Parsed YAML python object
    :param str value: Name of entry to check
    :param str yaml_file: Path to yaml file
    :raise ClowderYAMLError:
    """

    if value not in parsed_yaml:
        raise ClowderYAMLError(fmt.missing_entry_error(value, fmt.yaml_file('clowder.yaml'), yaml_file),
                               ClowderYAMLYErrorType.MISSING_ENTRY)


def _validate_depth(dictionary: dict, yaml_file: str) -> None:
    """Validate depth

    :param dict dictionary: Parsed YAML python object
    :param str yaml_file: Path to yaml file
    """

    if 'depth' in dictionary:
        _validate_type_depth(dictionary['depth'], yaml_file)
        del dictionary['depth']


def _validate_dict_contains_value(dictionary: dict, dict_name: str, value: str, yaml_file: str) -> None:
    """Check whether yaml file contains value

    :param dict dictionary: Parsed YAML python object
    :param str dict_name: Name of dict to print if missing
    :param str value: Name of entry to check
    :param str yaml_file: Path to yaml file
    :raise ClowderYAMLError:
    """

    if value not in dictionary:
        raise ClowderYAMLError(fmt.missing_entry_error(value, dict_name, yaml_file),
                               ClowderYAMLYErrorType.MISSING_ENTRY)


def _validate_empty(collection: dict, name: str, yaml_file: str) -> None:
    """Check whether collection is not empty

    :param dict collection: Parsed YAML python object
    :param str name: Name of collection to print if empty
    :param str yaml_file: Path to yaml file
    :raise ClowderYAMLError:
    """

    if collection:
        raise ClowderYAMLError(fmt.unknown_entry_error(name, collection, yaml_file),
                               ClowderYAMLYErrorType.UNKNOWN_ENTRY)


def _validate_not_empty(collection: dict, name: str, yaml_file: str) -> None:
    """Check whether collection is empty

    :param dict collection: Parsed YAML python object
    :param str name: Name of collection to print if empty
    :param str yaml_file: Path to yaml file
    :raise ClowderYAMLError:
    """

    if not collection:
        raise ClowderYAMLError(fmt.missing_entries_error(name, yaml_file), ClowderYAMLYErrorType.MISSING_ENTRY)


def _validate_optional_groups(dictionary: dict, yaml_file: str) -> None:
    """Check whether yaml file contains optional groups

    :param dict dictionary: Parsed YAML python object
    :param str yaml_file: Path to yaml file
    """

    if 'groups' in dictionary:
        groups = dictionary['groups']
        validate_type(groups, 'groups', list, 'list', yaml_file)
        for group in groups:
            validate_type(group, 'group', str, 'str', yaml_file)
        if 'all' in groups:
            ClowderYAMLError(fmt.groups_contains_all_error(yaml_file), ClowderYAMLYErrorType.GROUPS_CONTAINS_ALL)
        # TODO: Check for duplicates in list
        del dictionary['groups']


def _validate_optional_protocol(dictionary: dict, yaml_file: str) -> None:
    """Check whether protocol type is valid

    :param dict dictionary: Parsed YAML python object
    :param str yaml_file: Path to yaml file
    """

    if 'protocol' in dictionary:
        validate_type(dictionary['protocol'], 'protocol', str, 'str', yaml_file)
        _validate_protocol_type(dictionary, yaml_file)
        del dictionary['protocol']


def _validate_optional_ref(dictionary: dict, yaml_file: str) -> None:
    """Check whether ref type is valid

    :param dict dictionary: Parsed YAML python object
    :param str yaml_file: Path to yaml file
    """

    if 'ref' in dictionary:
        validate_type(dictionary['ref'], 'ref', str, 'str', yaml_file)
        _validate_ref_type(dictionary, yaml_file)
        del dictionary['ref']


def _validate_optional_bool(dictionary: dict, value: str, yaml_file: str) -> None:
    """Check whether yaml file contains optional boolean

    :param dict dictionary: Parsed YAML python object
    :param str value: Name of entry to check
    :param str yaml_file: Path to yaml file
    """

    _validate_optional_value(dictionary, value, bool, 'bool', yaml_file)


def _validate_optional_string(dictionary: dict, value: str, yaml_file: str) -> None:
    """Check whether yaml file contains optional string

    :param dict dictionary: Parsed YAML python object
    :param str value: Name of entry to check
    :param str yaml_file: Path to yaml file
    """

    _validate_optional_value(dictionary, value, str, 'str', yaml_file)


def _validate_optional_value(dictionary: dict, value: str, classinstance: type, type_name: str, yaml_file: str) -> None:
    """Check whether yaml file contains optional value

    :param dict dictionary: Parsed YAML python object
    :param str value: Name of entry to check
    :param type classinstance: Type to check
    :param str type_name: Name of type to print if invalid
    :param str yaml_file: Path to yaml file
    """

    if value in dictionary:
        validate_type(dictionary[value], value, classinstance, type_name, yaml_file)
        del dictionary[value]


def _validate_protocol_type(dictionary: dict, yaml_file: str) -> None:
    """Check whether protocol type is valid

    :param dict dictionary: Parsed YAML python object
    :param str yaml_file: Path to yaml file
    :raise ClowderYAMLError:
    """

    if not _is_valid_protocol_type(dictionary['protocol']):
        raise ClowderYAMLError(fmt.invalid_protocol_error(dictionary['protocol'], yaml_file),
                               ClowderYAMLYErrorType.INVALID_PROTOCOL)


def _validate_required_protocol(dictionary: dict, yaml_file: str) -> None:
    """Check for required protocol value

    :param dict dictionary: Parsed YAML python object
    :param str yaml_file: Path to yaml file
    """

    _validate_dict_contains_value(dictionary, 'defaults', 'protocol', yaml_file)
    validate_type(dictionary['protocol'], 'protocol', str, 'str', yaml_file)
    _validate_protocol_type(dictionary, yaml_file)
    del dictionary['protocol']


def _validate_required_ref(dictionary: dict, yaml_file: str) -> None:
    """Check for required ref value

    :param dict dictionary: Parsed YAML python object
    :param str yaml_file: Path to yaml file
    """

    _validate_dict_contains_value(dictionary, 'defaults', 'ref', yaml_file)
    validate_type(dictionary['ref'], 'ref', str, 'str', yaml_file)
    _validate_ref_type(dictionary, yaml_file)
    del dictionary['ref']


def _validate_required_string(dictionary: dict, dict_name: str, value: str, yaml_file: str) -> None:
    """Check whether yaml file contains required value

    :param dict dictionary: Parsed YAML python object
    :param str dict_name: Name of dict to print if missing
    :param str value: Name of entry to check
    :param str yaml_file: Path to yaml file
    """

    _validate_dict_contains_value(dictionary, dict_name, value, yaml_file)
    validate_type(dictionary[value], value, str, 'str', yaml_file)
    del dictionary[value]


def _validate_ref_type(dictionary: dict, yaml_file: str) -> None:
    """Check whether ref type is valid

    :param dict dictionary: Parsed YAML python object
    :param str yaml_file: Path to yaml file
    :raise ClowderYAMLError:
    """

    if not _is_valid_ref_type(dictionary['ref']):
        raise ClowderYAMLError(fmt.invalid_ref_error(dictionary['ref'], yaml_file), ClowderYAMLYErrorType.INVALID_REF)


def _validate_type_depth(value: int, yaml_file: str) -> None:
    """Validate depth value

    :param int value: Integer depth value
    :param str yaml_file: Path to yaml file
    :raise ClowderYAMLError:
    """

    if not isinstance(value, int) or int(value) < 0:
        raise ClowderYAMLError(fmt.depth_error(value, yaml_file), ClowderYAMLYErrorType.DEPTH)
