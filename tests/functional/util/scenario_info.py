"""New syntax test file"""

from pathlib import Path
from typing import Optional


class ScenarioInfo:
    def __init__(self, tmp_path: Path):
        self._tmp_path = tmp_path

        self.example: Optional[str] = None
        self.branch: Optional[str] = None
        self.protocol: str = "https"
        self.version: Optional[str] = None
        self.offline: bool = False
        self.relative_dir: Optional[str] = None

    @property
    def cmd_dir(self) -> Path:
        if self.relative_dir is None:
            return self._tmp_path
        return self._tmp_path / self.relative_dir
