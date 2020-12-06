"""New syntax test file"""

from parse_type import TypeBuilder


def parse_string(text) -> str:
    return str(text)


list_str_commas = TypeBuilder.with_many(parse_string, listsep=",")
list_str_newlines = TypeBuilder.with_many(parse_string, listsep="\n")
