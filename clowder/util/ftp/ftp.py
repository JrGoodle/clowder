"""ftp

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import ftplib
from pathlib import Path
from typing import Callable, List, Generator

from resource_pool import LazyPool

import pygoodle.filesystem as fs
from pygoodle.tasks import ProgressTask, ProgressTaskPool
from pygoodle.console import CONSOLE, disable_output

from .file_type import FileType
from .file_wrapper import FileWrapper


class CancelledDownloadError(Exception):
    pass


class FileInfo:

    def __init__(self, path: Path, size: int):
        self.path: Path = path
        self.name: str = path.name
        self.size: int = size

    def __lt__(self, other: 'FileInfo') -> bool:
        return str(self.path).lower() < str(other.path).lower()


class DirectoryInfo:

    def __init__(self, ftp: ftplib.FTP, directory: Path, recursive: bool = True):
        self.directory: Path = directory
        self.files: List[FileInfo] = []
        self._directories: List[Path] = []
        self.recursive = recursive

        self._load_directory(ftp, directory)

    def _load_directory(self, ftp: ftplib.FTP, directory: Path) -> None:
        results = [((directory / name).resolve(), facts)
                   for name, facts in ftp.mlsd(str(directory), facts=["type", "size"])]

        files = [FileInfo(name, int(facts['size'])) for name, facts in results if facts['type'] == 'file']
        self.files += files

        directories = [name for name, facts in results if facts['type'] == 'dir']
        self._directories += directories

        if not self.recursive:
            return

        for directory in directories:
            self._load_directory(ftp, directory)

    @property
    def size(self) -> int:
        if not self.recursive:
            raise Exception('Size can only be calculated when recursive')
        if not self.files:
            return 0
        return sum([f.size for f in self.files])

    @property
    def directories(self) -> List[Path]:
        directory_paths = [d for d in self._directories]
        return sorted(directory_paths, key=lambda path: str(path).lower())

    @property
    def file_paths(self) -> List[Path]:
        file_paths = [f.path for f in self.files]
        return sorted(file_paths, key=lambda path: str(path).lower())

    @property
    def all_paths(self) -> List[Path]:
        file_paths = [f.path for f in self.files]
        directory_paths = [d for d in self._directories]
        return sorted(file_paths + directory_paths, key=lambda path: str(path).lower())


class FTP:

    def __init__(self, host: str, user: str, password: str,
                 download_dir: Path, base_dir: Path = Path('/'), pool_size: int = 1):
        self.download_dir: Path = download_dir
        self.pool_size: int = pool_size
        self.base_dir = base_dir

        def make_ftp() -> ftplib.FTP:
            return ftplib.FTP(host=host, user=user, passwd=password)
        self._ftp_pool: LazyPool[ftplib.FTP] = LazyPool(factory=make_ftp, pool_size=pool_size)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        while len(self._ftp_pool) > 0:
            with self._ftp_pool.get() as ftp:
                ftp.close()

    @disable_output
    def download(self, path: Path) -> Path:
        file_type = self._file_type(path)
        if file_type is FileType.FILE:
            files = [FileInfo(path, self._get_file_size(path))]
        elif file_type is FileType.DIR:
            with self.reserve_ftp() as ftp:
                directory_info = DirectoryInfo(ftp, path)
            self._make_download_dirs(path, directory_info)
            files = directory_info.files
        else:
            raise Exception('Unknown file type')

        download_path = self._get_download_path(path)

        class DownloadTaskPool(ProgressTaskPool):
            def after_tasks(self, tasks: List[ProgressTask]) -> None:
                super().after_tasks(tasks)
                if self.cancelled:
                    CONSOLE.stdout(f'Remove {download_path}', force=True)
                    fs.remove(download_path)

        ftp = self

        class DownloadTask(ProgressTask):
            def __init__(self, file: FileInfo):
                super().__init__(file.name, units='bytes', total=file.size)
                self._file: FileInfo = file

            def run(self) -> None:
                def callback(data):
                    if self.cancelled:
                        raise CancelledDownloadError(f'FTP download of {self._file.name} was cancelled')
                    self.progress.update_subtask(self._file.name, advance=len(data))

                ftp.download_file(self._file, callback)

        download_tasks = [DownloadTask(file) for file in files]
        pool = DownloadTaskPool(jobs=self.pool_size, title='Files', units='files')
        pool.run(download_tasks)
        CONSOLE.stdout(f'Downloaded {len(files)} files', force=True)
        return download_path

    def get_file_wrapper(self, path: Path) -> FileWrapper:
        file_type = self._file_type(path)
        if file_type is FileType.DIR:
            return FileWrapper(path.name, self._get_directory_size(path), file_type)
        elif file_type is FileType.FILE:
            return FileWrapper(path.name, self._get_file_size(path), file_type)

    def list_dir(self, directory: Path) -> List[Path]:
        if not directory.is_absolute():
            directory = self.base_dir / directory
        # FIXME: Filter *.meta files
        # TODO: Use ssh to ask rutorrent for unfinished downloads
        with self.reserve_ftp() as ftp:
            directory_info = DirectoryInfo(ftp, directory, recursive=False)
        return directory_info.all_paths

    def reserve_ftp(self) -> Generator[ftplib.FTP, None, None]:
        return self._ftp_pool.reserve()

    def download_file(self, file: FileInfo, callback: Callable = lambda _: None) -> None:
        output_file = self._get_download_path(file.path)
        with output_file.open('wb') as output:
            with self.reserve_ftp() as ftp:
                def _callback(data):
                    output.write(data)
                    callback(data)
                ftp.retrbinary(f'RETR {file.path}', _callback)

    def _file_type(self, file: Path) -> FileType:
        with self.reserve_ftp() as ftp:
            if 'type=dir' in ftp.sendcmd(f'MLST {file}'):
                return FileType.DIR
            else:
                return FileType.FILE

    def _get_directory_size(self, directory: Path) -> int:
        with self.reserve_ftp() as ftp:
            directory_info = DirectoryInfo(ftp, directory)
        size = sum([f.size for f in directory_info.files])
        return size

    def _get_download_path(self, path: Path) -> Path:
        return fs.replace_path_prefix(path, self.base_dir, self.download_dir)

    def _get_file_size(self, file: Path) -> int:
        with self.reserve_ftp() as ftp:
            ftp.voidcmd('TYPE I')
            size = ftp.size(str(file))
        return size

    def _make_download_dirs(self, path: Path, directory_info: DirectoryInfo) -> None:
        fs.make_dir(self._get_download_path(path))
        for directory in directory_info.directories:
            fs.make_dir(self._get_download_path(directory))
