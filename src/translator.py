import funcstack
import ast
import copy
import black
import os, sys
import hashlib

class Translator(ast.NodeTransformer):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.func_code = {}

    def add_header(self, module_node):
        include_path = os.path.abspath(os.path.dirname(__file__))
        header_code = f"""
import os, sys
sys.path.append(\"{include_path}\")
from bugbeeinclude import Bugbee_build, Bugbee_complete 
        """
        header_ast = ast.parse(header_code)
        module_node.body[:0] = header_ast.body

    def generate_code_block(self, node, func_id):
        block_code = """
Bugbee_build(\"\", args, kwargs)
return_val = Bugbee_foo(*args, **kwargs)
Bugbee_complete(args, kwargs, return_val)
return return_val
        """
        block_ast = ast.parse(block_code)

        # Replace the function ID
        block_ast.body[0].value.args[0].value = func_id

        # Replace the function name
        block_ast.body[1].value.func.id = node.name

        return block_ast.body

    @staticmethod
    def generate_args():
        return ast.parse("def f(*args, **kwargs):\n\tpass").body[0].args

    def visit_ClassDef(self, node):
        for child_node in node.body:
            if isinstance(child_node, ast.FunctionDef) or \
                    isinstance(child_node, ast.AsyncFunctionDef):
                if len(child_node.decorator_list) == 0:
                    child_node.is_method = True
                else:
                    for decorator in child_node.decorator_list:
                        if decorator.id == 'staticmethod':
                            child_node.is_method = False
                            break
        self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node):
        cleaned_src = black.format_str(ast.unparse(node), \
                mode=black.FileMode())
        func_id = f"{self.curr_file_path}@line{node.lineno}/\
{funcstack.FUNC}@{node.name},\
{hashlib.sha256(cleaned_src.encode('utf-8')).hexdigest()}"
        self.func_code[func_id] = cleaned_src

        # Visit its subtree first
        self.generic_visit(node)
        inner_func_node = copy.deepcopy(node)
        inner_func_node.name = f"Bugbee_{node.name}"

        # Insert the inner function definition at the beginning
        node.body = [inner_func_node]
        code_block = self.generate_code_block(inner_func_node, func_id)
        
        if hasattr(node, "is_method") and node.is_method:
            first_arg = node.args.args[0]
            node.args = Translator.generate_args()
            node.args.args.insert(0, first_arg)
            code_block[1].value.args.insert(0, first_arg)
        else:
            node.args = Translator.generate_args()
        node.body.extend(code_block)
        return node

    def visit_AsyncFunctionDef(self, node):
        cleaned_src = black.format_str(ast.unparse(node), \
                mode=black.FileMode())
        func_id = f"{self.curr_file_path}@line{node.lineno}/\
{funcstack.ASYNCFUNC}@{node.name},\
{hashlib.sha256(cleaned_src.encode('utf-8')).hexdigest()}"
        self.func_code[func_id] = cleaned_src

        # Visit its subtree first
        self.generic_visit(node)

        inner_func_node = copy.deepcopy(node)
        inner_func_node.name = f"Bugbee_{node.name}"

        # Insert the inner function definition at the beginning
        node.body = [inner_func_node]
        code_block = self.generate_code_block(inner_func_node, func_id)
        if hasattr(node, "is_method") and node.is_method:
            first_arg = node.args.args[0]
            node.args = Translator.generate_args()
            node.args.args.insert(0, first_arg)
            code_block[1].value.args.insert(0, first_arg)
        else:
            node.args = Translator.generate_args()
        node.body.extend(code_block)
        return node

    def visit_Lambda(self, node):
        cleaned_src = black.format_str(ast.unparse(node), \
                mode=black.FileMode())
        func_id = f"{self.curr_file_path}@line{node.lineno}/\
{funcstack.LAMBDA},{hashlib.sha256(cleaned_src.encode('utf-8')).hexdigest()}"
        self.func_code[func_id] = cleaned_src

        # Visit its subtree first
        self.generic_visit(node)

        # Transform the lambda AST
        bugbee_lambda = ast.parse(f"Bugbee_execLambda(\"{func_id}\")").body[0].value
        bugbee_lambda.args.append(ast.parse(copy.deepcopy(\
                node.body)))
        node.body = bugbee_lambda
        return node

    # @file_path: the relative path of target file
    def translate(self, file_path):
        self.curr_file_path = file_path
        with open(file_path, "r") as src:
            src_code = src.read()

        tree = ast.parse(src_code)
        modified_tree = self.visit(tree)
        self.add_header(modified_tree)
        modified_code = black.format_str(ast.unparse(modified_tree), \
                mode=black.FileMode())

        # TODO
        with open("/home/username/new-Bugbee-example/test_math.py", "w") as f:
            f.write(modified_code)
