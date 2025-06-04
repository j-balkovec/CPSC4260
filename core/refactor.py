# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sun Apr 20th, 2025
#
# __file__: refactor_duplicates.py
#
# __brief__: Script to refactor duplicated code by extracting common blocks into functions
#            and replacing duplicates with function calls.
#
# =========
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# =========

import ast
import hashlib
from typing import Tuple

from utils.logger import setup_logger
from utils.exceptions import CodeProcessingError
from utils.utility import _read_file_contents

from core.duplicated_finder import (
    _tokenize_block,
    _jaccard_similarity,
    _remove_comments,
)

from core.constants import DUPS_THRESHOLD

# Logger setup
refactor_logger = setup_logger(
    name="refactor_duplicates.py_logger", log_file="refactor_duplicates.log"
)


class DuplicateRefactorer(ast.NodeTransformer):
    """_summary_

    Args:
        ast (_type_): Parent class
    """

    def __init__(self, duplicates, functions_map, use_wrapper: bool = True):
        """_summary_

        Args:
            duplicates (list): list of tuples containing function names and their Jaccard
                                 similarity
            functions_map (dict): dictionary mapping function names to their AST nodes
            use_wrapper (bool, optional): whether to use a wrapper function or not. Defaults to True.
        """
        super().__init__()
        self.dup_funcs = {f for f1, f2, _ in duplicates for f in (f1, f2)}

        self.use_wrapper = use_wrapper
        self.original_func = duplicates[0][0] if duplicates else None

        key = duplicates[0][0]
        if key not in functions_map:
            raise ValueError(f"Duplicate refers to unknown function: {key}")

        func_node = functions_map[key]
        sample = func_node.body
        self.helper = _make_helper_node(
            func_name=key, args=[arg.arg for arg in func_node.args.args], body=sample
        )
        refactor_logger.info(f"Helper function created: {self.helper.name}")
        refactor_logger.info(f"dups: {self.dup_funcs}")
        refactor_logger.info(f"use_wrapper set to: {self.use_wrapper}")

    def visit_Module(self, node: ast.Module):
        """_summary_
                * Module Level
        Args:
            node (ast.Module): node to be transformed

        Returns:
            ast.Module: transformed node
        """
        if not self.use_wrapper:
            # rm dups except the original
            node.body = [
                n
                for n in node.body
                if not (
                    isinstance(n, ast.FunctionDef)
                    and n.name in self.dup_funcs
                    and n.name != self.original_func
                )
            ]

        if self.use_wrapper and self.helper:
            node.body.insert(0, self.helper)

        self.generic_visit(node)

        return node

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """_summary_
                * Function Level
        Args:
            node (ast.FunctionDef): node to be transformed

        Returns:
            _type_: transformed node
        """
        if not self.use_wrapper:
            # if the function is not a duplicate, return it as is
            if node.name in self.dup_funcs and node.name != self.original_func:
                return None
            else:
                return node
        else:
            # if the function is a duplicate, replace its body with a call to the helper
            if node.name in self.dup_funcs:
                call = ast.Call(
                    func=ast.Name(self.helper.name, ast.Load()),
                    args=[ast.Name(arg.arg, ast.Load()) for arg in node.args.args],
                    keywords=[],
                )
                has_return_with_value = any(
                    isinstance(stmt, ast.Return) and stmt.value is not None
                    for stmt in node.body
                )

                if has_return_with_value:
                    new_body = [ast.Return(value=call)]
                else:
                    new_body = [ast.Expr(value=call)]

                node.body = new_body
            return node

    def replace_calls_with_helper(self, node: ast.AST) -> ast.AST:
        """_summary_

        Args:
            node (ast.AST): _description_

        Returns:
            ast.AST: _description_
        """
        class CallReplacer(ast.NodeTransformer):
            """_summary_

            Args:
                ast (object): Parent class
            """
            def __init__(self, dup_funcs, helper_name, use_wrapper, original_func):
                """_summary_

                Args:
                    dup_funcs (list): list of function names that are duplicates
                    helper_name (str): name of the helper function
                """
                self.dup_funcs = dup_funcs
                self.helper = helper_name
                self.use_wrapper = use_wrapper
                self.original_func = original_func

            def visit_Call(self, call_node: ast.Call) -> ast.Call:
                """_summary_

                Args:
                    call_node (ast.Call): node to be transformed

                Returns:
                    ast.Call: transformed node
                """
                self.generic_visit(call_node)
                if (
                    not self.use_wrapper
                    and isinstance(call_node.func, ast.Name)
                    and call_node.func.id in self.dup_funcs
                    and call_node.func.id != self.original_func
                ):
                    call_node.func.id = self.original_func
                return call_node

        replacer = CallReplacer(
                    self.dup_funcs, self.helper.name, self.use_wrapper, self.original_func
                    )
        return replacer.visit(node)


def _make_helper_node(func_name: str, args: list, body: list) -> ast.FunctionDef:
    """_summary_

    Args:
        func_name (str): name of the function
        args (list): list of arguments
        body (list): list of statements

    Returns:
        ast.FunctionDef: function definition node
    """
    h = hashlib.md5(func_name.encode()).hexdigest()
    helper_name = f"_common_logic_{h}"

    new_args = ast.arguments(
        posonlyargs=[],
        args=[ast.arg(arg=arg, annotation=None) for arg in args],
        vararg=None,
        kwonlyargs=[],
        kw_defaults=[],
        kwarg=None,
        defaults=[],
    )

    return ast.FunctionDef(
        name=helper_name, args=new_args, body=body, decorator_list=[], returns=None
    )

