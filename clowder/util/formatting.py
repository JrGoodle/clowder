"""String formatting utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import math
from pathlib import Path
from typing import List, Optional, Tuple, Union

from pygoodle.console import CONSOLE
from pygoodle.formatting import Format


# TODO: Update to return list of all duplicates found
def check_for_duplicates(list_of_elements: List[str]) -> Optional[str]:
    """Check if given list contains any duplicates

    :param List[str] list_of_elements: List of strings to check for duplicates
    :return: First duplicate encountered, or None if no duplicates found
    """

    set_of_elements = set()
    for elem in list_of_elements:
        if elem in set_of_elements:
            return elem
        else:
            set_of_elements.add(elem)
    return None


def clowder_command(cmd: str) -> str:
    """Return formatted clowder command name

    :param str cmd: Clowder command name
    :return: Formatted clowder command name
    """

    return Format.bold(cmd)


def clowder_name(name: str) -> str:
    """Return formatted clowder name

    :param str name: Clowder name
    :return: Formatted clowder name
    """

    return Format.bold(name)


def command(cmd: Union[str, List[str]]) -> str:
    """Return formatted command name

    :param Union[str, List[str]] cmd: Clowder command name
    :return: Formatted clowder command name
    """

    command_output = " ".join(cmd) if isinstance(cmd, list) else cmd
    return Format.bold(f"$ {command_output}")


def invalid_yaml(name: str) -> str:
    """Return error message for invalid yaml file

    :param str name: Invalid file's name
    :return: Formatted yaml error
    """

    return f"{path(Path(name))} appears to be invalid"


# def error_source_not_found(source: str, yml: Path, project: str, upstream_name: Optional[str] = None) -> str:
#     """Return formatted error string for project with unknown source specified
#
#     :param str source: Source name
#     :param Path yml: Path to yaml file
#     :param str project: Project name
#     :param Optional[str] upstream_name: Upstream name
#     :return: Formatted source not found error
#     """
#
#     upstream_output = ""
#     if upstream_name:
#         upstream_output = f" for upstream '{upstream_name}'"
#
#     messages = [invalid_yaml(yml.name),
#                 f"{yaml_path(yml)}",
#                 f"source '{source}'{upstream_output} specified in project '{project}' not found in 'sources'"]
#     return "\n".join(messages)


# FIXME: Only print project name using this where appropriate (now that project status and upstream_string
# are printed back to back)
def upstream(name: str) -> str:
    """Return formatted upstream name

    :param str name: Upstream name
    :return: Formatted upstream name
    """

    return Format.cyan(name)


def options_help_message(options: Tuple[str, ...], message: str) -> str:
    """Help message for groups option

    :param Tuple[str, ...] options: List of options
    :param str message: Help message
    :return: Formatted options help message
    """

    if options == [''] or options is None or options == [] or not all(isinstance(n, str) for n in options):
        return message

    help_message = '''
                   {0}:
                   {1}
                   '''

    return help_message.format(message, ', '.join(options))


def project_options_help_message(message: str) -> str:
    """Help message for projects/groups options

    :param str message: Help message
    :return: Formatted options help message
    """

    def column_entry(choices, length, line):
        if len(choices) > 0 and line < len(choices):
            return choices[line].ljust(length)
        return "".ljust(length)

    def three_column_width(choices, title, spacing=0):
        options = list(choices)
        options += title
        length = len(max(options, key=len))
        return length + spacing

    from clowder.clowder_controller import CLOWDER_CONTROLLER

    project_names = CLOWDER_CONTROLLER.project_names
    upstream_names = CLOWDER_CONTROLLER.upstream_names
    project_paths = CLOWDER_CONTROLLER.project_paths
    project_groups = CLOWDER_CONTROLLER.project_groups

    valid_project_names = _validate_help_options(project_names)
    valid_paths = _validate_help_options(project_paths)
    valid_groups = _validate_help_options(project_groups)
    if not valid_project_names or not valid_paths or not valid_groups:
        return message

    project_names_title = "Project Names"
    project_names_underline = "-------------"
    project_paths_title = "Project Paths"
    project_paths_underline = "-------------"
    project_groups_title = "Project Groups"
    project_groups_underline = "--------------"

    if not upstream_names:
        project_names_column_width = three_column_width(project_names, project_names_title, spacing=2)
        project_paths_column_width = three_column_width(project_paths, project_paths_title, spacing=2)
        project_groups_column_width = three_column_width(project_groups, project_groups_title)

        max_column_lines = max(len(project_names), len(project_paths), len(project_groups))

        message = f'{message}:\n\n'
        message += project_names_title.ljust(project_names_column_width)
        message += project_paths_title.ljust(project_paths_column_width)
        message += project_groups_title.ljust(project_groups_column_width)
        message += "\n"
        message += project_names_underline.ljust(project_names_column_width)
        message += project_paths_underline.ljust(project_paths_column_width)
        message += project_groups_underline.ljust(project_groups_column_width)
        message += "\n"

        column_line = 0
        while column_line < max_column_lines:
            message += column_entry(project_names, project_names_column_width, column_line)
            message += column_entry(project_paths, project_paths_column_width, column_line)
            message += column_entry(project_groups, project_groups_column_width, column_line)
            message += "\n"
            column_line += 1

        return message

    valid_upstream_names = _validate_help_options(upstream_names)
    if not valid_upstream_names:
        return message

    def two_column_width(choices_1, title_1, choices_2, title_2, spacing=0):
        options = list(choices_1)
        options += list(choices_2)
        options += title_1
        options += title_2
        length = len(max(options, key=len))
        return length + spacing

    upstream_names_title = "Upstream Names"
    upstream_names_underline = "--------------"
    names_column_width = two_column_width(project_names, project_names_title,
                                          upstream_names, upstream_names_title, spacing=2)
    paths_groups_width = two_column_width(project_paths, project_paths_title, project_groups, project_groups_title)

    message = f'{message}:\n\n'
    message += project_names_title.ljust(names_column_width)
    message += project_paths_title.ljust(paths_groups_width)
    message += "\n"
    message += project_names_underline.ljust(names_column_width)
    message += project_paths_underline.ljust(paths_groups_width)
    message += "\n"

    max_column_length = max(len(project_names), len(project_paths))
    column_line = 0
    while column_line < max_column_length:
        message += column_entry(project_names, names_column_width, column_line)
        message += column_entry(project_paths, paths_groups_width, column_line)
        message += "\n"
        column_line += 1

    message += "\n"
    message += upstream_names_title.ljust(names_column_width)
    message += project_groups_title.ljust(paths_groups_width)
    message += "\n"
    message += upstream_names_underline.ljust(names_column_width)
    message += project_groups_underline.ljust(paths_groups_width)
    message += "\n"

    max_column_length = max(len(upstream_names), len(project_groups))
    column_line = 0
    while column_line < max_column_length:
        message += column_entry(upstream_names, names_column_width, column_line)
        message += column_entry(project_groups, paths_groups_width, column_line)
        message += "\n"
        column_line += 1

    return message


