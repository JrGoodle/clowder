"""New syntax test file"""

from typing import Optional


class ScenarioInfo:
    def __init__(self):
        self.example: Optional[str] = None
        self.branch: Optional[str] = None
        self.protocol: str = "https"
        self.version: Optional[str] = None
        self.offline: bool = False
