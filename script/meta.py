#!/usr/bin/env python

import inspect
from typing import Any, List

def get_all_subclasses(cls) -> List[Any]:
    all_subclasses = []

    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses

class A(object):
    d = 1
    e = 5
    class Meta(object):
        f = 1
    def __init__(self):
        self.c = 1
        print(self.__class__.__dict__)
        print(self.d)
        print(self.e)
        # subclasses = get_all_subclasses(A)
        # print(subclasses)
        # for subclass in subclasses:
        #     print(subclass.d)
        mro = type.mro(type(self))
        mro.reverse()
        print(mro)
        # print(self.__class__.__dict__)
        # print(dir(self))

class B(A):
    class Meta(object):
        f = 1

    d = 42
    def __init__(self):
        self.c = 2
        super().__init__()
        # print(self.__class__.__dict__)


class C(B):
    class Meta(object):
        f = 1

    d = 42
    def __init__(self):
        self.c = 2
        super().__init__()
        # print(self.__class__.__dict__)


# a = A()
# # print(a.__class__.__dict__)
# print(a.d)

# b = B()
# print(b.__class__.__dict__)
# print(b.d)

c = C()
