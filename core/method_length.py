# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sun Apr 20th, 2025
#
# __file__: long_method.py
#
# __brief__: This file contains all the logic used for finding long methods in a given source code file.

# =========
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# =========

import re

from core.constants import LENGTH_THRESHOLD
from utils.logger import setup_logger

# ==========
long_method_logger = setup_logger(
    name="long_method.py_logger", log_file="long_method.log"
)
# ==========

long_method_logger.info("long_method_logger")


def _find_long_method(source_code: str) -> list:
    """_summary_

    Args:
        source_code (str): code returned form "_read_file_contents()"

    Returns:
        list: list of all instances where a method is longer than <LENGTH_THRESHOLD>
    """
    long_methods = []
    lines = source_code.split("\n")

    in_function = False
    start_line = 0
    function_indent = 0
    function_name = ""

    for idx, line in enumerate(lines):
        stripped = line.strip()

        if re.match(r"(async\s+)?def\s+\w+", stripped):
            if in_function:
                end_line = idx - 1
                method_length = end_line - start_line + 1
                if method_length > LENGTH_THRESHOLD:
                    long_methods.append(
                        {
                            "function": function_name,
                            "start_line": start_line + 1,
                            "end_line": end_line + 1,
                            "length": method_length,
                            "threshold": LENGTH_THRESHOLD,
                        }
                    )
            in_function = True
            start_line = idx
            function_indent = len(line) - len(line.lstrip())
            match = re.match(r"(async\s+)?def\s+(\w+)", stripped)
            if match:
                function_name = match.group(2)
            continue

        if in_function:
            current_indent = len(line) - len(line.lstrip())

            if current_indent < function_indent and stripped:
                end_line = idx - 1
                method_length = end_line - start_line + 1
                if method_length > LENGTH_THRESHOLD:
                    long_methods.append(
                        {
                            "function": function_name,
                            "start_line": start_line + 1,
                            "end_line": end_line + 1,
                            "length": method_length,
                            "threshold": LENGTH_THRESHOLD,
                        }
                    )
                in_function = False
                function_name = ""

    if in_function:
        end_line = len(lines) - 1
        method_length = end_line - start_line + 1
        if method_length > LENGTH_THRESHOLD:
            long_methods.append(
                {
                    "function": function_name,
                    "start_line": start_line + 1,
                    "end_line": end_line + 1,
                    "length": method_length,
                    "threshold": LENGTH_THRESHOLD,
                }
            )

    long_method_logger.info(f"Found {len(long_methods)} long methods.")
    for method in long_methods:
        long_method_logger.info(
            f"Method '{method['function']}' from line {method['start_line']} to {method['end_line']} is {method['length']} lines long (threshold: {method['threshold']})."
        )

    return long_methods
