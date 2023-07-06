"""File system utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

# import errno
import fnmatch
import os
import re
import shutil
from pathlib import Path
from typing import List

import pygoodle.command as cmd


def list_subdirectories(path: Path, recursive: bool = False) -> List[Path]:
    if recursive:
        return [Path(info[0]) for info in os.walk(path)]
    else:
        paths = [Path(str(p)) for p in os.scandir(path)]
        return [f for f in paths if f.is_dir()]


def find_files_with_extension(directory: Path, extension: str) -> List[Path]:
    all_files = []
    for root, _, files in os.walk(directory):
        matching_files = [Path(root, f) for f in files if f.lower().endswith(f'.{extension.lower()}')]
        all_files += matching_files
    return all_files


def find_files(directory: Path, name: str) -> List[Path]:
    all_files = []
    for root, dirs, files in os.walk(directory):
        matching_files = [Path(root, f) for f in files if f.lower() == name.lower()]
        matching_dirs = [Path(root, d) for d in dirs if d.lower() == name.lower()]
        all_files += (matching_files + matching_dirs)
    return all_files


def find_files_containing_match(directory: Path, match: str) -> List[Path]:
    all_files = []
    for root, dirs, files in os.walk(directory):
        matching_files = [Path(root, f) for f in files if match.lower() in f.lower()]
        matching_dirs = [Path(root, d) for d in dirs if match.lower() in d.lower()]
        all_files += (matching_files + matching_dirs)
    return all_files


def find_rars(directory: Path, match_all: bool = False) -> List[Path]:
    all_rar_files = []
    for root, dirs, files in os.walk(directory):
        rar_files = [Path(root, f) for f in files if f.endswith('.rar')]
        if match_all:
            all_rar_files += rar_files
            continue
        tmp_files = []
        for file in rar_files:
            if file.name[:-4] in dirs:
                continue
            tmp_files.append(file)
            r = re.compile(r"^.+[.]part[0-9][0-9][0-9]?[.]rar$")
            if all(r.match(f.name) for f in rar_files):
                break
        all_rar_files += tmp_files
    return all_rar_files


def make_dir(dir_path: Path, exist_ok: bool = False) -> Path:
    os.makedirs(dir_path, exist_ok=exist_ok)
    return dir_path


def move(input_path: Path, output_path: Path) -> None:
    shutil.move(str(input_path), str(output_path))


def remove_dir(dir_path: Path, ignore_errors: bool = False) -> None:
    shutil.rmtree(str(dir_path), ignore_errors=ignore_errors)


def remove_file(file: Path) -> None:
    os.remove(str(file))


def remove(path: Path) -> None:
    if path.is_symlink():
        path.unlink()
    elif path.is_dir():
        remove_dir(path)
    elif path.is_file():
        remove_file(path)


def is_relative_to(path: Path, prefix: Path) -> bool:
    return str(path).startswith(str(prefix))


def replace_path_prefix(path: Path, old_prefix: Path, new_prefix: Path):
    # assert path.is_absolute()
    # assert path.is_relative_to(old_prefix)
    relative_path = path.relative_to(old_prefix)
    return new_prefix / relative_path


def listdir(directory: Path) -> List[Path]:
    files = os.listdir(directory)
    return [directory / f for f in files]


def listdir_matching(directory: Path, pattern: str) -> List[Path]:
    files = os.listdir(directory)
    matches = fnmatch.filter(files, pattern)
    return [directory / m for m in matches]


def unar(file: Path) -> None:
    # escaped_file_name = str(file).replace("'", r"\'")
    cmd.run(f'unar "{file}"', cwd=file.parent)


def create_backup_file(file: Path) -> None:
    """Copy file to {file}.backup

    :param Path file: File path to copy
    """

    shutil.copyfile(str(file), f"{str(file)}.backup")


def restore_from_backup_file(file: Path) -> None:
    """Copy {file}.backup to file

    :param Path file: File path to copy
    """

    shutil.copyfile(f"{file}.backup", file)


# def make_dir(directory: Path, check: bool = True) -> None:
#     """Make directory if it doesn't exist
#
#     :param str directory: Directory path to create
#     :param bool check: Whether to raise exceptions
#     """
#
#     if directory.exists():
#         return
#
#     try:
#         os.makedirs(str(directory))
#     except OSError as err:
#         if err.errno == errno.EEXIST:
#             LOG.error(f"Directory already exists at {Format.path(directory)}")
#         else:
#             LOG.error(f"Failed to create directory {Format.path(directory)}")
#         if check:
#             raise


# def remove_directory(dir_path: Path, check: bool = True) -> None:
#     """Remove directory at path
#
#     :param str dir_path: Path to directory to remove
#     :param bool check: Whether to raise errors
#     """
#
#     try:
#         shutil.rmtree(dir_path)
#     except shutil.Error:
#         LOG.error(f"Failed to remove directory {Format.path(dir_path)}")
#         if check:
#             raise


def has_contents(path: Path) -> bool:
    return not is_empty_dir(path)


def is_empty_dir(path: Path) -> bool:
    if not path.exists() or not path.is_dir():
        raise Exception(f"Directory at {path} doesn't exist")
    if not os.listdir(path):
        return True
    else:
        return False


def create_file(path: Path, contents: str) -> None:
    with path.open('w') as f:
        f.write(contents)
    assert path.is_file()
    assert not path.is_symlink()
    assert path.read_text().strip() == contents.strip()


def symlink_to(path: Path, target: Path) -> None:
    parent = path.parent
    fd = os.open(parent, os.O_DIRECTORY)
    os.symlink(target, path, dir_fd=fd)
    os.close(fd)
    assert path.exists()
    assert path.is_symlink()
    assert is_relative_symlink_from_to(path, str(target))


def symlink_relative_to(source: Path, target: Path, relative_to: Path) -> None:
    """Create relative symlink

    :param Path source: File to create symlink pointing to
    :param Path target: Symlink location
    :param Path relative_to: Directory source is relative to
    :raise ExistingFileError:
    :raise MissingSourceError:
    """

    source = source.relative_to(relative_to)
    try:
        path = target.parent
        fd = os.open(path, os.O_DIRECTORY)
        os.symlink(source, target, dir_fd=fd)
        os.close(fd)
    except OSError:
        # LOG.error(f"Failed to symlink file {Format.path(target)} -> {Format.path(source)}")
        raise


def copy_file(path: Path, destination: Path) -> None:
    shutil.copyfile(path, destination)
    assert destination.is_file()
    assert not destination.is_symlink()


def is_relative_symlink_from_to(symlink: Path, destination: str) -> bool:
    if not symlink.is_symlink():
        return False
    path = symlink.parent
    resolved_symlink = symlink.resolve()
    if not resolved_symlink.samefile(path / destination):
        return False
    link = os.readlink(symlink)
    is_relative = not Path(link).is_absolute()
    return is_relative


def copy_directory(from_dir: Path, to_path: Path):
    # TODO: Replace rmdir() with copytree(dirs_exist_ok=True) when support for Python 3.7 is dropped
    to_path.rmdir()
    shutil.copytree(from_dir, to_path, symlinks=True)


def copy_file(from_path: Path, to_path: Path):
    shutil.copyfile(from_path, to_path)


def copy(from_path: Path, to_path: Path):
    if from_path.is_dir():
        copy_directory(from_path, to_path)
    else:
        copy_file(from_path, to_path)
