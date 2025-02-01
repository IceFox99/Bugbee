import json
import jsonpickle


# def gene():
#     for i in range(10):
#         yield i
#
#
# a = gene()
# b = jsonpickle.dumps(a)
# print(json.loads(b))
# print(next(a))

# def foo():
#     for i in range(10):
#         yield
#
#
# import pickle, copy
#
# a = [foo()]
# print(type(a))
# b = copy.deepcopy(a)
# print(a)
#
# try:
#     pickle.dumps(a)
# except Exception as e:
#     print(next(a[0]))
from Bugbee.src import utils, utils2
import copy
class A:
    def __init__(self):
        self.attr = ""

a = A()

class B:
    def __init__(self, attr):
        self.attr = attr

b = B(a)
a.attr = b
print(json.dumps(jsonpickle.dumps(a)))
def foo():
    pass

print(utils2.to_json(foo))
print(next(foo()))