def path(text: Path) -> str:
    """Return formatted path

    :param Path text: Path name
    :return: Formatted path name
    """

    return Format.cyan(text.resolve())


def ref(text: str) -> str:
    """Return formatted ref name

    :param str text: Git reference
    :return: Formatted ref name
    """

    return Format.magenta(text)


def remote(text: str) -> str:
    """Return formatted remote name

    :param str text: Remote name
    :return: Formmatted remote name
    """

    return Format.yellow(text)


def url_string(url: str) -> str:
    """Return formatted url

    :param str url: URL
    :return: Formatted URL
    """

    return Format.cyan(url)


def version_options_help_message(message: str, versions: Tuple[str, ...]) -> str:
    """Help message for projects/groups options

    :param str message: Help message
    :param Tuple[str, ...] versions: Version choices
    :return: Formatted options help message
    """

    if not _validate_help_options(versions):
        return message

    message = f"{message}:\n\n"
    if len(versions) < 10:
        for v in versions:
            message += f"{v}\n"
        return message

    terminal_width = CONSOLE.width

    def column_entry(choices, length, line):
        if len(choices) > 0 and line < len(choices):
            return choices[line].ljust(length)
        return "".ljust(length)

    def column_width(choices, spacing=0):
        length = len(max(choices, key=len))
        return length + spacing

    # Determine required widths for 3 column layout
    max_lines = math.ceil(len(versions) / 3)

    first_column_versions = versions[:max_lines]
    second_column_versions = versions[max_lines:2*max_lines]
    third_column_versions = versions[2*max_lines:]

    first_column_width = column_width(first_column_versions, spacing=2)
    second_column_width = column_width(second_column_versions, spacing=2)
    third_column_width = column_width(third_column_versions)

    total_width = first_column_width + second_column_width + third_column_width

    if total_width < terminal_width:
        column_line = 0
        while column_line < max_lines:
            message += column_entry(first_column_versions, first_column_width, column_line)
            message += column_entry(second_column_versions, second_column_width, column_line)
            message += column_entry(third_column_versions, third_column_width, column_line)
            message += "\n"
            column_line += 1
        return message

    # If doesn't fit, determine required widths for 2 column layout
    column_length = math.ceil(len(versions) / 2)

    first_column_versions = versions[:column_length]
    second_column_versions = versions[column_length:]

    first_column_width = column_width(first_column_versions, spacing=2)
    second_column_width = column_width(second_column_versions)

    total_width = first_column_width + second_column_width

    if total_width < terminal_width:
        column_line = 0
        while column_line < max_lines:
            message += column_entry(first_column_versions, first_column_width, column_line)
            message += column_entry(second_column_versions, second_column_width, column_line)
            message += "\n"
            column_line += 1
        return message

    for v in versions:
        message += f"{v}\n"
    return message


def version(version_name: str) -> str:
    """Return formatted string for clowder yaml version

    :param str version_name: Clowder version name
    :return: Formatted clowder version name
    """

    return Format.bold(version_name)


def project_name(name: str) -> str:
    """Return formatted string for project name

    :param str name: Project name
    :return: Formatted project name
    """

    return Format.green(name)


def _validate_help_options(options: Optional[Union[str, list, tuple]]) -> bool:
    """Validate help options is valid

    :param str options: Possible options
    :return: Whether options is valid
    """

    if options is None:
        return False
    if not options:
        return False
    if options == ['']:
        return False
    if not all(isinstance(n, str) for n in options):
        return False
    return True
