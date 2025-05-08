# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sun Apr 20th, 2025
#
# __file__: code_smells.py
#
# __brief__: TODO

# =========
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# =========

from utils.logger import setup_logger
from utils.utility import (_read_file_contents, 
                      _save_to_json, 
                      _generate_readable_report)

from core.duplicated_finder import _find_duplicated_code
from core.method_length import _find_long_method
from core.param_length import _find_long_parameter_list


# ==========
code_smells_logger = setup_logger(name="code_smells.py_logger", log_file="code_smells.log")
# ==========

code_smells_logger.info("code_smells_logger")

def find_code_smells(file_name: str) -> dict:
    """_summary_

    Raises:
        TypeError: _description_

    Returns:
        dict: _description_
    """
    source_code = _read_file_contents(file_name)
    
    if source_code is not None:
        code_smells_logger.info(f"read file: {file_name}, got {len(source_code)} lines")
        
    else:
        code_smells_logger.error(f"could not read file: {file_name}")
        raise TypeError(f"could not read file: {file_name}")
    
    code_smells = {
        "long_parameter_list": [],
        "long_method": [],
        "duplicated_code": [],
    }
    
    code_smells["long_parameter_list"] = _find_long_parameter_list(source_code)
    code_smells["long_method"] = _find_long_method(source_code)
    code_smells["duplicated_code"] = _find_duplicated_code(source_code)
    
    
    raw_json = _save_to_json(code_smells, file_name)
    _generate_readable_report(raw_json)
    
    code_smells_logger.info(f"found code smells: {code_smells}")
    code_smells_logger.info(f"json ready: {raw_json}")
    
    return code_smells