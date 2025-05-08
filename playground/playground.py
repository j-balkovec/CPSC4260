# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sun Apr 20th, 2025
# __file__: refactor_duplicates.py
# __brief__: Refactors duplicated code identified by duplicated_code.py into a reusable function,
#            focusing on a single line of duplicated code to preserve control flow.


# =======================================================================
# ==== I'M GONNA DURK MY SCHMURK IF THIS SHIT DOES NOT START WORKING ====
# =======================================================================

# =========
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# =========


import json
import re
import keyword
import hashlib

from core.duplicated_finder import (
    _normalize_block,
    _split_into_blocks,
    _tokenize_block,
    _remove_comments,
    duplicated_code_logger
)

def generate_unique_func_name(block_text):
    """_summary_
    
    Args:
        block_text (str): Text of the duplicated block.
    
    Returns:
        str: Unique function name.
    """
    hash_val = hashlib.md5(_normalize_block(block_text).encode()).hexdigest()[:8]
    return f"compute_block_{hash_val}"

def identify_variables(block_text):
    """_summary_
    
    Args:
        block_text (str): Text of the duplicated block.
    
    Returns:
        tuple: (input_vars, output_vars) where input_vars are used but not defined,
               and output_vars are defined and returned or used externally.
    """
    lines = _normalize_block(block_text).split("\n")
    defined_vars = set()
    used_vars = set()
    
    for line in lines:
        if line.strip().startswith(("if ", "else:", "elif ", "for ", "while ", "return ")):
            continue
        
        match = re.match(r'^\s*([a-zA-Z_]\w*)\s*=', line.strip())
        if match:
            var = match.group(1)
            if not keyword.iskeyword(var):
                defined_vars.add(var)
        
        tokens = re.findall(r'\b([a-zA-Z_]\w*)\b', line)
        for token in tokens:
            if not keyword.iskeyword(token) and token not in ("True", "False", "None"):
                used_vars.add(token)
    
    input_vars = list(used_vars - defined_vars)
    
    output_vars = []
    last_line = lines[-1].strip()
    if last_line.startswith("return "):
        return_vars = re.findall(r'\b([a-zA-Z_]\w*)\b', last_line[len("return "):])
        output_vars = [v for v in return_vars if v in defined_vars]
    else:
        output_vars = list(defined_vars)
    
    return input_vars, output_vars

def generate_function(block_text, input_vars, output_vars, func_name):
    """_summary_
    
    Args:
        block_text (str): Text of the duplicated block.
        input_vars (list): Input variables to pass as parameters.
        output_vars (list): Output variables to return.
        func_name (str): Name of the generated function.
    
    Returns:
        str: Function definition as a string.
    """
    param_str = ", ".join(input_vars) if input_vars else ""
    
    lines = block_text.split("\n")
    if not lines:
        return ""
    
    first_line = next((line for line in lines if line.strip()), "")
    base_indent = len(first_line) - len(first_line.lstrip()) if first_line else 0
    
    body_lines = []
    for line in lines:
        if line.strip():
            current_indent = len(line) - len(line.lstrip())
            new_indent = max(0, current_indent - base_indent) + 4
            body_lines.append(" " * new_indent + line.lstrip())
    
    body = "\n".join(body_lines)
    
    return_stmt = ""
    if output_vars:
        if len(output_vars) == 1:
            return_stmt = f"    return {output_vars[0]}"
        else:
            return_stmt = f"    return {', '.join(output_vars)}"
    elif not body_lines[-1].strip().startswith("return "):
        for line in reversed(body_lines):
            match = re.match(r'^\s*([a-zA-Z_]\w*)\s*=', line.strip())
            if match:
                return_stmt = f"    return {match.group(1)}"
                break
    
    func_def = f"def {func_name}({param_str}):\n{body}\n{return_stmt}\n" if return_stmt else f"def {func_name}({param_str}):\n{body}\n"
    return func_def

