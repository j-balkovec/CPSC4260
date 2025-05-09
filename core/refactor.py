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
import ast
import hashlib
from typing import List, Dict, Set, Tuple

from utils.logger import setup_logger
from utils.exceptions import CodeProcessingError

from core.duplicated_finder import (_tokenize_block, 
                                    _normalize_block, 
                                    _generate_ngrams, 
                                    _jaccard_similarity,
                                    _remove_comments)

from core.constants import (DUPS_THRESHOLD)

# Logger setup
refactor_logger = setup_logger(name="refactor_duplicates.py_logger", log_file="refactor_duplicates.log")

# tested -> works
def _extract_functions(source_code: str) -> dict:
    functions = {}
    source_code = _remove_comments(source_code)
    tree = ast.parse(source_code)
    lines = source_code.splitlines(keepends=True)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if not hasattr(node, 'end_lineno'):
                start_line = node.lineno - 1
                indent = len(lines[start_line]) - len(lines[start_line].lstrip())
                end_line = start_line + 1
                while end_line < len(lines):
                    line = lines[end_line]
                    if line.strip() and (len(line) - len(line.lstrip()) <= indent) and not line.lstrip().startswith('#'):
                        break
                    end_line += 1
            else:
                start_line = node.lineno - 1
                end_line = node.end_lineno

            start_offset = sum(len(l) for l in lines[:start_line])
            
            end_offset = sum(len(l) for l in lines[:end_line])
            if end_line < len(lines):
                end_offset += len(lines[end_line])
                
            func_text = ''.join(lines[start_line:end_line])
            functions[node.name] = {
                "name": node.name,
                "start": start_offset,
                "end": end_offset,
                "text": func_text
            }

    return functions
# tested -> works
def _find_duplicates(func_map: dict) -> list:
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
    return duplicates

# tested -> works
def _hash_var(name: str, type: str) -> str:
    hash = hashlib.md5(name.encode()).hexdigest()
    
    if type == 'var':
        return "var_" + hash
    
    elif type == 'func':
        return hash
    
    else:
        raise CodeProcessingError(f"invalid type for hashing: {type}. Must be 'var' or 'func'.")
    

def _parse_signature(header: str) -> Tuple[str, str]:
    match = re.match(r'\s*def\s+(\w+)\s*\((.*?)\)\s*:', header)
    if not match:
        raise CodeProcessingError("Invalid function header")
    return match.group(1), match.group(2)


def _refactor_duplicates(source_code: str, duplicates: list, debug = False) -> str:
    functions = _extract_functions(source_code)
    helpers = []
    replacements = []

    for idx, (f1, f2, _) in enumerate(duplicates):
        fn1 = functions[f1]
        fn2 = functions[f2]

        # Get header and args
        header1 = fn1["text"].splitlines()[0]
        _, args = _parse_signature(header1)

        # Get function body (without header)
        body_lines = fn1["text"].splitlines()[1:]
        if not body_lines:
            continue

        # Re-indent body to 1-level inside the helper
        body = "\n".join("  " + line for line in body_lines)
        helper_name = f"_common_logic_{_hash_var(f1, 'func')}"
        helpers.append(f"def {helper_name}({args}):\n{body}\n")

        # Build replacements
        new_def_1 = f"def {fn1['name']}({args}):\n    return {helper_name}({args})\n"
        new_def_2 = f"def {fn2['name']}({args}):\n    return {helper_name}({args})\n"
        replacements.append((fn1["start"], fn1["end"], new_def_1))
        replacements.append((fn2["start"], fn2["end"], new_def_2))
    
    if debug == True:
        for start, end, new_func in sorted(replacements, key=lambda x: x[0], reverse=True):
            old_func = source_code[start:end]
            print("=== OLD FUNC ===")
            print(old_func)
            print("=== NEW FUNC ===")
            print(new_func)
            print("---")
            source_code = source_code[:start] + new_func + source_code[end:]
    
    else:
        for start, end, new_func in sorted(replacements, key=lambda x: x[0], reverse=True):
            source_code = source_code[:start] + new_func + source_code[end:]

    return "\n".join(helpers) + "\n\n" + source_code
    
    
    
    
# ============================== DEBUG ==============================

def _debug_dict(source_code: str, threshold: float = 0.85) -> dict:
    debug = {}

    func_map = _extract_functions(source_code)
    debug["functions"] = {
        name: {
            "start": data["start"],
            "end": data["end"],
            "text": data["text"]
        } for name, data in func_map.items()
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

    refactor_logger.debug("debug_dict", debug)
    return debug

# ===================================================================
