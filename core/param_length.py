# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sun Apr 20th, 2025
#
# __file__: long_param_list.py
#
# __brief__: This file contains all the logic used for finding methods with long parameter lists in a given source file of code

# =========
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# =========

import re

from core.constants import (PARAMS_THRESHOLD)
from utils.logger import setup_logger


# ==========
long_param_list_logger = setup_logger(name="long_param_list.py_logger", log_file="long_param_list.log")
# ==========

long_param_list_logger.info("long_param_list_logger")

def _find_long_parameter_list(source_code: str) -> list:
    """_summary_

    Args:
        source_code (str): code returned form "_read_file_contents()"

    Returns:
        list: list of all instances where a method has more than <PARAMS_THRESHOLD> parameters
    """
    tokens = re.findall(r'\w+|[()]', source_code)
    long_parameter_methods = []
    
    i = 0
    while i < len(tokens):
        if tokens[i] == "def":
            if i + 1 < len(tokens):
                function_name = tokens[i + 1]
            else:
                function_name = "<NOT FOUND>"
                
            while i < len(tokens) and tokens[i] != "(":
                i += 1
            if i >= len(tokens):
                break  
            
            i += 1
            num_params = 0
            
            while i < len(tokens) and tokens[i] != ")":
                if tokens[i] not in (',',):
                    num_params += 1
                i += 1
            
            if num_params > PARAMS_THRESHOLD:
                found_method = f"Function: \n\tposition: {i}, \n\tname: {function_name}, \n\tparameters: {num_params},\n which exceeds the threshold of {PARAMS_THRESHOLD}"
                long_parameter_methods.append({
                        "function": function_name,
                        "position": i,
                        "params_count": num_params,
                        "threshold": PARAMS_THRESHOLD
                    })
        i += 1
    
    long_param_list_logger.info(f"long_parameter_methods: {long_parameter_methods}")
    return long_parameter_methods