# ============================================================================
#               DEPRECATED BECAUSE THE ONE BELOW WORKS BETTER
# ============================================================================
# def _refactor_with_ast(source_code: str, duplicates: list, use_wrapper: bool = True) -> str:
#     """_summary_
#
#     Args:
#         source_code (str): source code to be refactored
#         duplicates (list): list of tuples containing function names and their Jaccard similarity
#
#     Returns:
#         str: refactored source code
#     """
#     tree = ast.parse(source_code)
#
#     func_map = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
#     transformer = DuplicateRefactorer(duplicates, func_map, use_wrapper)
#
#     new_tree = transformer.visit(tree)
#     ast.fix_missing_locations(new_tree)
#
#     return ast.unparse(new_tree)

def _refactor_with_ast(source_code: str, duplicates, use_wrapper: bool = True) -> str:
    tree = ast.parse(source_code)

    func_map = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}

    transformer = DuplicateRefactorer(duplicates, func_map, use_wrapper)
    tree = transformer.visit(tree)
    tree = ast.fix_missing_locations(tree)

    if not use_wrapper:
        tree = transformer.replace_calls_with_helper(tree)

    return ast.unparse(tree)


def _extract_functions(source_code: str) -> dict:
    """_summary_

    Args:
        source_code (str): source code to be processed

    Returns:
        dict: dictionary mapping function names to their AST nodes
    """
    functions = {}
    source_code = _remove_comments(source_code)
    tree = ast.parse(source_code)
    lines = source_code.splitlines(keepends=True)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):

            func_name = node.name.strip()
            if func_name != node.name:
                refactor_logger.warning(
                    f"Function name sanitized: original='{node.name}' → stripped='{func_name}'"
                )

            if not hasattr(node, "end_lineno"):
                start_line = node.lineno - 1
                indent = len(lines[start_line]) - len(lines[start_line].lstrip())
                end_line = start_line + 1
                while end_line < len(lines):
                    line = lines[end_line]
                    if (
                        line.strip()
                        and (len(line) - len(line.lstrip()) <= indent)
                        and not line.lstrip().startswith("#")
                    ):
                        break
                    end_line += 1
                end_line = min(end_line + 1, len(lines))
            else:
                start_line = node.lineno - 1
                end_line = node.end_lineno

                while end_line < len(lines) and (
                    lines[end_line].strip() == ""
                    or lines[end_line].lstrip().startswith("#")
                ):
                    end_line += 1

            start_offset = sum(len(line) for line in lines[:start_line])
            end_offset = sum(len(line) for line in lines[:end_line])

            func_text = "".join(lines[start_line:end_line])
            functions[node.name] = {
                "name": node.name,
                "start": start_offset,
                "end": end_offset,
                "text": func_text,
            }

    refactor_logger.debug(f"Extracted functions: {functions}")
    refactor_logger.debug(f"Keys: {functions.keys()}")
    return functions

def _find_duplicates(func_map: dict) -> list:
    """_summary_

    Args:
        func_map (dict): dictionary mapping function names to their AST nodes

    Returns:
        list: list of tuples containing function names and their Jaccard similarity
    """
    tokens = {name: _tokenize_block(data["text"]) for name, data in func_map.items()}
    duplicates = []

    seen = set()
    for a, tokens_a in tokens.items():
        for b, tokens_b in tokens.items():
            if a >= b or (a, b) in seen:
                continue
            sim = _jaccard_similarity(tokens_a, tokens_b)
            if sim >= DUPS_THRESHOLD:
                duplicates.append((a, b, sim))
                seen.add((a, b))

    refactor_logger.debug(f"Found duplicates: {duplicates}")
    return duplicates

# ============================== CALLABLE ===========================
def refactor_duplicates(filepath, use_wrapper: bool = True) -> Tuple[str, bool]:
    """_summary_

    Args:
        filepath (_type_): filepath to be processed
        use_wrapper (_type_): whether to extract the common logic/functionality and
                              wrap it with the original function -> to preserve context

        EXAMPLE:

            def area(a, b):
                return a*b

            def force(m, a):
                return m*a

            Instead of one function getting deleted, and calls getting replaced
            we create a separate function called _common_logic_<hash> (to avoid name clashes).
            This allows us to preserve context.

    Raises:
        CodeProcessingError: if the file could not be read

    Returns:
        str: refactored source code
    """
    source_code = _read_file_contents(filepath)
    if not source_code:
        raise CodeProcessingError(f"Could't read any code from: {filepath}")

    functions_dict = _extract_functions(source_code)
    duplicates = _find_duplicates(functions_dict)

    if not duplicates:
        return "# No duplicates found, nothing to refactor.", False

    return _refactor_with_ast(source_code, duplicates, use_wrapper), True  # tuple(str, bool)


# ===================================================================
# >                          DEBUG ONLY
# ===================================================================
def _debug_dict(source_code: str, threshold: float = 0.85) -> dict:
    debug = {}

    func_map = _extract_functions(source_code)
    debug["functions"] = {
        name: {"start": data["start"], "end": data["end"], "text": data["text"]}
        for name, data in func_map.items()
    }

    token_map = {name: _tokenize_block(data["text"]) for name, data in func_map.items()}
    debug["tokens"] = token_map

    similarities = []
    for a, tokens_a in token_map.items():
        for b, tokens_b in token_map.items():
            if a >= b:
                continue
            sim = _jaccard_similarity(tokens_a, tokens_b)
            similarities.append({"pair": (a, b), "similarity": sim})
    debug["similarities"] = similarities

    global DUPS_THRESHOLD
    prev_threshold = DUPS_THRESHOLD
    DUPS_THRESHOLD = threshold
    duplicates = _find_duplicates(func_map)
    DUPS_THRESHOLD = prev_threshold
    debug["duplicates"] = duplicates

    if debug is None:
        refactor_logger.error("debug_dict was not generated")

    refactor_logger.debug("debug_dict", debug)
    return debug


# ===================================================================
