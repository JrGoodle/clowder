"""New syntax test file"""

import os
import shutil
from pathlib import Path


def is_directory_empty(path: Path) -> bool:
    if path.exists() and path.is_dir():
        if not os.listdir(path):
            return True
        else:
            return False
    else:
        raise Exception(f"Directory at {path} doesn't exist")


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
    if not is_relative:
        return False
    return True


def copy_directory(from_dir: Path, to: Path):
    # TODO: Replace rmdir() with copytree(dirs_exist_ok=True) when support for Python 3.7 is dropped
    to.rmdir()
    shutil.copytree(from_dir, to, symlinks=True)
