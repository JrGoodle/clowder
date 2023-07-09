"""reflection utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

# import inspect
from typing import Any, List, Optional, Type


def all_subclasses(cls) -> List[Type]:
    subclasses = []
    for subclass in cls.__subclasses__():
        subclasses.append(subclass)
        subclasses.extend(all_subclasses(subclass))
    return subclasses


def class_member(obj: Any, name: str) -> Optional[Any]:
    class_dict = obj.__dict__
    if name in class_dict:
        return class_dict[name]
    return None


def update_attr(obj: Any, name: str, value: Any, ignore_missing: bool = True):
    has_attr = hasattr(value, name)
    if not ignore_missing and not has_attr:
        raise Exception(f'Missing attribute {name} on {value}')
    if has_attr:
        meta_value = getattr(value, name)
        setattr(obj, name, meta_value)


def method_resolution_order(obj, reverse: bool = False) -> List[Type]:
    # classes = inspect.getmro(type(obj))
    classes = type.mro(type(obj))
    if not reverse:
        return classes
    classes.reverse()
    return classes
