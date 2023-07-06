"""general utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

# from abc import abstractmethod
# from typing import Protocol
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, MutableSequence


# class Comparable(Protocol):
#     """Protocol for annotating comparable types."""
#
#     @abstractmethod
#     def __lt__(self: 'CT', other: 'CT') -> bool:
#         pass


T = TypeVar('T')
# CT = TypeVar('CT', bound=Comparable)


def is_even(number: int) -> bool:
    return (number % 2) == 0


def sorted_tuple(items: MutableSequence[T], unique: bool = False, reverse: bool = False,
                 key: Optional[Callable] = None) -> Tuple[T, ...]:
    if unique:
        items = set(items)
    return tuple(sorted(items, reverse=reverse, key=key))


def values_sorted_by_key(dictionary: Dict[Any, T]) -> List[T]:
    return [dictionary[key] for key in sorted(dictionary.keys())]
