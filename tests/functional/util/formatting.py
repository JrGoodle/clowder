"""New syntax test file"""

from typing import List, Optional

from parse_type import TypeBuilder


def parse_string(text) -> str:
    return str(text)


list_str_commas = TypeBuilder.with_many(parse_string, listsep=",")
list_str_newlines = TypeBuilder.with_many(parse_string, listsep="\n")


def list_from_string(text: str, sep: Optional[str] = None) -> List[str]:
    return text.split(sep=sep)
