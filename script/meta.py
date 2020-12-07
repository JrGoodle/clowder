#!/usr/bin/env python

import inspect

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

class B(A):
    class Meta(object):
        f = 1

    d = 42
    def __init__(self):
        self.c = 2
        super().__init__()
        print(self.__class__.__dict__)


# a = A()
# # print(a.__class__.__dict__)
# print(a.d)

b = B()
# print(b.__class__.__dict__)
# print(b.d)
