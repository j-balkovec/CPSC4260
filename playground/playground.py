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

from core.refactor import (_extract_functions, 
                           _find_duplicates,
                           _hash_var,
                           _refactor_duplicates,
                           _debug_dict)

from core.constants import TEST_PATHS
from utils.utility import (_read_file_contents, 
                           _pretty_print,
                           _pretty_print_debug_dict)

# name1 = "baz"
# name2 = "bar"
# name3 = "foo"

# print(_hash_var(name1))
# print(_hash_var(name2))
# print(_hash_var(name3))

code = _read_file_contents(TEST_PATHS['9'])
functions_dict = _extract_functions(code)
dups = _find_duplicates(functions_dict)
debug = _debug_dict(code)

# _pretty_print(functions_dict)
# print(dups)
# _pretty_print_debug_dict(debug)

refactored_string = _refactor_duplicates(source_code=code, duplicates=dups)

print(refactored_string)

