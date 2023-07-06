"""unrar utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from typing import Dict, List, Union

from pygoodle.format import Format

from .file_type import FileType


class FileWrapper:

    csv_header: List[str] = [
        'name',
        'size',
        'file_type',
        'downloaded'
    ]

    def __init__(self, name: str, size: int, file_type: Union[FileType, str], downloaded: Union[bool, str] = False):
        self.name: str = name
        self.size: int = int(size)

        if isinstance(file_type, str):
            self.file_type: str = file_type
        elif isinstance(file_type, FileType):
            self.file_type: str = file_type.value
        else:
            raise Exception('Unknown file type')

        if isinstance(downloaded, str):
            self.downloaded: bool = True if downloaded == 'True' else False
        elif isinstance(downloaded, bool):
            self.downloaded: bool = downloaded
        else:
            raise Exception('Unknown downloaded type')

    def __eq__(self, other) -> bool:
        if isinstance(other, FileWrapper):
            return self.name == other.name and self.size == other.size and self.downloaded == other.downloaded
        return False

    def __hash__(self):
        return hash(self.name) ^ hash(self.size) ^ hash(self.downloaded)

    def __lt__(self, other: 'FileWrapper') -> bool:
        return self.name.lower() < other.name.lower()

    @property
    def csv(self) -> List[str]:
        csv = []
        for prop in FileWrapper.csv_header:
            csv.append(getattr(self, prop.lower()))
        return csv

    @property
    def formatted_row(self) -> List[str]:
        return [
            self.name,
            self.get_file_type().formatted_value,
            Format.size(self.size),
            Format.bool(self.downloaded)
        ]

    @property
    def lower_name(self) -> str:
        return self.name.lower()

    def get_file_type(self) -> FileType:
        return FileType(self.file_type)

    @classmethod
    def from_csv(cls, csv: Dict[str, str]) -> 'FileWrapper':
        kwargs = {column: row if row else None for (column, row) in csv.items()}
        return FileWrapper(**kwargs)
