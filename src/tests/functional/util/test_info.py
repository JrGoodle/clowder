"""New syntax test file"""

from typing import Optional


class TestInfo:
    def __init__(self):
        self.example: Optional[str] = None
        self.branch: Optional[str] = None
        self.protocol: str = "https"
        self.version: Optional[str] = None
