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
from typing import Optional, List, Tuple

from utils.utility import _read_file_contents
from core.constants import TEST_PATHS

# ==== UNITS TO BE TESTED ====
from core.refactor import _refactor_with_ast
from core.method_length import _find_long_method
from core.param_length import _find_long_parameter_list
from core.duplicated_finder import _find_duplicated_code
# ==== UNITS TO BE TESTED ====

def generate_ids(test_list: list):
    """_summary_

    Args:
        test_list (list): list of test cases

    Returns:
        ids (list): the list of ids for the test cases
    """
    ids = []
    for i, (source_code, _) in enumerate(test_list, start=1):
        try:
            tree = ast.parse(source_code)
            func_names = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
            label = "_".join(func_names[:2]) if func_names else "no_functions"
            label = f"num_{i}_{label}"
        except:
            label = "unknown_case"
        ids.append(label)
    return ids      


# =============================================== LONG METHOD =================================================
LONG_METHOD = [
    (_read_file_contents(TEST_PATHS['1']), True),
    (_read_file_contents(TEST_PATHS['2']), True),
    (_read_file_contents(TEST_PATHS['3']), False),
    (_read_file_contents(TEST_PATHS['4']), True),
    (_read_file_contents(TEST_PATHS['5']), False),
    (_read_file_contents(TEST_PATHS['6']), False),
    (_read_file_contents(TEST_PATHS['7']), True),
    (_read_file_contents(TEST_PATHS['8']), False),
    (_read_file_contents(TEST_PATHS['9']), True),
    (_read_file_contents(TEST_PATHS['10']), False),
]

@pytest.mark.long_method
@pytest.mark.parametrize(
    "source_code, expected_non_empty",
    LONG_METHOD,
    ids=generate_ids(LONG_METHOD)
)
def test_find_long_method(source_code: str, expected_non_empty: bool):
    result = _find_long_method(source_code)
    
    assert isinstance(result, list), f"Expected result to be a list but got {type(result)}"
    
    if expected_non_empty:
        assert len(result) > 0, f"Expected at least one long method, but found none.\nSource:\n{source_code}"
        for item in result:
            assert "function" in item and "length" in item, "Missing expected keys in result dict"
            assert item["length"] > item["threshold"], "Reported method is not actually over threshold"
    else:
        assert len(result) == 0, "Expected no long methods, but some were found"

# =============================================================================================================



# =============================================== LONG PARAMS =================================================
LONG_PARAM = [
    (_read_file_contents(TEST_PATHS['11']), True),
    (_read_file_contents(TEST_PATHS['12']), False),
    (_read_file_contents(TEST_PATHS['13']), True),
    (_read_file_contents(TEST_PATHS['14']), True),
    (_read_file_contents(TEST_PATHS['15']), True),
    (_read_file_contents(TEST_PATHS['16']), True),
    (_read_file_contents(TEST_PATHS['17']), False),
    (_read_file_contents(TEST_PATHS['18']), True),
    (_read_file_contents(TEST_PATHS['19']), True),
    (_read_file_contents(TEST_PATHS['20']), True),
]

@pytest.mark.long_param
@pytest.mark.parametrize(
    "source_code, expected_non_empty",
    LONG_PARAM,
    ids=generate_ids(LONG_PARAM)
)
def test_find_long_parameter_list(source_code: str, expected_non_empty: bool):
    result = _find_long_parameter_list(source_code)
    
    assert isinstance(result, list), f"Expected result to be a list but got {type(result)}"
    
    if expected_non_empty:
        assert len(result) > 0, "Expected one or more long parameter list functions, but found none"
        for entry in result:
            assert "function" in entry and "params_count" in entry and "threshold" in entry, \
                f"Result missing required keys: {entry}"
            assert entry["params_count"] > entry["threshold"], \
                f"Reported function has {entry['params_count']} parameters but threshold is {entry['threshold']}"
    else:
        assert len(result) == 0, "Expected no long parameter list functions, but some were found"

# =============================================================================================================



