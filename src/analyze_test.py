import json

from func_stack import FuncStack, FuncID


with open('/Users/eduardo/Desktop/bugfox-py/python_results/youtube-dl-41-buggy.json', 'r') as f1:
    base_func_stack_json = json.load(f1)
with open('/Users/eduardo/Desktop/bugfox-py/python_results/youtube-dl-41-buggy-src.json', 'r') as f2:
    base_src_json = json.load(f2)


base_func_stack = FuncStack(base_func_stack_json)


def print_func_id(funcstack):
    if funcstack.func_id != "ENTRY_POINT":

        if funcstack.func_id.to_str() not in base_src_json.keys():
            print((funcstack.func_id.to_str()))

    for fs in funcstack.callee:
        print_func_id(fs)

print_func_id(base_func_stack)