def get_block_context(source_code, line_number, block_text):
    """_summary_
    
    Args:
        source_code (str): Full source code.
        line_number (int): Line number of the duplicated block.
        block_text (str): Text of the duplicated block.
    
    Returns:
        dict: Context including indentation and block text.
    """
    lines = source_code.splitlines()
    norm_block_text = _normalize_block(block_text)
    block_lines = norm_block_text.split("\n")
    
    start_idx = line_number - 1
    if start_idx + len(block_lines) > len(lines):
        duplicated_code_logger.error(f"Block at line {line_number} exceeds source code length")
        raise ValueError(f"Invalid block at line {line_number}")
    
    source_block = "\n".join(lines[start_idx:start_idx + len(block_lines)])
    if _normalize_block(source_block) != norm_block_text:
        duplicated_code_logger.error(f"Block at line {line_number} does not match expected text")
        raise ValueError(f"Block mismatch at line {line_number}")
    
    block_indent = len(lines[start_idx]) - len(lines[start_idx].lstrip()) if lines[start_idx].strip() else 0
    
    return {
        "block_indent": block_indent,
        "block_lines": block_lines
    }

def replace_duplicate(source_code, line_number, block_text, func_name, input_vars, output_vars):
    """_summary_
    
    Args:
        source_code (str): Full source code.
        line_number (int): Line number of the duplicated block.
        block_text (str): Text of the duplicated block.
        func_name (str): Name of the generated function.
        input_vars (list): Input variables to pass to the function.
        output_vars (list): Output variables to assign from the function.
    
    Returns:
        str: Modified source code.
    """
    lines = source_code.splitlines()
    context = get_block_context(source_code, line_number, block_text)
    block_indent = context["block_indent"]
    block_lines = context["block_lines"]
    
    func_call = f"{func_name}({', '.join(input_vars)})" if input_vars else f"{func_name}()"
    indent = " " * block_indent
    
    replacement = ""
    if output_vars:
        if len(output_vars) == 1:
            replacement = f"{indent}{output_vars[0]} = {func_call}"
        else:
            output_str = ", ".join(output_vars)
            replacement = f"{indent}{output_str} = {func_call}"
    else:
        replacement = f"{indent}{func_call}"
    
    norm_block = _normalize_block(block_text)
    if norm_block.split("\n")[-1].strip().startswith("return"):
        replacement = f"{indent}return {func_call}"
    
    start_idx = line_number - 1
    end_idx = start_idx + len(block_lines)
    lines[start_idx:end_idx] = [replacement]
    
    return "\n".join(lines)

def refactor_duplicates(source_code, duplicates_json):
    """_summary_
    
    Args:
        source_code (str): Full source code.
        duplicates_json (list): JSON output from duplicated_code.py.
    
    Returns:
        str: Refactored source code.
    """
    duplicated_code_logger.info("[starting] refactor_duplicates")
    
    modified_code = source_code
    for dup in duplicates_json:
        try:
            block1 = dup["block1"]
            block2 = dup["block2"]
            block_text = block1["text"]
            
            input_vars, output_vars = identify_variables(block_text)
            duplicated_code_logger.info(f"[identified] input_vars: {input_vars}, output_vars: {output_vars}")
            
            func_name = generate_unique_func_name(block_text)
            duplicated_code_logger.info(f"[generated] function name: {func_name}")
            
            func_def = generate_function(block_text, input_vars, output_vars, func_name)
            duplicated_code_logger.info(f"[generated] function:\n{func_def}")
            
            if not func_def.strip():
                duplicated_code_logger.error("Generated function is empty")
                continue
            
            modified_code = func_def + "\n" + modified_code
            
            modified_code = replace_duplicate(
                modified_code,
                block1["line_number"],
                block1["text"],
                func_name,
                input_vars,
                output_vars
            )
            duplicated_code_logger.info(f"[replaced] block at line {block1['line_number']}")
            
            modified_code = replace_duplicate(
                modified_code,
                block2["line_number"],
                block2["text"],
                func_name,
                input_vars,
                output_vars
            )
            duplicated_code_logger.info(f"[replaced] block at line {block2['line_number']}")
            
        except Exception as e:
            duplicated_code_logger.error(f"[error] refactoring duplicate: {str(e)}")
            continue
    
    duplicated_code_logger.info("[done] refactoring complete")
    return modified_code
    
# ========================================== WORKBENCH ===================================================

import json

from utils.utility import _read_file_contents
from core.duplicated_finder import _find_duplicated_code
from core.constants import TEST_PATHS

source_code = _read_file_contents(TEST_PATHS['8'])
duplicates = _find_duplicated_code(source_code)

refactored_code = refactor_duplicates(source_code, duplicates)

print("\n\n=====================================================")
print("Original Duplicates:\n", json.dumps(duplicates, indent=4))
print("\nRefactored Code:\n", refactored_code)
# ========================================================================================================