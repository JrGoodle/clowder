"""String formatting utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import math
import os
from pathlib import Path
from typing import List, Optional, Tuple, Union

from clowder.logging import LOG


Output = Union[str, Path]


def bold(output: Output) -> str:
    return f'[bold]{output}[/bold]'


def cyan(output: Output) -> str:
    return f'[cyan]{output}[/cyan]'


def green(output: Output) -> str:
    return f'[green]{output}[/green]'


def red(output: Output) -> str:
    return f'[red]{output}[/red]'


def magenta(output: Output) -> str:
    return f'[magenta]{output}[/magenta]'


def yellow(output: Output) -> str:
    return f'[yellow]{output}[/yellow]'


def escape(output: Output) -> str:
    import rich.markup as markup
    return f'[yellow]{markup.escape(output)}[/yellow]'


# TODO: Update to return list of all duplicates found
def check_for_duplicates(list_of_elements: List[str]) -> Optional[str]:
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


def clowder_command(cmd: str) -> str:
    """Return formatted clowder command name

    :param str cmd: Clowder command name
    :return: Formatted clowder command name
    :rtype: str
    """

    return bold(cmd)


def clowder_name(name: str) -> str:
    """Return formatted clowder name

    :param str name: Clowder name
    :return: Formatted clowder name
    :rtype: str
    """

    return bold(name)


def command(cmd: Union[str, List[str]]) -> str:
    """Return formatted command name

    :param Union[str, List[str]] cmd: Clowder command name
    :return: Formatted clowder command name
    :rtype: str
    """

    command_output = " ".join(cmd) if isinstance(cmd, list) else cmd
    return bold(f"$ {command_output}")


def error(err: Exception) -> str:
    """Return error message for generic error

    :param Exception err: Generic error
    :return: Formatted generic error
    :rtype: str
    """

    return f"{err}"


def error_clone_missing_projects() -> str:
    """Format error message for clone missing projects

    :return: Formatted error message for clone missing projects
    :rtype: str
    """

    return f"First run {clowder_command('clowder herd')} to clone missing projects"


def error_clowder_already_initialized() -> str:
    """Format error message for clowder already initialized

    :return: Formatted message for clowder already initialized error
    :rtype: str
    """

    return f"Clowder already initialized in this directory"


def error_clowder_symlink_source_missing(symlink_path: Path) -> str:
    """Return formatted error string for clowder symlink source not found

    :param Path symlink_path: Clowder yaml symlink path
    :return: Formatted clowder symlink source not found warning
    :rtype: str
    """

    target = yaml_file(str(symlink_path))
    source = yaml_file(str(symlink_path.resolve()))
    return f"Found symlink {target} but source {source} appears to be missing"


def error_command_failed(cmd: Union[str, List[str]]) -> str:
    """Format error message for failed command

    :param Union[str, List[str]] cmd: Clowder command name
    :return: Formatted clowder command name
    :rtype: str
    """

    return f"Failed to run command {command(cmd)}"


def error_directory_exists(dir_path: str) -> str:
    """Format error message for already existing directory

    :param Path dir_path: Directory path
    :return: Formatted directory exists error
    :rtype: str
    """

    return f"Directory already exists at {path(dir_path)}"


def error_duplicate_version(v: str) -> str:
    """Format error message for duplicate clowder version

    :param str v: Clowder version name
    :return: Formatted duplicate clowder version error
    :rtype: str
    """

    return f"Duplicate version found: {yaml_file(Path(v))}"


def error_duplicate_project_path(project_path: str, yml: Path) -> str:
    """Return formatted error string for duplicate project path

    :param str project_path: Duplicate project path
    :param Path yml: Path to yaml file
    :return: Formatted duplicate remote upstream name error
    :rtype: str
    """

    messages = [error_invalid_yaml_file(yml.name),
                f"{yaml_path(yml)}",
                f"Multiple projects with path '{project_path}'"]
    return "\n".join(messages)


def error_empty_yaml(yml: Path, name: Path) -> str:
    """Return formatted error string for empty clowder yaml file

    :param Path yml: Path to yaml file
    :param Path name: Path to use in error message
    :return: Formatted empty yaml error
    :rtype: str
    """

    output = yaml_path(yml)
    file = yaml_file(str(name))
    return f"{output}\nNo entries in {file}"


def error_existing_file_at_clowder_repo_path(file_path: str) -> str:
    """Format error message for existing file at .clowder path

    :param str file_path: Path to existing .clowder file
    :return: Formatted existing file at .clowder path error
    :rtype: str
    """

    return f"Found non-directory file {path(file_path)} where clowder repo directory should be"


def error_existing_file_at_symlink_target_path(name: str) -> str:
    """Format error message for existing non-symlink file at symlink target path

    :param str name: Path to use in error message
    :return: Formatted existing non-symlink file at symlink target path error
    :rtype: str
    """

    return f"Found non-symlink file {path(name)} at target path"


def error_failed_clowder_init() -> str:
    """Format error message for failed clowder init

    :return: Formatted failed clowder init error
    :rtype: str
    """

    return f"Failed to initialize clowder repo"


def error_failed_create_directory(dir_path: str) -> str:
    """Format error message for failing to create directory

    :param str dir_path: Directory path to create
    :return: Formatted create directory error
    :rtype: str
    """

    return f"Failed to create directory {path(dir_path)}"


def error_failed_remove_directory(dir_path: str) -> str:
    """Format error message for failing to remove directory

    :param str dir_path: Directory path to remove
    :return: Formatted remove directory error
    :rtype: str
    """

    return f"Failed to remove directory {path(dir_path)}"


def error_failed_remove_file(file_path: str) -> str:
    """Format error message for failing to remove file

    :param str file_path: File path
    :return: Formatted remove file error
    :rtype: str
    """

    return f"Failed to remove file {path(file_path)}"


def error_failed_symlink_file(target: str, source: str) -> str:
    """Format error message for failing to symlink file

    :param str target: Target file path
    :param str source: Source file path
    :return: Formatted remove file error
    :rtype: str
    """

    return f"Failed to symlink file {path(target)} -> {path(source)}"


def error_file_exists(file_path: str) -> str:
    """Format error message for already existing file

    :param str file_path: File path name
    :return: Formatted file exists error
    :rtype: str
    """

    return f"File already exists {path(file_path)}"


def error_groups_contains_all(yml: Path) -> str:
    """Return formatted error string for invalid 'all' entry in groups list

    :param Path yml: Path to yaml file
    :return: Formatted error for groups containing all
    :rtype: str
    """

    return f"{yaml_path(yml)}\n'groups' cannot contain 'all'"


def error_invalid_config_file(file_path: str) -> str:
    """Return error message for invalid config file

    :param str file_path: Invalid config file path
    :return: Formatted invalid config file error
    :rtype: str
    """

    return f"{yaml_file(file_path)}\nClowder config file appears to be invalid"


def error_failed_create_parser() -> str:
    """Format error message for failing to create cli parsers

    :return: Formatted failed to create parsers error
    :rtype: str
    """

    return f"Failed to create command line parsers"


def error_invalid_git_config_value(key: str, value: str) -> str:
    """Format error message for invalid git config value

    :param str key: Key for value with invalid git type
    :param str value: Value with invalid git type
    :return: Formatted error message for invalid git config value
    :rtype: str
    """

    return f"Invalid git config value - {key}: {value}"


def error_invalid_project_state() -> str:
    """Format error message for invalid project state

    :return: Formatted error message for invalid project state
    :rtype: str
    """

    return f"Invalid project state"


def error_invalid_ref(git_ref: str, yml: Path) -> str:
    """Return formatted error string for incorrect ref

    :param str git_ref: Git reference
    :param Path yml: Path to yaml file
    :return: Formatted invalid ref error
    :rtype: str
    """

    output = yaml_path(yml)
    return f"{output}\n'ref' value '{git_ref}' is not formatted correctly"


def error_invalid_yaml_file(name: str) -> str:
    """Return error message for invalid yaml file

    :param str name: Invalid file's name
    :return: Formatted yaml error
    :rtype: str
    """

    file = yaml_file(Path(name))
    return f"{file} appears to be invalid"


def error_missing_clowder_repo() -> str:
    """Format error message for missing clowder repo

    :return: Formatted missing clowder repo error
    :rtype: str
    """

    return f"No {path(Path('.clowder'))} directory found"


def error_missing_clowder_git_repo() -> str:
    """Format error message for missing clowder git repo

    :return: Formatted missing clowder git repo error
    :rtype: str
    """

    return f"No {path(Path('.clowder'))} git repository found"


def error_missing_clowder_yaml() -> str:
    """Format error message for missing clowder yaml file

    :return: Formatted missing YAML error
    :rtype: str
    """

    clowder_file = Path('clowder.yml')
    return error_missing_file(clowder_file)


def error_missing_file(file: str) -> str:
    """Format error message for missing linked clowder yaml file

    :param str file: Path to missing yaml file
    :return: Formatted missing YAML error
    :rtype: str
    """

    file = yaml_file(file)
    return f"{file} appears to be missing"


def error_remote_already_exists(remote_name: str, remote_url: str, actual_url: str) -> str:
    """Format error message when remote already exists with different url

    :param str remote_name: Remote name
    :param str remote_url: Remote URL
    :param str actual_url: Actual URL
    :return: Formatted remote exists error
    :rtype: str
    """

    output = remote(remote_name)
    return f"Remote {output} already exists with a different url\n" \
           f"{url_string(actual_url)} should be {url_string(remote_url)}"


def error_remote_dup(upstream: str, project: str, remote_name: str, yml: Path) -> str:
    """Return formatted error string for upstream with same remote as project

    :param str upstream: Upstream name
    :param str project: Project name
    :param str remote_name: Remote name
    :param Path yml: Path to yaml file
    :return: Formatted duplicate remote upstream name error
    :rtype: str
    """

    messages = [error_invalid_yaml_file(yml.name),
                f"{yaml_path(yml)}",
                f"upstream '{upstream}' and project '{project}' have same remote name '{remote_name}'"]
    return "\n".join(messages)


def error_save_version_exists(version_name: str, yml: Path) -> str:
    """Format error message previous existing saved version

    :param str version_name: Version name
    :param Path yml: Path to yaml file
    :return: Formatted version exists error
    :rtype: str
    """

    return f"{yaml_file(str(yml))}\nVersion '{version(version_name)}' already exists"


def error_source_default_not_found(source: str, yml: Path) -> str:
    """Return formatted error string for unknown default source specified

    :param str source: Source name
    :param Path yml: Path to yaml file
    :return: Formatted source not found error
    :rtype: str
    """

    error_invalid_yaml_file(yml.name)
    messages = [error_invalid_yaml_file(yml.name),
                f"{yaml_path(yml)}",
                f"source '{source}' not found in 'defaults'"]
    return "\n".join(messages)


def error_wrong_source_type() -> str:
    """Format error message for wrong source type

    :return: Formatted error message for wrong source type
    :rtype: str
    """

    return f"Wrong source type"


def error_wrong_submodules_type() -> str:
    return f"Wrong group type"


def error_wrong_group_type() -> str:
    return f"Wrong group type"


def error_sources_already_validated() -> str:
    return f"Sources have already been validated"


def error_source_not_validated() -> str:
    return f"Sources have not been validated"


def error_wrong_upstream_type() -> str:
    """Format error message for wrong upstream type

    :return: Formatted error message for wrong upstream type
    :rtype: str
    """

    return f"Wrong upstream type"


def error_source_not_defined(name: Optional[str] = None) -> str:
    if name is not None:
        return f"Source {name} not defined"
    return f"Source not defined"


def error_source_not_found(source: str, yml: Path, project: str, upstream: Optional[str] = None) -> str:
    """Return formatted error string for project with unknown source specified

    :param str source: Source name
    :param Path yml: Path to yaml file
    :param str project: Project name
    :param Optional[str] upstream: Upstream name
    :return: Formatted source not found error
    :rtype: str
    """

    upstream_output = ""
    if upstream:
        upstream_output = f" for upstream '{upstream}'"

    messages = [error_invalid_yaml_file(yml.name),
                f"{yaml_path(yml)}",
                f"source '{source}'{upstream_output} specified in project '{project}' not found in 'sources'"]
    return "\n".join(messages)


def error_unknown_config_type() -> str:
    """Format error message for unknown config type

    :return: Formatted error message for unknown config type
    :rtype: str
    """

    return f"Unknown config type"


def error_unknown_error() -> str:
    """Format error message for unknown error

    :return: Formatted unknown error message
    :rtype: str
    """

    return f"Unknown error occurred"


# FIXME: Only print project name using this where appropriate (now that project status and upstream_string
# are printed back to back)
def upstream_string(name: str) -> str:
    """Return formatted upstream name

    :param str name: Upstream name
    :return: Formatted upstream name
    :rtype: str
    """

    return cyan(name)


def options_help_message(options: Tuple[str, ...], message: str) -> str:
    """Help message for groups option

    :param Tuple[str, ...] options: List of options
    :param str message: Help message
    :return: Formatted options help message
    :rtype: str
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
    :rtype: str
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


