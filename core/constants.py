# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sun Apr 20th, 2025
#
# __file__: constants.py
#
# __brief__: This file holds all the constants used in the project in one place, avoiding shotgun surgery

# =========
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# =========

# Add guide on how to resolve errors
ERROR_CODES: dict = {
    "file_read": 1001,
    "corrupt_file": 1002,
    "file_not_found": 1003,
    "file_empty": 1004,
    "file_type_unsupported": 1005,
    "file_decode_error": 1006,
    "file_locked": 1007,
    "file_too_large": 1008,
    "file_open_error": 1009,
}

YELLOW_TEXT: str = "\033[33m"
RESET_TEXT: str = "\033[0m"
RED_TEXT: str = "\033[31m"

SIZE_LIMIT: int = 10 * 1024 * 1024  # 10 MB

# Could cause issues
ALLOWED_OPERATORS = {
    "+",
    "-",
    "*",
    "**",
    "*=",
    "**=",
    "/",
    "//",
    "/=",
    "//=",
    "%",
    "%=",
    "=",
    "==",
    "!=",
    ":=",
    "<",
    ">",
    "<=",
    ">=",
    "&",
    "&=",
    "|",
    "|=",
    "^",
    "^=",
    "~",
    "<<",
    "<<=",
    ">>",
    ">>=",
    "->",
    "@",
    "@=",
}

PARAMS_THRESHOLD: int = 3
LENGTH_THRESHOLD: int = 15
DUPS_THRESHOLD: float = 0.76  # 0.75

LOG_COLORS = {
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "bold_red",
}

JSON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/json/"))

# Set to false when being graded
i_am_local = False

TEST_PATHS = {
    "1": os.path.abspath(os.path.join(os.path.dirname(__file__), "../tests/test1.py")),
    "2": os.path.abspath(os.path.join(os.path.dirname(__file__), "../tests/test2.py")),
    "3": os.path.abspath(os.path.join(os.path.dirname(__file__), "../tests/test3.py")),
    "4": os.path.abspath(os.path.join(os.path.dirname(__file__), "../tests/test4.py")),
    "5": os.path.abspath(os.path.join(os.path.dirname(__file__), "../tests/test5.py")),
    "6": os.path.abspath(os.path.join(os.path.dirname(__file__), "../tests/test6.py")),
    "7": os.path.abspath(os.path.join(os.path.dirname(__file__), "../tests/test7.py")),
    "8": os.path.abspath(os.path.join(os.path.dirname(__file__), "../tests/test8.py")),
    "9": os.path.abspath(os.path.join(os.path.dirname(__file__), "../tests/test9.py")),
    "10": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test10.py")
    ),
    "11": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test11.py")
    ),
    "12": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test12.py")
    ),
    "13": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test13.py")
    ),
    "14": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test14.py")
    ),
    "15": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test15.py")
    ),
    "16": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test16.py")
    ),
    "17": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test17.py")
    ),
    "18": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test18.py")
    ),
    "19": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test19.py")
    ),
    "20": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test20.py")
    ),
    "21": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test21.py")
    ),
    "22": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test22.py")
    ),
    "23": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test23.py")
    ),
    "24": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test24.py")
    ),
    "25": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test25.py")
    ),
    "26": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test26.py")
    ),
    "27": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test27.py")
    ),
    "28": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test28.py")
    ),
    "29": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test29.py")
    ),
    "30": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test30.py")
    ),
    "31": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test31.py")
    ),
    "32": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test32.py")
    ),
    "33": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test33.py")
    ),
    "34": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test34.py")
    ),
    "35": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test35.py")
    ),
    "36": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test36.py")
    ),
    "37": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test37.py")
    ),
    "38": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test38.py")
    ),
    "39": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test39.py")
    ),
    "40": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test40.py")
    ),
    "41": (
        r"/Users/jbalkovec/Desktop/CPSC4610/Projects/P2/multiagent/multiAgents.py"
        if i_am_local
        else r"invalid/path/check/constants.py"
    ),
    "42": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test42.java")
    ),
    "43": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test43.py")
    ),
    "44": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test44.py")
    ),
    "9997": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test9997.py")
    ),
    "9998": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test9998.py")
    ),
    "9999": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../tests/test9999.py")
    ),
}
