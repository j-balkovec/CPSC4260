# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sun Apr 20th, 2025
#
# __file__: refactor_duplicates.py
#
# __brief__: Script to refactor duplicated code by extracting common blocks into functions
#            and replacing duplicates with function calls.

# =========
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# =========

import re
import keyword
import hashlib
from typing import List, Dict, Set, Tuple

from utils.logger import setup_logger
from utils.exceptions import CodeProcessingError

# Logger setup
refactor_logger = setup_logger(name="refactor_duplicates.py_logger", log_file="refactor_duplicates.log")

def _generate_function_name(block: str) -> str:
    """_summary_

    Args:
        block (str): The code block text.

    Returns:
        str: Unique function name (e.g., 'refactored_<hash>').
    """
    hash_object = hashlib.md5(block.encode())
    return f"refactored_{hash_object.hexdigest()[:8]}"

def _extract_variables(block: str) -> Set[str]:
    """_summary_

    Args:
        block (str): The code block text.

    Returns:
        Set[str]: Set of variable names.
    """
    variables = set()
    raw_tokens = re.findall(r'\w+|[+\-*/=<>!&|%^~]+|[()\[\]{},;.:]', block)
    for tok in raw_tokens:
        if (re.fullmatch(r'[a-zA-Z_]\w*', tok) and
                not keyword.iskeyword(tok) and
                tok not in {'True', 'False', 'None', 'large', 'small'}):
            variables.add(tok)
    return variables

def _create_function(block: str, variables: Set[str], func_name: str) -> str:
    """_summary_

    Args:
        block (str): The code block to convert into a function.
        variables (Set[str]): Variables to be parameterized.
        func_name (str): Name of the new function.

    Returns:
        str: Function definition as a string.
    """
    params = ", ".join(sorted(variables)) if variables else ""
    lines = block.splitlines()
    indented_block = "\n".join("    " + line for line in lines)
    func_def = f"def {func_name}({params}):\n{indented_block}\n"
    return func_def

def _replace_block_with_call(block: str, func_name: str, variables: Set[str], line_number: int, source_lines: List[str]) -> Tuple[List[str], int]:
    """_summary_

    Args:
        block (str): The original block text.
        func_name (str): Name of the function to call.
        variables (Set[str]): Variables to pass as arguments.
        line_number (int): Starting line number of the block (1-based).
        source_lines (List[str]): List of source code lines.

    Returns:
        Tuple[List[str], int]: Updated source lines and number of lines replaced.
    """
    block_lines = block.splitlines()
    block_line_count = len(block_lines)
    indent = len(block_lines[0]) - len(block_lines[0].lstrip()) if block_lines else 0
    
    input_vars = [v for v in variables if v in {'x', 'y', 'a', 'b'}]
    internal_vars = [v for v in variables if v not in {'x', 'y', 'a', 'b'}]
    args = ", ".join(input_vars + [f"{v}=None" for v in internal_vars]) if variables else ""
    func_call = " " * indent + f"return {func_name}({args})" if block.strip().endswith("return") else " " * indent + f"{func_name}({args})"
    
    if line_number - 1 + block_line_count > len(source_lines):
        refactor_logger.warning(f"[skip] Invalid line number {line_number} for block replacement, skipping.")
        return source_lines, 0
    
    source_block = "\n".join(source_lines[line_number - 1:line_number - 1 + block_line_count]).strip()
    if '\n'.join(line.strip() for line in source_block.splitlines()) != '\n'.join(line.strip() for line in block.strip().splitlines()):
        refactor_logger.warning(f"[skip] Token mismatch at line {line_number}, skipping.")
        return source_lines, 0
    
    source_lines[line_number - 1:line_number - 1 + block_line_count] = [func_call]
    return source_lines, block_line_count

def _find_function_scope(line_number: int, source_lines: List[str]) -> Tuple[int, int]:
    """_summary_

    Args:
        line_number (int): Starting line number of the block (1-based).
        source_lines (List[str]): List of source code lines.

    Returns:
        Tuple[int, int]: (start_line, indent_level) of the function scope, or (0, 0) if module-level.
    """
    for i in range(line_number - 1, -1, -1):
        line = source_lines[i]
        stripped = line.strip()
        if not stripped:
            continue
        indent = len(line) - len(line.lstrip())
        if stripped.startswith('def ') and indent == 0:  # Only module-level funcs
            return i + 1, indent + 4
    return 0, 0  # Module-level