def path(text: str) -> str:
    """Return formatted path

    :param Path text: Path name
    :return: Formatted path name
    :rtype: str
    """

    return cyan(text)


def ref(text: str) -> str:
    """Return formatted ref name

    :param str text: Git reference
    :return: Formatted ref name
    :rtype: str
    """

    return magenta(f"[{text}]")


def remote(text: str) -> str:
    """Return formatted remote name

    :param str text: Remote name
    :return: Formmatted remote name
    :rtype: str
    """

    return yellow(text)


def remove_prefix(text: str, prefix: str) -> str:
    """Remove prefix from string

    :param str text: Text to remove prefix from
    :param str prefix: Prefix to remoe
    :return: Text with prefix removed if present
    :rtype: str
    """

    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def url_string(url: str) -> str:
    """Return formatted url

    :param str url: URL
    :return: Formatted URL
    :rtype: str
    """

    return cyan(url)


def version_options_help_message(message: str, versions: Tuple[str, ...]) -> str:
    """Help message for projects/groups options

    :param str message: Help message
    :param Tuple[str, ...] versions: Version choices
    :return: Formatted options help message
    :rtype: str
    """

    if not _validate_help_options(versions):
        return message

    message = f"{message}:\n\n"
    if len(versions) < 10:
        for v in versions:
            message += f"{v}\n"
        return message

    try:
        size = os.get_terminal_size()
        terminal_width = size.columns
    except OSError as err:
        LOG.debug('Failed to get terminal size', err)
        terminal_width = 80

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
    :rtype: str
    """

    return bold(version_name)


def warning_invalid_config_file(file_path: str) -> str:
    """Return warning message for invalid config file

    :param Path file_path: Invalid config file path
    :return: Formatted invalid config file warning
    :rtype: str
    """

    return f"Clowder config file at {yaml_file(file_path)} appears to be invalid"


def project_name(name: str) -> str:
    """Return formatted string for project name

    :param str name: Project name
    :return: Formatted project name
    :rtype: str
    """

    return green(name)


def _validate_help_options(options: Optional[Union[str, list, tuple]]) -> bool:
    """Validate help options is valid

    :param str options: Possible options
    :return: Whether options is valid
    :rtype: bool
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


def yaml_path(yml: Path) -> str:
    """Returns formatted yaml path

    :param Path yml: Path to yaml file
    :return: Formatted YAML path
    :rtype: str
    """

    return path(str(yml.resolve()))


def yaml_file(yml: str) -> str:
    """Return formatted string for clowder yaml file

    :param str yml: Path to yaml file
    :return: Formatted YAML string
    :rtype: str
    """

    return cyan(yml)
