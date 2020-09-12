"""New syntax test file"""

from pathlib import Path
from typing import List, Optional


class ScenarioInfo:
    def __init__(self, tmp_path: Path):
        self._tmp_path = tmp_path

        self.example: Optional[str] = None
        self.branch: Optional[str] = None
        self.protocol: str = "https"
        self.version: Optional[str] = None
        self.offline: bool = False
        self.relative_dir: Optional[str] = None
        self.commit_messages_ahead: Optional[List[str]] = None
        self.commit_messages_behind: Optional[List[str]] = None
        self.number_commit_messages_ahead: Optional[int] = None
        self.number_commit_messages_behind: Optional[int] = None
        self.current_validation_test: Optional[str] = None

    @property
    def cmd_dir(self) -> Path:
        if self.relative_dir is not None:
            return self._tmp_path / self.relative_dir
        return self._tmp_path

