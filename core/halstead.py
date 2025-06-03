# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sun Apr 20th, 2025
#
# __file__: halstead_metrics.py
#
# __brief__: This file contains the logic used to calculate the Halstead metrics

import os
# =========
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# =========

import re
import math
import keyword

from core.constants import ALLOWED_OPERATORS
from utils.exceptions import CodeProcessingError
from utils.logger import setup_logger
from utils.utility import _read_file_contents

# ==========
halstead_metrics_logger = setup_logger(
    name="halstead_metrics.py_logger", log_file="halstead_metrics.log"
)
# ==========

halstead_metrics_logger.info("halstead_metrics_logger")


def _extract_operators_and_operands(source_code: str) -> dict:
    """_summary_

    Args:
        source_code (str): A long string with all the lines of code.

    Returns:
        dict: A dictionary with the following keys:
            * unique_operators -> set
            * unique_operands  -> set
            * total_operators  -> list
            * total_operands   -> list
    """
    halstead_metrics_logger.info(
        "[_extract_operators_and_operands] starting extraction"
    )

    grouped = {
        "unique_operators": set(),
        "unique_operands": set(),
        "total_operators": [],
        "total_operands": [],
    }

    inside_multiline_comment = False

    fstring_pattern = r'f"[^"]*"|f\'[^\']*\''
    multi_operators_pattern = r"(==|!=|<=|>=|&&|\|\|)"

    for line in source_code.splitlines():
        stripped_line = line.strip()

        if stripped_line == "":
            continue

        if stripped_line.startswith(('"""', "'''")):
            inside_multiline_comment = not inside_multiline_comment
            continue

        if inside_multiline_comment:
            continue

        line = re.sub(fstring_pattern, "", line)
        line = re.sub(
            r'"""([^"]|"(?!""))+"""|\'\'\'([^\']|\'(?!\'\'))+\'\'\'', "", line
        )

        code_part = re.sub(r"\s*#.*$", "", line).strip()

        if code_part.strip():
            multi_ops = re.findall(multi_operators_pattern, code_part)
            for op in multi_ops:
                grouped["total_operators"].append(op)
                grouped["unique_operators"].add(op)

            for char in code_part:
                if char in ALLOWED_OPERATORS:
                    grouped["total_operators"].append(char)
                    grouped["unique_operators"].add(char)

            tokens = re.findall(r"\b\w+\b", code_part)

            for token in tokens:
                if token in keyword.kwlist or token.isdigit():
                    continue
                grouped["total_operands"].append(token)
                grouped["unique_operands"].add(token)

        else:
            # raise CodeProcessingError(
            #     "Failed to parse the code",
            #     function="_extract_operators_and_operands",
            #     source_code=source_code
            # )
            continue

    # sanity check
    if not grouped["total_operators"] and not grouped["total_operands"]:
        raise CodeProcessingError(
            "No valid code content found for Halstead metrics.",
            function="_extract_operators_and_operands",
            source_code=source_code,
        )

    halstead_metrics_logger.info(
        "[_extract_operators_and_operands] Finished extraction. Operators: %d, Operands: %d",
        len(grouped["total_operators"]),
        len(grouped["total_operands"]),
    )
    return grouped


def _calculate_halstead_metrics(info_dict: dict) -> dict:
    """_summary_

    Args:
        info_dict (dict): dictionary returned from group_lines()
                          with all the necessary parameters

    Returns:
        dict: dictionary with halstead metrics

    Formulas:
        Length (N) = N1 + N2
        Vocabulary (n) = n1 + n2
        Volume (V) = N * log2(n)
        Difficulty (D) = (n1/2) * (N2/n2)
        Program Length (HN) = n1 * log2(n1) + n2 * log2(n2)
        Effort (E) = D * V
        Time (T) = E / 18
        Bugs (B) = E / 3000
        Maintainability (M) = 171 - 5.2 * log2(V) - 0.23 * D - 16.2 * log2(N)
    """

    halstead_metrics_logger.info("[_calculate_halstead_metrics] starting calculation")

    halstead_metrics = {
        "n1": len(info_dict["unique_operators"]),
        "n2": len(info_dict["unique_operands"]),
        "N1": len(info_dict["total_operators"]),
        "N2": len(info_dict["total_operands"]),
        "N": 0,
        "n": 0,
        "V": 0,
        "D": 0,
        "HN": 0,
        "E": 0,
        "T": 0,
        "B": 0,
        "M": 0,
    }

    n1 = halstead_metrics["n1"]
    n2 = halstead_metrics["n2"]
    N1 = halstead_metrics["N1"]
    N2 = halstead_metrics["N2"]

    length = N1 + N2
    vocabulary = n1 + n2
    volume = length * math.log2(vocabulary) if vocabulary > 0 else 0
    difficulty = (n1 / 2) * (N2 / n2) if n2 > 0 else 0
    program_length = n1 * math.log2(n1) + n2 * math.log2(n2) if n1 > 0 and n2 > 0 else 0
    effort = difficulty * volume
    time = effort / 18
    bugs = effort / 3000
    maintainability = (
        171 - 5.2 * math.log2(volume) - 0.23 * difficulty - 16.2 * math.log2(length)
        if length > 0 and volume > 0
        else 0
    )

    halstead_metrics["N"] = length
    halstead_metrics["n"] = vocabulary
    halstead_metrics["V"] = round(volume, ndigits=3)
    halstead_metrics["D"] = round(difficulty, ndigits=3)
    halstead_metrics["HN"] = round(program_length, ndigits=3)
    halstead_metrics["E"] = round(effort, ndigits=3)
    halstead_metrics["T"] = round(time, ndigits=3)
    halstead_metrics["B"] = round(bugs, ndigits=3)
    halstead_metrics["M"] = round(maintainability, ndigits=3)

    halstead_metrics_logger.info(
        "[_calculate_halstead_metrics] Completed. Volume: %.3f, Difficulty: %.3f, Effort: %.3f",
        halstead_metrics["V"],
        halstead_metrics["D"],
        halstead_metrics["E"],
    )
    return halstead_metrics


def fetch_halstead_metrics(file_name: str) -> dict:
    """_summary_

    Note:
        Abstract the details from the client

    Args:
        file_name (str): _description_

    Returns:
        _type_: @see _calculate_halstead_metrics()
    """
    raw_code = _read_file_contents(file_name)
    lines = _extract_operators_and_operands(raw_code)
    halstead_metrics = _calculate_halstead_metrics(lines)

    return halstead_metrics