# =================================================== DUPS ====================================================
DUPLICATES = [
    (_read_file_contents(TEST_PATHS['21']), True),
    (_read_file_contents(TEST_PATHS['22']), True),
    (_read_file_contents(TEST_PATHS['23']), True),
    (_read_file_contents(TEST_PATHS['24']), True),
    (_read_file_contents(TEST_PATHS['25']), False),
    (_read_file_contents(TEST_PATHS['26']), True),
    (_read_file_contents(TEST_PATHS['27']), False),
    (_read_file_contents(TEST_PATHS['28']), False),
    (_read_file_contents(TEST_PATHS['29']), True),
    (_read_file_contents(TEST_PATHS['30']), False),
]

@pytest.mark.duplicated_code
@pytest.mark.parametrize(
    "source_code, expected_non_empty",
    DUPLICATES,
    ids=generate_ids(DUPLICATES)
)
def test_find_duplicated_code(source_code: str, expected_non_empty: bool):
    result = _find_duplicated_code(source_code)
    
    assert isinstance(result, list), f"Expected list from _find_duplicated_code but got {type(result)}"
    
    if expected_non_empty:
        assert len(result) > 0, "Expected duplicated code blocks to be found, but got none"
        
        for dup in result:
            assert "block1" in dup and "block2" in dup and "similarity" in dup, "Missing required keys in result item"
            assert isinstance(dup["similarity"], float), "Similarity should be a float"
            assert dup["similarity"] >= dup["threshold"], "Similarity below threshold"

            for block_key in ("block1", "block2"):
                block = dup[block_key]
                for required_field in ("text", "tokens", "line_number"):
                    assert required_field in block, f"Missing field '{required_field}' in {block_key}"
                assert isinstance(block["tokens"], list), f"{block_key}.tokens must be a list"

    else:
        assert len(result) == 0, "Expected no duplicated code blocks, but some were found"

# =============================================================================================================



# =============================================== REFACTORING =================================================
REFACTOR = [
    (_read_file_contents(TEST_PATHS['31']), True),
    (_read_file_contents(TEST_PATHS['32']), True),
    (_read_file_contents(TEST_PATHS['33']), True),
    (_read_file_contents(TEST_PATHS['34']), True),
    (_read_file_contents(TEST_PATHS['35']), True),
    (_read_file_contents(TEST_PATHS['36']), True),
    (_read_file_contents(TEST_PATHS['37']), True),
    (_read_file_contents(TEST_PATHS['38']), True),
    (_read_file_contents(TEST_PATHS['39']), True),
    (_read_file_contents(TEST_PATHS['40']), True),
]

def is_helper_generated(refactored_code: str) -> bool:
    """_summary_

    Args:
        refactored_code (str): The refactored code to check for helper function generation.

    Returns:
        bool: True if a helper function was generated, False otherwise.
    """
    return any("_common_logic_" in line for line in refactored_code.splitlines())

@pytest.mark.refactor
@pytest.mark.parametrize(
    "source_code, expect_helper",
    REFACTOR,
    ids=generate_ids(REFACTOR),
)
def test_refactor_cases(source_code: str, expect_helper: bool):
    """_summary_

    Args:
        source_code (str): The source code to be tested.
        expect_helper (bool): Flag indicating whether a helper function is expected to be generated.
    """
    try:
        tree = ast.parse(source_code)
        functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
        func_names = [func.name for func in functions]

        if len(functions) < 2:
            pytest.fail(f"Test case requires at least two functions to compare. Found: {func_names} in:\n{source_code}")

        duplicates = [(func_names[0], func_names[1], 1.0)]
        refactored = _refactor_with_ast(source_code, duplicates)
        helper_found = is_helper_generated(refactored)
        assert helper_found == expect_helper, f"Expected helper to be {expect_helper}, but got {helper_found} in:\n{refactored}"

    except Exception as e:
        if expect_helper:
            pytest.fail(f"Test case expected helper function but refactoring failed: {e}\nSource Code:\n{source_code}")
        else:
            pytest.fail(f"Refactoring unexpectedly failed when no helper was expected: {e}\nSource Code:\n{source_code}")
# =============================================================================================================