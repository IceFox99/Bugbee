from Bugbee.src import util

obj1 = 1
print(util.to_json(obj1))

obj2 = 1.1
print(util.to_json(obj2))

obj3 = "str"
print(util.to_json(obj3))

obj4 = b"str"
print(util.to_json(obj4))

obj5 = [1, 2, 3]
print(util.to_json(obj5))

obj6 = {1, 2, 3}
print(util.to_json(obj6))

obj7 = (1, 2, 3)
print(util.to_json(obj7))

obj8 = {"s1": 1, "s2": 2, "s3": 3}
print(util.to_json(obj8))


class classA:
    def __init__(self, obj):
        self.attr_a = obj


obj9 = classA("fs")
print(util.to_json(obj9))


class classB:
    pass


class classC:
    pass


obj10 = classB()
obj11 = classC()
obj10.attr = obj11
obj11.attr = obj10

print(util.to_json(obj10))

obj12 = {}
obj13 = {"obj12":obj12}
obj12["obj13"] = obj13
print(util.to_json(obj12))


def func1():
    pass


print(util.to_json(func1))
