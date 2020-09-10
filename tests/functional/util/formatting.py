"""New syntax test file"""

import re
from typing import List, Optional

from parse_type import TypeBuilder


def parse_string(text) -> str:
    return str(text)


list_str_commas = TypeBuilder.with_many(parse_string, listsep=",")
list_str_newlines = TypeBuilder.with_many(parse_string, listsep="\n")


def list_from_string(text: str, sep: Optional[str] = None) -> List[str]:
    return text.split(sep=sep)


def clean_escape_sequences(string: str) -> str:
    reaesc = re.compile(r'\x1b[^m]*m')
    return reaesc.sub('', string)


def remove_prefix(text: str, prefix: str) -> str:
    if text.startswith(prefix):
        return text[len(prefix):]
    return text