def _is_valid_block(block: str) -> bool:
    """_summary_

    Args:
        block (str): block of code

    Returns:
        bool: True if VALID, False if INVALID
    """
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    if not lines:
        return False

    first_line = lines[0]

    if first_line.startswith(('else:', 'except', 'finally:')):
        return False

    has_if = any(line.startswith('if ') for line in lines)
    has_else = any(line.startswith('else:') for line in lines)
    has_return = any(line.startswith('return') for line in lines)

    if has_if and has_return and not (lines[0].startswith('return') and all(not l.startswith('if ') for l in lines[1:])):
        return False

    if any(line in {'return', 'pass', 'break', 'continue'} for line in lines):
        return False

    has_statement = any('=' in line or line.startswith(('return ', 'raise ', 'yield ')) for line in lines)
    return has_statement


def refactor_duplicates(source_code: str, duplicates: List[Dict]) -> str:
    """Refactor duplicated code by extracting common blocks into functions and replacing duplicates.

    Args:
        source_code (str): Original source code.
        duplicates (List[Dict]): List of duplicate dictionaries from _find_duplicated_code.

    Returns:
        str: Refactored source code as a string.
    """
    refactor_logger.info("[starting] refactor_duplicates()")
    
    if not duplicates:
        refactor_logger.info("[no duplicates] No refactoring needed.")
        return source_code

    source_lines = source_code.splitlines()
    new_functions = []
    line_adjustments = {}

    for idx, dup in enumerate(duplicates):
        block1 = dup['block1']['text']
        block2 = dup['block2']['text']
        line1 = dup['block1']['line_number']
        line2 = dup['block2']['line_number']

        # ====== validate ======
        if block1 != block2:
            refactor_logger.warning(f"[skip] Blocks at lines {line1} and {line2} are not identical, skipping.")
            continue
        if not _is_valid_block(block1):
            refactor_logger.warning(f"[skip] Block at lines {line1} and {line2} is not a valid logical block:\n{block1}\nskipping.")
            continue

        # ====== extract vars ======
        variables = _extract_variables(block1)
        refactor_logger.debug(f"[variables] Found variables: {variables}")

        # ====== gen func ======
        func_name = _generate_function_name(block1)
        func_def = _create_function(block1, variables, func_name)
        
        # ====== find scope ======
        scope_line1, indent1 = _find_function_scope(line1, source_lines)
        scope_line2, indent2 = _find_function_scope(line2, source_lines)
        
        if scope_line1 == scope_line2 and scope_line1 != 0:
            insert_line = scope_line1
            indent = indent1
            placement = f"inside function at line {insert_line}"
        else:
            insert_line = len(source_lines) + 1
            indent = 0
            placement = "module level"
        
        new_functions.append((func_def, insert_line, indent))
        refactor_logger.info(f"[generated] Function {func_name} for duplicate at lines {line1} and {line2}, placed at {placement}")

        # ====== replace blocks ======
        adjusted_line1 = line1 - sum(adj for ln, adj in line_adjustments.items() if ln < line1)
        source_lines, lines_replaced1 = _replace_block_with_call(block1, func_name, variables, adjusted_line1, source_lines)
        if lines_replaced1 == 0:
            continue
        line_adjustments[line1] = lines_replaced1 - 1

        adjusted_line2 = line2 - sum(adj for ln, adj in line_adjustments.items() if ln < line2)
        source_lines, lines_replaced2 = _replace_block_with_call(block2, func_name, variables, adjusted_line2, source_lines)
        if lines_replaced2 == 0:
            continue
        line_adjustments[line2] = lines_replaced2 - 1

    # ====== insert new func ======
    new_functions.sort(key=lambda x: (x[1], x[2]))
    refactored_lines = source_lines[:]
    offset = 0
    for func_def, insert_line, indent in new_functions:
        func_lines = func_def.splitlines()
        indented_func = [" " * indent + line for line in func_lines]
        insert_pos = min(insert_line - 1 + offset, len(refactored_lines))
        refactored_lines[insert_pos:insert_pos] = indented_func + [""]  # Add blank line
        offset += len(indented_func) + 1

    refactored_code = "\n".join(refactored_lines).rstrip() + "\n"
    refactor_logger.info(f"[done] Refactored {len([d for d in duplicates if d['block1']['text'] == d['block2']['text']])} duplicate pairs.")
    return refactored_code