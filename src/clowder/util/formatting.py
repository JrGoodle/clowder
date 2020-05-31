# -*- coding: utf-8 -*-
"""String formatting utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from pathlib import Path
from typing import Optional, Tuple

from termcolor import colored
from typing import List, Union


ERROR = colored(' - Error:', 'red')
WARNING = colored(' - Warning:', 'yellow')


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

    return colored(cmd, attrs=['bold'])


def clowder_name(name: str) -> str:
    """Return formatted clowder name

    :param str name: Clowder name
    :return: Formatted clowder name
    :rtype: str
    """

    return colored(name, attrs=['bold'])


def command(cmd: Union[str, List[str]]) -> str:
    """Return formatted command name

    :param Union[str, List[str]] cmd: Clowder command name
    :return: Formatted clowder command name
    :rtype: str
    """

    command_output = " ".join(cmd) if isinstance(cmd, list) else cmd
    return colored(f"$ {command_output}", attrs=['bold'])


def error(err: Exception) -> str:
    """Return error message for generic error

    :param Exception err: Generic error
    :return: Formatted generic error
    :rtype: str
    """

    return f"{ERROR} {str(err)}"


def error_ambiguous_clowder_yaml() -> str:
    """Return formatted error string for ambiguous clowder yaml file

    :return: Formatted ambigious clowder yaml error
    :rtype: str
    """

    yml_file = _yaml_file(Path('clowder.yml'))
    yaml_file = _yaml_file(Path('clowder.yaml'))
    return f"{ERROR} Found {yml_file} and {yaml_file} files in same directory"


def error_clone_missing_projects() -> str:
    """Format error message for clone missing projects

    :return: Formatted error message for clone missing projects
    :rtype: str
    """

    return f"{ERROR} First run {clowder_command('clowder herd')} to clone missing projects"


def error_clowder_already_initialized() -> str:
    """Format error message for clowder already initialized

    :return: Formatted message for clowder already initialized error
    :rtype: str
    """

    return f"{ERROR} Clowder already initialized in this directory"


def error_clowder_symlink_source_missing(symlink_path: Path, clowder_dir: Path) -> str:
    """Return formatted error string for clowder symlink source not found

    :param Path symlink_path: Clowder yaml symlink path
    :param Path clowder_dir: Clowder directory
    :return: Formatted clowder symlink source not found warning
    :rtype: str
    """

    target = _yaml_file(symlink_path.relative_to(clowder_dir))
    source = _yaml_file(symlink_path.resolve().relative_to(clowder_dir))
    return f"{ERROR} Found symink {target} -> {source} but source appears to be missing"


def error_command_failed(cmd: Union[str, List[str]]) -> str:
    """Format error message for failed command

    :param Union[str, List[str]] cmd: Clowder command name
    :return: Formatted clowder command name
    :rtype: str
    """

    return f"{ERROR} Failed to run command {command(cmd)}"


def error_directory_exists(dir_path: Path) -> str:
    """Format error message for already existing directory

    :param Path dir_path: Directory path
    :return: Formatted directory exists error
    :rtype: str
    """

    dir_path = path_string(dir_path)
    return f"{ERROR} Directory already exists at {dir_path}"


def error_duplicate_version(version: str) -> str:
    """Format error message for duplicate clowder version

    :param str version: Clowder version name
    :return: Formatted duplicate clowder version error
    :rtype: str
    """

    return f"{ERROR} Duplicate version found: {_yaml_file(Path(version))}"


def error_duplicate_project_path(path: Path, yml: Path) -> str:
    """Return formatted error string for duplicate project path

    :param Path path: Duplicate project path
    :param Path yml: Path to yaml file
    :return: Formatted duplicate remote fork name error
    :rtype: str
    """

    messages = [error_invalid_yaml_file(yml.name),
                f"{ERROR} {_yaml_path(yml)}",
                f"{ERROR} Multiple projects with path '{path}'"]
    return "\n".join(messages)


def error_empty_yaml(yml: Path, name: Path) -> str:
    """Return formatted error string for empty clowder yaml file

    :param Path yml: Path to yaml file
    :param Path name: Path to use in error message
    :return: Formatted empty yaml error
    :rtype: str
    """

    path = _yaml_path(yml)
    file = _yaml_file(str(name))
    return f"{path}\n{ERROR} No entries in {file}"


def error_existing_file_at_clowder_repo_path(file_path: Path) -> str:
    """Format error message for existing file at .clowder path

    :param Path file_path: Path to existing .clowder file
    :return: Formatted existing file at .clowder path error
    :rtype: str
    """

    return f"{ERROR} Found non-directory file {path_string(file_path)} where clowder repo directory should be"


def error_existing_file_at_symlink_target_path(name: Path) -> str:
    """Format error message for existing non-symlink file at symlink target path

    :param Path name: Path to use in error message
    :return: Formatted existing non-symlink file at symlink target path error
    :rtype: str
    """

    return f"{ERROR} Found non-symlink file {path_string(name)} at target path"


def error_failed_clowder_init() -> str:
    """Format error message for failed clowder init

    :return: Formatted failed clowder init error
    :rtype: str
    """

    return f"{ERROR} Failed to initialize clowder repo"


def error_failed_create_directory(dir_path: Path) -> str:
    """Format error message for failing to create directory

    :param Path dir_path: Directory path to create
    :return: Formatted create directory error
    :rtype: str
    """

    dir_path = path_string(dir_path)
    return f"{ERROR} Failed to create directory {dir_path}"


def error_failed_remove_directory(dir_path: Path) -> str:
    """Format error message for failing to remove directory

    :param Path dir_path: Directory path to remove
    :return: Formatted remove directory error
    :rtype: str
    """

    dir_path = path_string(dir_path)
    return f"{ERROR} Failed to remove directory {dir_path}"


def error_failed_remove_file(file_path: Path) -> str:
    """Format error message for failing to remove file

    :param Path file_path: File path
    :return: Formatted remove file error
    :rtype: str
    """

    file_path = path_string(file_path)
    return f"{ERROR} Failed to remove file {file_path}"


def error_failed_symlink_file(target: Path, source: Path) -> str:
    """Format error message for failing to symlink file

    :param Path target: Target file path
    :param Path source: Source file path
    :return: Formatted remove file error
    :rtype: str
    """

    target_path = path_string(target)
    source_path = path_string(source)
    return f"{ERROR} Failed to symlink file {target_path} -> {source_path}"


def error_file_exists(file_path: Path) -> str:
    """Format error message for already existing file

    :param Path file_path: File path name
    :return: Formatted file exists error
    :rtype: str
    """

    file_path = path_string(file_path)
    return f"{ERROR} File already exists {file_path}"


def error_groups_contains_all(yml: Path) -> str:
    """Return formatted error string for invalid 'all' entry in groups list

    :param Path yml: Path to yaml file
    :return: Formatted error for groups containing all
    :rtype: str
    """

    path = _yaml_path(yml)
    return f"{path}\n{ERROR} 'groups' cannot contain 'all'"


def error_invalid_config_file(file_path: Path) -> str:
    """Return error message for invalid config file

    :param Path file_path: Invalid config file path
    :return: Formatted invalid config file error
    :rtype: str
    """

    file = _yaml_file(str(file_path))
    return f"{ERROR} {file}\n{ERROR} Clowder config file appears to be invalid"


def error_invalid_git_config_value(key: str, value: str) -> str:
    """Format error message for invalid git config value

    :param str key: Key for value with invalid git type
    :param str value: Value with invalid git type
    :return: Formatted error message for invalid git config value
    :rtype: str
    """

    return f"{ERROR} Invalid git config value - {key}: {value}"


def error_invalid_project_state() -> str:
    """Format error message for invalid project state

    :return: Formatted error message for invalid project state
    :rtype: str
    """

    return f"{ERROR} Invalid project state"


def error_invalid_ref(ref: str, yml: Path) -> str:
    """Return formatted error string for incorrect ref

    :param str ref: Git reference
    :param Path yml: Path to yaml file
    :return: Formatted invalid ref error
    :rtype: str
    """

    path = _yaml_path(yml)
    return f"{ERROR} {path}\n{ERROR} 'ref' value '{ref}' is not formatted correctly"


def error_invalid_yaml_file(name: str) -> str:
    """Return error message for invalid yaml file

    :param str name: Invalid file's name
    :return: Formatted yaml error
    :rtype: str
    """

    file = _yaml_file(Path(name))
    return f"{ERROR} {file} appears to be invalid"


def error_missing_clowder_repo() -> str:
    """Format error message for missing clowder repo

    :return: Formatted missing clowder repo error
    :rtype: str
    """

    return f"{ERROR} No {path_string(Path('.clowder'))} directory found"


def error_missing_clowder_git_repo() -> str:
    """Format error message for missing clowder git repo

    :return: Formatted missing clowder git repo error
    :rtype: str
    """

    return f"{ERROR} No {path_string(Path('.clowder'))} git repository found"


def error_missing_clowder_yaml() -> str:
    """Format error message for missing clowder yaml file

    :return: Formatted missing YAML error
    :rtype: str
    """

    clowder_file = Path('clowder.yml')
    return error_missing_file(clowder_file)


def error_missing_file(yaml_file: Path) -> str:
    """Format error message for missing linked clowder yaml file

    :param Path yaml_file: Path to missing yaml file
    :return: Formatted missing YAML error
    :rtype: str
    """

    file = _yaml_file(str(yaml_file))
    return f"{ERROR} {file} appears to be missing"


def error_no_clowder_found(dir_path: Path) -> str:
    """Format error message for no clowder found

    :param Path dir_path: Missing clowder directory path
    :return: Formatted no clowder found error
    :rtype: str
    """

    dir_path = path_string(dir_path)
    return f"{ERROR} No clowder found at {dir_path}"


def error_offline() -> str:
    """Return error message for no internet connection

    :return: Offline error message
    :rtype: str
    """

    return f"{ERROR} No available internet connection"


def error_open_file(path: Path) -> str:
    """Format error message for failing to open file

    :param Path path: File path
    :return: Formatted file error
    :rtype: str
    """

    path = path_string(path)
    return f"{ERROR} Failed to open file '{path}'"


def error_parallel_command_failed() -> str:
    """Return formatted error string for parallel command failed

    :return: Formatted parallel command failed error
    :rtype: str
    """

    return f"{ERROR} Parallel command failed"


def error_parallel_commands_unavailable() -> str:
    """Return formatted error string for parallel command unavailable

    :return: Formatted parallel command unavailable error
    :rtype: str
    """

    return f'{ERROR} Parallel commands are only available on posix operating systems'


def error_parallel_exception(file_path: Path, *args) -> str:
    """Return formatted error string for parallel error

    :param Path file_path: Clowder file path
    :param args: Method arguments
    :return: Formatted parallel exception error
    :rtype: str
    """

    file_path = path_string(file_path)
    return f"{ERROR} {file_path}\n{ERROR} {''.join(args)}"


def error_remote_already_exists(remote_name: str, remote_url: str, actual_url: str) -> str:
    """Format error message when remote already exists with different url

    :param str remote_name: Remote name
    :param str remote_url: Remote URL
    :param str actual_url: Actual URL
    :return: Formatted remote exists error
    :rtype: str
    """

    remote = remote_string(remote_name)
    return f"{ERROR} Remote {remote} already exists with a different url\n" \
           f"{url_string(actual_url)} should be {url_string(remote_url)}"


def error_remote_dup(fork: str, project: str, remote: str, yml: Path) -> str:
    """Return formatted error string for fork with same remote as project

    :param str fork: Fork name
    :param str project: Project name
    :param str remote: Remote name
    :param Path yml: Path to yaml file
    :return: Formatted duplicate remote fork name error
    :rtype: str
    """

    messages = [error_invalid_yaml_file(yml.name),
                f"{ERROR} {_yaml_path(yml)}",
                f"{ERROR} fork '{fork}' and project '{project}' have same remote name '{remote}'"]
    return "\n".join(messages)


def error_save_default(name: str) -> str:
    """Format error message for trying to save disallowed version

    :param str name: Version name
    :return: Formatted default version error
    :rtype: str
    """

    return f"{ERROR} Version name '{name}' is not allowed"


def error_save_file(file_path: Path) -> str:
    """Format error message for failing to save file

    :param Path file_path: File path
    :return: Formatted save failure error
    :rtype: str
    """

    file_path = path_string(file_path)
    return f"{ERROR} Failed to save file {file_path}"


def error_save_version_exists(version_name: str, yml: Path) -> str:
    """Format error message previous existing saved version

    :param str version_name: Version name
    :param Path yml: Path to yaml file
    :return: Formatted version exists error
    :rtype: str
    """

    file = _yaml_file(str(yml))
    version = version_string(version_name)
    return f"{ERROR} {file}\n{ERROR} Version '{version}' already exists"


def error_source_default_not_found(source: str, yml: Path) -> str:
    """Return formatted error string for unknown default source specified

    :param str source: Source name
    :param Path yml: Path to yaml file
    :return: Formatted source not found error
    :rtype: str
    """

    error_invalid_yaml_file(yml.name)
    messages = [error_invalid_yaml_file(yml.name),
                f"{ERROR} {_yaml_path(yml)}",
                f"{ERROR} source '{source}' not found in 'defaults'"]
    return "\n".join(messages)


def error_source_not_found(source: str, yml: Path, project: str, fork: Optional[str] = None) -> str:
    """Return formatted error string for project with unknown source specified

    :param str source: Source name
    :param Path yml: Path to yaml file
    :param str project: Project name
    :param Optional[str] fork: Fork name
    :return: Formatted source not found error
    :rtype: str
    """

    fork_output = ""
    if fork:
        fork_output = f" for fork '{fork}'"

    messages = [error_invalid_yaml_file(yml.name),
                f"{ERROR} {_yaml_path(yml)}",
                f"{ERROR} source '{source}'{fork_output} specified in project '{project}' not found in 'sources'"]
    return "\n".join(messages)


def error_symlink_source_missing(source: Path) -> str:
    """Return formatted error string for symlink source not found

    :param Path source: Symlink source path
    :return: Formatted clowder symlink source not found warning
    :rtype: str
    """

    source = _yaml_file(str(source))
    return f"{ERROR} Symlink source {source} appears to be missing"


def error_timestamp_not_found() -> str:
    """Return timestamp not found error message

    :return: Formatted timestamp not found error message
    :rtype: str
    """
    return f"{ERROR} Failed to find timestamp\n"


def error_unknown_config_type() -> str:
    """Format error message for unknown config type

    :return: Formatted error message for unknown config type
    :rtype: str
    """

    return f"{ERROR} Unknown config type"


def error_unknown_project(name: str) -> str:
    """Return formatted unknown project name error

    :param str name: Project name
    :return: Formatted unknown project name error
    :rtype: str
    """

    return f"{ERROR} Unknown project {_project_name(name)}"


def error_user_interrupt() -> str:
    """Format error message for user interrupt

    :return: Formatted user interrupt
    :rtype: str
    """

    return f"{ERROR} User interruption"


def fork_string(name: str) -> str:
    """Return formatted fork name

    :param str name: Fork name
    :return: Formatted fork name
    :rtype: str
    """

    return colored(name, 'cyan')


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


def path_string(path: Path) -> str:
    """Return formatted path

    :param Path path: Path name
    :return: Formatted path name
    :rtype: str
    """

    return colored(str(path), 'cyan')


def ref_string(ref: str) -> str:
    """Return formatted ref name

    :param str ref: Git reference
    :return: Formatted ref name
    :rtype: str
    """

    return colored(f"[{ref}]", 'magenta')


def remote_string(remote: str) -> str:
    """Return formatted remote name

    :param str remote: Remote name
    :return: Formmatted remote name
    :rtype: str
    """

    return colored(remote, 'yellow')


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


def save_version_message(version: str, yml: Path) -> str:
    """Format message for saving version

    :param str version: Clowder version name
    :param Path yml: Path to yaml file
    :return: Formatted version name
    :rtype: str
    """

    version = version_string(version)
    path = path_string(yml)
    return f" - Save version '{version}'\n{path}"


def url_string(url: str) -> str:
    """Return formatted url

    :param str url: URL
    :return: Formatted URL
    :rtype: str
    """

    return colored(url, 'cyan')


def version_string(version_name: str) -> str:
    """Return formatted string for clowder yaml version

    :param str version_name: Clowder version name
    :return: Formatted clowder version name
    :rtype: str
    """

    return colored(version_name, attrs=['bold'])


def warning_clowder_repo_missing_git_dir() -> str:
    """Return formatted warning string for existing .clowder directory that isn't a git repository

    :return: Formatted warning string for existing .clowder directory that isn't a git repository
    :rtype: str
    """

    return f"{WARNING} Found {path_string(Path('.clowder'))} directory that is not a git repository"


def warning_clowder_yaml_not_symlink_with_clowder_repo(name: str) -> str:
    """Return formatted warning string for non-symlink clowder yaml file with an existing clowder repo

    :param str name: Clowder yaml file name
    :return: Formatted warning string for non-symlink clowder yaml file with an existing clowder repo
    :rtype: str
    """

    return f"{WARNING} Found a {_yaml_file(name)} file but it is not a symlink " \
           f"to a file stored in the existing {path_string(Path('.clowder'))} repo"


def warning_invalid_config_file(file_path: Path) -> str:
    """Return warning message for invalid config file

    :param Path file_path: Invalid config file path
    :return: Formatted invalid config file warning
    :rtype: str
    """

    file = _yaml_file(str(file_path))
    return f"{WARNING} Clowder config file at {file} appears to be invalid"


def _project_name(name: str) -> str:
    """Return formatted string for project name

    :param str name: Project name
    :return: Formatted project name
    :rtype: str
    """

    return colored(name, 'green')


def _yaml_path(yml: Path) -> str:
    """Returns formatted yaml path

    :param Path yml: Path to yaml file
    :return: Formatted YAML path
    :rtype: str
    """

    return path_string(yml.resolve())


def _yaml_file(yml: str) -> str:
    """Return formatted string for clowder yaml file

    :param str yml: Path to yaml file
    :return: Formatted YAML string
    :rtype: str
    """

    return colored(yml, 'cyan')
