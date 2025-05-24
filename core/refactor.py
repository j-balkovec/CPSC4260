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

    def __init__(self, duplicates, functions_map):
        """_summary_

        Args:
            duplicates (_type_): list of tuples containing function names and their Jaccard
                                 similarity
            functions_map (_type_): dictionary mapping function names to their AST nodes
        """
        super().__init__()
        self.dup_funcs = {f for f1, f2, _ in duplicates for f in (f1, f2)}

        key = duplicates[0][0]
        if key not in functions_map:
            raise ValueError(f"Duplicate refers to unknown function: {key}")

        func_node = functions_map[key]
        sample = func_node.body
        self.helper = _make_helper_node(
            func_name=key, args=[arg.arg for arg in func_node.args.args], body=sample
        )
        refactor_logger.debug(f"Helper function created: {self.helper.name}")
        refactor_logger.debug(f"dups: {self.dup_funcs}")

    def visit_Module(self, node: ast.Module):
        """_summary_
                * Module Level
        Args:
            node (ast.Module): node to be transformed

        Returns:
            _type_: transformed node
        """
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


def _refactor_with_ast(source_code: str, duplicates: list) -> str:
    """_summary_

    Args:
        source_code (str): source code to be refactored
        duplicates (list): list of tuples containing function names and their Jaccard similarity

    Returns:
        str: refactored source code
    """
    tree = ast.parse(source_code)

    func_map = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    transformer = DuplicateRefactorer(duplicates, func_map)

    new_tree = transformer.visit(tree)
    ast.fix_missing_locations(new_tree)

    return ast.unparse(new_tree)


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
def refactor_duplicates(filepath) -> Tuple[str, bool]:
    """_summary_

    Args:
        filepath (_type_): filepath to be processed

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
        return ("# No duplicates found, nothing to refactor.", False)

    return (_refactor_with_ast(source_code, duplicates), True)


# ===================================================================
# >
# >
# >
# ============================== DEBUG ==============================
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
