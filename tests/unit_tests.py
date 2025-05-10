# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sun Apr 20th, 2025
# __file__: unit_tests.py
# __brief__: Script that tests units one by one, nothing too crazy, just making sure my software behaves as it's supposed to behave


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
            
    


EXAMPLES2 = get_test_files()


EXAMPLES = [
    # 1. Return vs void function
    ("""
def foo(x):
    print(x)

def bar(x):
    print(x)
""", True),

    ("""
def foo(a, b):
    return a + b

def bar(x, y):
    return x + y
""", True),

    # 2. Different arg names, same logic
    ("""
def add1(a, b):
    return a + b

def add2(x, y):
    return x + y
""", True),

    # 3. Formatting
    ("""
def foo(a, b):
    return a + b

def bar(a, b):

    # comment
    return a + b
""", True),

    # 4. Early return
    ("""
def check(x):
    if x < 0:
        return False
    return True

def validate(y):
    if y < 0:
        return False
    return True
""", True),

    # 5. Control flow variation (still similar)
    ("""
def f1(a):
    if a > 10:
        return 'big'
    else:
        return 'small'

def f2(x):
    if x > 10:
        return 'big'
    return 'small'
""", True),

    # 6. Functions with side effects
    ("""
def side1():
    print("hi")

def side2():
    print("hi")
""", True),

    # 7. Default args
    ("""
def f1(x=1):
    return x * 2

def f2(x=1):
    return x * 2
""", True),

    # 8. Non-duplicates
    ("""
def f1():
    return 1

def f2():
    return 2
""", False),

    # 9. Nested functions (should skip)
    ("""
def outer():
    def inner():
        return 5
    return inner()

def outer2():
    def inner():
        return 5
    return inner()
""", False)
]

def is_helper_generated(refactored_code: str) -> bool:
    return any("_common_logic_" in line for line in refactored_code.splitlines())

@pytest.mark.parametrize("source_code, expect_helper", EXAMPLES2)
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