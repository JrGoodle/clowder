"""New syntax test file"""

import os
import shutil
from pathlib import Path


def is_directory_empty(path: Path) -> bool:
    if path.exists() and path.is_dir():
        if not os.listdir(path):
            print("Directory is empty")
            return True
        else:
            print("Directory is not empty")
            return False
    else:
        print("Given Directory don't exists")
        raise Exception


def create_file(path: Path) -> None:
    with open(path, 'w') as _:
        pass
    assert path.exists()
    assert path.is_file()
    assert not path.is_dir()
    assert not path.is_symlink()


def create_symlink(source: Path, target: Path) -> None:
    assert source.exists()
    assert not target.exists()
    os.symlink(source, target)
    assert is_symlink_from_to(target, source)


def is_valid_symlink(path: Path) -> bool:
    return path.is_symlink() and path.exists() and path.is_file()


def is_symlink_from_to(symlink: Path, destination: Path) -> bool:
    return is_valid_symlink(symlink) and destination.samefile(symlink.resolve())


def copy_directory(from_dir: Path, to: Path):
    # TODO: Replace rmdir() with copytree(dirs_exist_ok=True) when support for Python 3.7 is dropped
    to.rmdir()
    shutil.copytree(from_dir, to, symlinks=True)
