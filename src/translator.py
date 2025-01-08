from utils import to_json
import ast
import copy
import black
import os

class Translator(ast.NodeTransformer):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def add_header(self, module_node):
        pass

    def generate_code_block(self, node, func_id):
        block_code = """
Bugbee.build(\"\", args, kwargs)
return_val = Bugbee_foo(*args, **kwargs)
Bugbee.complete(args, kwargs, return_val)
return return_val
        """
        block_ast = ast.parse(block_code)

        # Replace the function ID
        block_ast.body[0].value.args[0].value = func_id

        # Replace the function name
        block_ast.body[1].value.func.id = node.name

        return block_ast.body

    def visit_FunctionDef(self, node):
        func_id = f"{self.curr_file_path}@line{node.lineno}/Func@node.name"

        # Visit its subtree first
        self.generic_visit(node)
        inner_func_node = copy.deepcopy(node)
        inner_func_node.name = f"Bugbee_{node.name}"

        # Insert the inner function definition at the beginning
        node.body = [inner_func_node]
        node.body.extend(self.generate_code_block(inner_func_node, func_id))
        node.args = ast.parse("def f(*args, **kwargs):\n\tpass").\
                body[0].args
        return node

    def visit_AsyncFunctionDef(self, node):
        func_id = f"{self.curr_file_path}@line{node.lineno}/Func@node.name"

        # Visit its subtree first
        self.generic_visit(node)

        inner_func_node = copy.deepcopy(node)
        inner_func_node.name = f"Bugbee_{node.name}"

        # Insert the inner function definition at the beginning
        node.body = [inner_func_node]
        node.body.extend(self.generate_code_block(node, func_id))
        node.args = ast.parse("def f(*args, **kwargs):\n\tpass").\
                body[0].args
        return node

    def visit_Lambda(self, node):
        func_id = f"{self.curr_file_path}@line{node.lineno}/Lambda"

        # Visit its subtree first
        self.generic_visit(node)

        # Transform the lambda AST
        bugbee_lambda = ast.parse(f"Bugbee_lambda(\"{func_id}\")").body[0].value
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
        modified_code = black.format_str(ast.unparse(modified_tree), \
                mode=black.FileMode())

        # TODO
        print(modified_code)
