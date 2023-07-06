"""sort type enum

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from enum import auto, unique
from typing import List

from pygoodle.enum import AutoLowerName


@unique
class SortType(AutoLowerName):
    NAME = auto()
    SIZE = auto()
    DOWNLOADED = auto()
    TYPE = auto()

    @classmethod
    def all_values(cls) -> List[str]:
        return [e.value for e in SortType]
