"""csv utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import csv
from pathlib import Path
from typing import List, Optional


def append_to_csv_file(file: Path, rows: List[List[str]]) -> None:
    with file.open('a') as csv_file:
        write_csv(csv_file, rows)


def create_csv_file(file: Path, header: List[str], rows: List[List[str]]) -> None:
    with file.open('w') as csv_file:
        write_csv(csv_file, rows, header)


def write_csv(csv_file, rows: List[List[str]], header: Optional[List[str]] = None) -> None:
    filewriter = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    if header is not None:
        filewriter.writerow(header)
    for row in rows:
        filewriter.writerow(row)
