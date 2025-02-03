# src = """
#     @staticmethod
#     def __aiter__(*args, **kwargs):
#         def Bugbee___aiter__(self):
#             raise Return(self)
#
#         Bugbee_build(
#             "/Users/eduardo/Desktop/BugsInPy/framework/bin/temp/base-version/tornado-10/tornado/gen.py@line482/Func@__aiter__,9377f047f79def92ebaec6b1a0f2cc48d8b0445bb99fdf307b19a1982d2aff6f",
#             args,
#             kwargs,
#         )
#         return_val = Bugbee___aiter__(*args, **kwargs)
#         Bugbee_complete(args, kwargs, return_val)
#         return return_val
# """
# import black
# import ast
# cleaned_src = black.format_str(src, mode=black.FileMode())
# print(cleaned_src)


# import pickle
# f = open("/Users/eduardo/Desktop/bugfox-py/testfile.txt", "w")
# a = {"s": f}
# try:
#     pickle.dumps(a)
# except:
#     a = f.write("fd")
#     print(a)



# class A:
#     a = []
#
#     def foo(self):
#
#         def bar(b=self.a):
#
#             print(b)
#
#         bar()
#
# A().foo()

# import jsonpickle
# a = b"fds"
# print(type(a))
# b = jsonpickle.dumps(a)
# print(b)
# import json
# with open("/Users/eduardo/Desktop/bugfox-py/Bugbee/examples/trace.json") as f:
#     a = json.load(f)
# print(a)


# def gene():
#     for i in range(10):
#         yield i

# def fun_generator():
#     yield "Hello world!!"
#     yield "hello"
#
#
# obj = fun_generator()
#
# print(type(obj))
#
# print(next(obj))
# print(next(obj))
import jsonpickle
import json
import dill
# print(next(a))
# print(next(a))
# b = jsonpickle.dumps(a)
# print(next(a))
# print(next(a))


# def gene():
#     for i in range(10):
#         yield i
#
#
# a = gene()
# print(next(a))
# print(next(a))
# # import copy
# # copy.deepcopy(a)


import dill

def my_generator():
    for i in range(3):
        yield i

gen = my_generator()

# Serialize generator
serialized = dill.dumps(gen)

# Deserialize and continue execution
deserialized_gen = dill.loads(serialized)
print(list(deserialized_gen))  # Output: [0, 1, 2]