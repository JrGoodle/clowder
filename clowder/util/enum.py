"""enum utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from enum import Enum
from typing import List


class UnknownEnumCaseError(Exception):
    pass


class AutoLowerName(Enum):
    def _generate_next_value_(name: str, start: int, count: int, last_values: List[str]) -> str:  # noqa
        return name.lower()
