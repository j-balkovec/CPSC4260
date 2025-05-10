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

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# =========

import json

from core.refactor import (_debug_dict,
                           refactor_duplicates)

from core.constants import TEST_PATHS
from utils.utility import (_read_file_contents, 
                           _pretty_print,
                           _pretty_print_debug_dict)


new_code = refactor_duplicates(TEST_PATHS['12'])
print(new_code)



