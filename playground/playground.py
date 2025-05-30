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

from core.refactor import _debug_dict

from core.constants import TEST_PATHS
from utils.utility import (_read_file_contents,
                           _pretty_print,
                           _pretty_print_debug_dict,
                           _pretty_print_raw_string_func)

from core.method_length import _find_long_method
from core.param_length import _find_long_parameter_list
from core.duplicated_finder import _find_duplicated_code
from core.code_smells import find_code_smells
from core.halstead import fetch_halstead_metrics
from core.refactor import _extract_functions
from core.code_metrics import fetch_code_metrics
from core.file_saver import save_refactored_file
from core.refactor import refactor_duplicates
from core.trend_analysis import main

from plot.plot_trends import plot_dir_trends
from core.trend_analysis import markdown_fmt

from pathlib import Path

rn = None

test_file = TEST_PATHS["31"]

print(" ===== ORIGINAL1 ===== \n")
original = print(_read_file_contents(test_file))
print("\n" * 2)

# Refactored

refactored_wrapper = refactor_duplicates(test_file, use_wrapper=True)
refactored_no_wrapper = refactor_duplicates(test_file, use_wrapper=False)

print("\n" * 2)

# Print
print("==========" * 5)
print("\n" * 2)

print(" ===== REFACTORED WITH WRAPPER ===== ")
print(refactored_wrapper[0])

print("\n" * 2)

print(" ===== REFACTORED WITHOUT WRAPPER ===== ")
print(refactored_no_wrapper[0])

print("\n" * 2)
