# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sun Apr 20th, 2025
# __file__: playground.py
# __brief__: used for testing/debugging purposes, think of it as, well a PLAYGROUND or a SANDBOX


# =======================================================================
# ==== I'M GONNA DURK MY SCHMURK IF THIS SHIT DOES NOT START WORKING ====
# =======================================================================

# =========
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# =========

import json

from core.refactor import _debug_dict, refactor_duplicates

from core.constants import TEST_PATHS
from utils.utility import _read_file_contents, _pretty_print, _pretty_print_debug_dict

from core.method_length import _find_long_method
from core.param_length import _find_long_parameter_list
from core.duplicated_finder import _find_duplicated_code
from core.code_smells import find_code_smells
from core.halstead import fetch_halstead_metrics
from core.refactor import _extract_functions
from core.code_metrics import fetch_code_metrics


source_code = _read_file_contents("../tests/test5.py")

print(source_code)

funcs = _extract_functions(source_code)

print()
print("Type:\t", type(funcs))
print("Length:\t", len(funcs))
print("Contents:\n", funcs)

for func_name, func_data in funcs.items():
    print("Function name:", func_data["name"])
