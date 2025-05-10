# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sun Apr 20th, 2025
# __file__: unit_tests.py
# __brief__: Script that tests units one by one, nothing too crazy, just making sure my software behaves as it's supposed to behave

# TO RUN: pytest -vs unit_tests.py

# =========
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# =========

import ast
import pytest

from core.refactor import _refactor_with_ast
from utils.utility import _read_file_contents
from core.constants import TEST_PATHS

# list of tuples
def get_test_files():
    test_cases = []
    for num, path in list((TEST_PATHS.items()))[-10:]: 
        raw_code = _read_file_contents(path)
        test_cases.append((raw_code, True)) #jank
        
    return test_cases

def generate_ids():
    ids = []
    for source_code, _ in DUPS_REFACTOR_EXAMPLES:
        try:
            tree = ast.parse(source_code)
            func_names = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
            label = "_".join(func_names[:2])
        except:
            label = "unknown_case"
        ids.append(label)
    return ids      
    
DUPS_REFACTOR_EXAMPLES = get_test_files()

def is_helper_generated(refactored_code: str) -> bool:
    return any("_common_logic_" in line for line in refactored_code.splitlines())

@pytest.mark.parametrize("source_code, expect_helper", DUPS_REFACTOR_EXAMPLES, ids=generate_ids())
def test_refactor_cases(source_code, expect_helper):
    try:
        tree = ast.parse(source_code)
        func_names = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
        assert len(func_names) >= 2, "Need at least two functions to compare"
        duplicates = [(func_names[0], func_names[1], 1.0)]
        
        refactored = _refactor_with_ast(source_code, duplicates)
        helper_found = is_helper_generated(refactored)
        assert helper_found == expect_helper
    except Exception as e:
        if expect_helper:
            raise AssertionError("Expected helper function but failed") from e