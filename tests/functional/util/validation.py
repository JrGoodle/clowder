"""New syntax test file"""

import glob
from pathlib import Path
from typing import List


def get_all_project_property_test_files(project_property: str) -> List[Path]:
    jpgFilenamesList = glob.glob('145592*.jpg')
    return []
