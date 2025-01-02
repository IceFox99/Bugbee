import os, sys
sys.path.append(os.path.abspath(os.path.join(\
        os.path.dirname(__file__), '../src')))
from utils import to_json

obj1 = 1
print(to_json(obj1))

obj2 = 1.1
print(to_json(obj2))

obj3 = "str"
print(to_json(obj3))

obj4 = b"str"
print(to_json(obj4))

obj5 = [1, 2, 3]
print(to_json(obj5))

obj6 = {1, 2, 3}
print(to_json(obj6))

obj7 = (1, 2, 3)
print(to_json(obj7))

obj8 = {"s1": 1, "s2": 2, "s3": 3}
print(to_json(obj8))


class classA:
    def __init__(self, obj):
        self.attr_a = obj


obj9 = classA("fs")
print(to_json(obj9))


class classB:
    pass


class classC:
    pass


obj10 = classB()
obj11 = classC()
obj10.attr = obj11
obj11.attr = obj10

print(to_json(obj10))

obj12 = {}
obj13 = {"obj12":obj12}
obj12["obj13"] = obj13
print(to_json(obj12))


def func1():
    pass


print(to_json(func1))

def is_even(n):
    if n == 0:
        return True
    else:
        return is_odd(n - 1)


def is_odd(n):
    if n == 0:
        return False
    else:
        return is_even(n - 1)


print(to_json(is_odd))
