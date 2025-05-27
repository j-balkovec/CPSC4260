# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sun Apr 20th, 2025
# __file__: unit_tests.py
# __brief__: Script that tests units one by one, nothing too crazy, just making sure my software behaves as it's supposed to behave

# TO RUN: pytest -vs unit_tests.py

# =========
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# =========

import ast
import logging
from unittest import mock
from unittest.mock import patch
import pytest
import math
import re

from utils.exceptions import FileEmptyError, CodeProcessingError
from utils.utility import _read_file_contents
from utils.utility import (
    _pretty_print,
    _pretty_print_debug_dict,
    _generate_readable_report,
)
from core.code_metrics import _classify_lines_of_code
from core.constants import TEST_PATHS

# ==== UNITS TO BE TESTED ====
from core.refactor import _refactor_with_ast
from core.method_length import _find_long_method
from core.param_length import _find_long_parameter_list
from core.duplicated_finder import _find_duplicated_code

from core.code_smells import find_code_smells

from core.halstead import (_extract_operators_and_operands,
                           fetch_halstead_metrics,
                           _calculate_halstead_metrics
                           )

from core.refactor import (
    _extract_functions,
    _find_duplicates,
    refactor_duplicates,
    _debug_dict,
)

from core.file_saver import save_refactored_file

# ==== UNITS TO BE TESTED ====


# =============================================== UTILITY ====================================================
def generate_ids(test_list: list):
    """_summary_

    Args:
        test_list (list): list of test cases, where each case is a tuple containing source code and expected results.

    Returns:
        _type_: id for the test case, based on the function names or expected names
    """
    ids = []
    for i, test_case in enumerate(test_list, start=1):
        try:
            source_code = test_case[0]
            tree = ast.parse(source_code)
            func_names = [
                node.name for node in tree.body if isinstance(node, ast.FunctionDef)
            ]
            if len(test_case) >= 3:
                expected_names = test_case[2]
                label = (
                    "_".join(expected_names[:2]) if expected_names else "no_expected"
                )
            else:
                label = "_".join(func_names[:2]) if func_names else "no_functions"
            label = f"num_{i}_{label}"
        except Exception:
            label = f"num_{i}_unknown_case"
        ids.append(label)
    return ids


# =============================================================================================================


# =============================================== LONG METHOD =================================================
LONG_METHOD = [
    (_read_file_contents(TEST_PATHS["1"]), True),
    (_read_file_contents(TEST_PATHS["2"]), True),
    (_read_file_contents(TEST_PATHS["3"]), False),
    (_read_file_contents(TEST_PATHS["4"]), True),
    (_read_file_contents(TEST_PATHS["5"]), True),
    (_read_file_contents(TEST_PATHS["6"]), False),
    (_read_file_contents(TEST_PATHS["7"]), True),
    (_read_file_contents(TEST_PATHS["8"]), False),
    (_read_file_contents(TEST_PATHS["9"]), True),
    (_read_file_contents(TEST_PATHS["10"]), True),
]


@pytest.mark.long_method
@pytest.mark.parametrize(
    "source_code, expected_non_empty", LONG_METHOD, ids=generate_ids(LONG_METHOD)
)
def test_find_long_method(source_code: str, expected_non_empty: bool):
    result = _find_long_method(source_code)

    assert isinstance(
        result, list
    ), f"Expected result to be a list but got {type(result)}"

    if expected_non_empty:
        assert (
            len(result) > 0
        ), f"Expected at least one long method, but found none.\nSource:\n{source_code}"
        for item in result:
            assert (
                "function" in item and "length" in item
            ), "Missing expected keys in result dict"
            assert (
                item["length"] > item["threshold"]
            ), "Reported method is not actually over threshold"
    else:
        assert len(result) == 0, "Expected no long methods, but some were found"


# =============================================================================================================


# =============================================== LONG PARAMS =================================================
LONG_PARAM = [
    (_read_file_contents(TEST_PATHS["11"]), True),
    (_read_file_contents(TEST_PATHS["12"]), False),
    (_read_file_contents(TEST_PATHS["13"]), True),
    (_read_file_contents(TEST_PATHS["14"]), True),
    (_read_file_contents(TEST_PATHS["15"]), True),
    (_read_file_contents(TEST_PATHS["16"]), True),
    (_read_file_contents(TEST_PATHS["17"]), False),
    (_read_file_contents(TEST_PATHS["18"]), True),
    (_read_file_contents(TEST_PATHS["19"]), True),
    (_read_file_contents(TEST_PATHS["20"]), True),
]


@pytest.mark.long_param
@pytest.mark.parametrize(
    "source_code, expected_non_empty", LONG_PARAM, ids=generate_ids(LONG_PARAM)
)
def test_find_long_parameter_list(source_code: str, expected_non_empty: bool):
    result = _find_long_parameter_list(source_code)

    assert isinstance(
        result, list
    ), f"Expected result to be a list but got {type(result)}"

    if expected_non_empty:
        assert (
            len(result) > 0
        ), "Expected one or more long parameter list functions, but found none"
        for entry in result:
            assert (
                "function" in entry and "params_count" in entry and "threshold" in entry
            ), f"Result missing required keys: {entry}"
            assert (
                entry["params_count"] > entry["threshold"]
            ), f"Reported function has {entry['params_count']} parameters but threshold is {entry['threshold']}"
    else:
        assert (
            len(result) == 0
        ), "Expected no long parameter list functions, but some were found"


# =============================================================================================================


# =================================================== DUPS ====================================================
DUPLICATES = [
    (_read_file_contents(TEST_PATHS["21"]), True),
    (_read_file_contents(TEST_PATHS["22"]), True),
    (_read_file_contents(TEST_PATHS["23"]), True),
    (_read_file_contents(TEST_PATHS["24"]), True),
    (_read_file_contents(TEST_PATHS["25"]), False),
    (_read_file_contents(TEST_PATHS["26"]), False),
    (_read_file_contents(TEST_PATHS["27"]), False),
    (_read_file_contents(TEST_PATHS["28"]), False),
    (_read_file_contents(TEST_PATHS["29"]), True),
    (_read_file_contents(TEST_PATHS["30"]), False),
]


@pytest.mark.duplicated_code
@pytest.mark.parametrize(
    "source_code, expected_non_empty", DUPLICATES, ids=generate_ids(DUPLICATES)
)
def test_find_duplicated_code(source_code: str, expected_non_empty: bool):
    result = _find_duplicated_code(source_code)

    assert isinstance(
        result, list
    ), f"Expected list from _find_duplicated_code but got {type(result)}"

    if expected_non_empty:
        assert (
            len(result) > 0
        ), "Expected duplicated code blocks to be found, but got none"

        for dup in result:
            assert (
                "block1" in dup and "block2" in dup and "similarity" in dup
            ), "Missing required keys in result item"
            assert isinstance(dup["similarity"], float), "Similarity should be a float"
            assert dup["similarity"] >= dup["threshold"], "Similarity below threshold"

            for block_key in ("block1", "block2"):
                block = dup[block_key]
                for required_field in ("text", "tokens", "line_number"):
                    assert (
                        required_field in block
                    ), f"Missing field '{required_field}' in {block_key}"
                assert isinstance(
                    block["tokens"], list
                ), f"{block_key}.tokens must be a list"

    else:
        assert (
            len(result) == 0
        ), "Expected no duplicated code blocks, but some were found"


# =============================================================================================================


# =============================================== REFACTORING =================================================
REFACTOR = [
    (_read_file_contents(TEST_PATHS["31"]), True),
    (_read_file_contents(TEST_PATHS["32"]), True),
    (_read_file_contents(TEST_PATHS["33"]), True),
    (_read_file_contents(TEST_PATHS["34"]), True),
    (_read_file_contents(TEST_PATHS["35"]), True),
    (_read_file_contents(TEST_PATHS["36"]), True),
    (_read_file_contents(TEST_PATHS["37"]), True),
    (_read_file_contents(TEST_PATHS["38"]), True),
    (_read_file_contents(TEST_PATHS["39"]), True),
    (_read_file_contents(TEST_PATHS["40"]), True),
]


def is_helper_generated(refactored_code: str) -> bool:
    """_summary_

    Args:
        refactored_code (str): The refactored code to check for helper function generation.

    Returns:
        bool: True if a helper function was generated, False otherwise.
    """
    return any("_common_logic_" in line for line in refactored_code.splitlines())


@pytest.mark.refactor
@pytest.mark.parametrize(
    "source_code, expect_helper",
    REFACTOR,
    ids=generate_ids(REFACTOR),
)
def test_refactor_cases(source_code: str, expect_helper: bool):
    """_summary_

    Args:
        source_code (str): The source code to be tested.
        expect_helper (bool): Flag indicating whether a helper function is expected to be generated.
    """
    try:
        tree = ast.parse(source_code)
        functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
        func_names = [func.name for func in functions]

        if len(functions) < 2:
            pytest.fail(
                f"Test case requires at least two functions to compare. Found: {func_names} in:\n{source_code}"
            )

        duplicates = [(func_names[0], func_names[1], 1.0)]
        refactored = _refactor_with_ast(source_code, duplicates)
        helper_found = is_helper_generated(refactored)
        assert (
            helper_found == expect_helper
        ), f"Expected helper to be {expect_helper}, but got {helper_found} in:\n{refactored}"

    except Exception as e:
        if expect_helper:
            pytest.fail(
                f"Test case expected helper function but refactoring failed: {e}\nSource Code:\n{source_code}"
            )
        else:
            pytest.fail(
                f"Refactoring unexpectedly failed when no helper was expected: {e}\nSource Code:\n{source_code}"
            )


# =============================================================================================================

# ============================================ PRIVATE METHODS ================================================
EXTRACT_FUNCTIONS = [
    (_read_file_contents(TEST_PATHS["5"]), True, ["filter_and_sort_dictionary"]),
    (_read_file_contents(TEST_PATHS["12"]), True, ["format_address"]),
    (
        _read_file_contents(TEST_PATHS["23"]),
        True,
        ["calculate_area_rectangle_v1", "compute_volume_cuboid_v1"],
    ),
    (
        _read_file_contents(TEST_PATHS["24"]),
        True,
        ["get_rectangle_area_v2", "find_cuboid_volume_v2"],
    ),
    (
        _read_file_contents(TEST_PATHS["8"]),
        True,
        ["find_common_elements_with_whitespace"],
    ),
    (_read_file_contents(TEST_PATHS["17"]), True, ["process_sensor_data"]),
]


@pytest.mark.refactor
@pytest.mark.parametrize(
    "source_code, expect_non_empty, expected_names",
    EXTRACT_FUNCTIONS,
    ids=generate_ids(EXTRACT_FUNCTIONS),
)
def test_extract_functions(
    source_code: str, expect_non_empty: bool, expected_names: list[str]
) -> None:
    """Test function extraction logic."""

    functions = _extract_functions(source_code)

    if expect_non_empty:
        assert functions, "Expected non-empty function extraction result"
        extracted_names = list(functions.keys())
        for name in expected_names:
            assert (
                name in extracted_names
            ), f"Expected function '{name}' not found in extracted functions"
    else:
        assert not functions, "Expected no functions, but some were extracted"


# ================

DUPS = [
    (_read_file_contents(TEST_PATHS["32"]), True),
    (_read_file_contents(TEST_PATHS["9"]), False),
    (_read_file_contents(TEST_PATHS["35"]), True),
    (_read_file_contents(TEST_PATHS["31"]), True),
    (_read_file_contents(TEST_PATHS["5"]), False),
    (_read_file_contents(TEST_PATHS["37"]), True),
]


@pytest.mark.parametrize("source_code, expect_duplicates", DUPS, ids=generate_ids(DUPS))
def test_find_duplicates(source_code, expect_duplicates):
    func_map = _extract_functions(source_code)
    duplicates = _find_duplicates(func_map)

    if expect_duplicates:
        assert duplicates, "Expected duplicates, but found none"
        for dup in duplicates:
            assert isinstance(dup, tuple)
            assert len(dup) == 3
            assert 0 <= dup[2] <= 1
    else:
        assert not duplicates, f"Did not expect duplicates, but found: {duplicates}"


# ================

REFACTOR_DUPS = [
    (TEST_PATHS["32"], True),
    (TEST_PATHS["9"], False),
    (TEST_PATHS["35"], True),
    (TEST_PATHS["31"], True),
    (TEST_PATHS["5"], False),
    (TEST_PATHS["39"], True),
]


@pytest.mark.parametrize(
    "filepath, expect_change", REFACTOR_DUPS, ids=generate_ids(REFACTOR_DUPS)
)
def test_refactor_duplicates(filepath, expect_change):
    result, changed = refactor_duplicates(filepath)

    assert isinstance(result, str)
    assert isinstance(changed, bool)

    if expect_change:
        assert changed is True
        assert "def " in result or "No duplicates" not in result
    else:
        assert changed is False
        assert "# No duplicates" in result


# ================

DBG = [
    (_read_file_contents(TEST_PATHS["32"])),
    (_read_file_contents(TEST_PATHS["9"])),
    (_read_file_contents(TEST_PATHS["35"])),
    (_read_file_contents(TEST_PATHS["31"])),
    (_read_file_contents(TEST_PATHS["5"])),
    (_read_file_contents(TEST_PATHS["39"])),
]


@pytest.mark.parametrize("source_code", DBG, ids=generate_ids(DBG))
def test_debug_dict(source_code):
    debug = _debug_dict(source_code, threshold=0.8)

    assert isinstance(debug, dict)
    assert "functions" in debug
    assert "tokens" in debug
    assert "similarities" in debug
    assert "duplicates" in debug

    assert isinstance(debug["functions"], dict)
    assert isinstance(debug["tokens"], dict)
    assert isinstance(debug["similarities"], list)
    assert isinstance(debug["duplicates"], list)


# =============================================================================================================


# ============================================== FILE SAVER ===================================================
@pytest.fixture
def mock_time():
    with mock.patch("time.strftime", return_value="20250419_120000"):
        yield


@pytest.fixture
def mock_dirs():
    with mock.patch("os.makedirs") as mock_makedirs:
        yield mock_makedirs


@pytest.fixture
def mock_open_file():
    m = mock.mock_open()
    with mock.patch("builtins.open", m):
        yield m


def test_save_valid_file(mock_time, mock_dirs, mock_open_file):
    content = "def foo():\n    pass\n"
    filename = "example.py"

    path = save_refactored_file(content, filename)

    assert path.endswith("refactored_example_20250419_120000.py")
    mock_open_file.assert_called_once_with(path, "w", encoding="utf-8")
    handle = mock_open_file()
    handle.write.assert_called_once_with(content)


def test_save_empty_file_raises_error():
    with pytest.raises(FileEmptyError) as exc:
        save_refactored_file("   \n   ", "empty.py")

    assert "File content is empty" in str(exc.value)


def test_filename_structure(mock_time, mock_dirs, mock_open_file):
    content = "# Sample code"
    filename = "dir/another_file.py"

    result = save_refactored_file(content, filename)
    base = os.path.basename(result)

    assert base.startswith("refactored_another_file_")
    assert base.endswith(".py")


# =============================================================================================================


# =============================================== UTILITY =====================================================
MOCK_ANALYSIS = {
    "long_parameter_list": [
        {
            "function": "log_event_detailed_v2",
            "position": 60,
            "params_count": 8,
            "threshold": 3,
        },
        {
            "function": "audit_operation_complex_v2",
            "position": 110,
            "params_count": 10,
            "threshold": 3,
        },
    ],
    "long_method": [
        {
            "function": "setup_logger",
            "start_line": 10,
            "end_line": 60,
            "length": 50,
            "threshold": 40,
        }
    ],
    "duplicated_code": [
        {
            "block1": {
                "index": 0,
                "text": 'if not isinstance(data_list, list) or not isinstance(expected_length, int):\n        raise TypeError("First argument must be a list, second must be an integer.")\n    return len(data_list) == expected_length',
                "type": "code",
                "tokens": [
                    "if",
                    "not",
                    "VAR",
                    "(",
                    "VAR",
                    ",",
                    "VAR",
                    ")",
                    "or",
                    "not",
                    "VAR",
                    "(",
                    "VAR",
                    ",",
                    "VAR",
                    ")",
                    ":",
                    "raise",
                    "VAR",
                    "(",
                    "VAR",
                    ")",
                    "return",
                    "VAR",
                    "(",
                    "VAR",
                    ")",
                    "==",
                    "VAR",
                ],
                "line_number": 2,
            },
            "block2": {
                "index": 1,
                "text": 'if not isinstance(array_data, list) or not isinstance(target_size, int):\n        raise TypeError("First argument must be a list, second must be an integer.")\n    return len(array_data) == target_size',
                "type": "code",
                "tokens": [
                    "if",
                    "not",
                    "VAR",
                    "(",
                    "VAR",
                    ",",
                    "VAR",
                    ")",
                    "or",
                    "not",
                    "VAR",
                    "(",
                    "VAR",
                    ",",
                    "VAR",
                    ")",
                    ":",
                    "raise",
                    "VAR",
                    "(",
                    "VAR",
                    ")",
                    "return",
                    "VAR",
                    "(",
                    "VAR",
                    ")",
                    "==",
                    "VAR",
                ],
                "line_number": 6,
            },
            "similarity": 1.0,
            "threshold": 0.75,
        }
    ],
    "code_metrics": {
        "LOC": 8,
        "SLOC": 15,
        "Comment Density": 0.4,
        "Blank Line Density": 0.067,
    },
    "halstead_metrics": {
        "n1": 2,
        "n2": 18,
        "N1": 3,
        "N2": 24,
        "N": 27,
        "n": 20,
        "V": 116.692,
        "D": 1.333,
        "HN": 77.059,
        "E": 155.589,
        "T": 8.644,
        "B": 0.052,
        "M": 57.958,
    },
}


@pytest.fixture
def mock_open_and_load():
    m = mock.mock_open()
    with mock.patch("builtins.open", m), mock.patch(
        "json.load", return_value=MOCK_ANALYSIS
    ), mock.patch("os.makedirs"), mock.patch(
        "textwrap.dedent", side_effect=lambda x: x
    ):
        yield m


def test_generate_report_success(mock_open_and_load):
    fake_path = "some/fake_analysis.json"

    with mock.patch("os.path.abspath", return_value="/abs"), mock.patch(
        "os.path.dirname", return_value="/abs"
    ):
        out_path = _generate_readable_report(fake_path)

    assert "report_fake_analysis_readable.md" in out_path

    # Ensure it attempted to write the report
    handle = mock_open_and_load()
    assert handle.write.call_count > 0


def test_generate_report_empty_metrics(mock_open_and_load):
    minimal_analysis = {
        "code_metrics": {},
        "halstead_metrics": {},
        "long_parameter_list": [],
        "long_method": [],
        "duplicated_code": [],
    }
    with mock.patch("json.load", return_value=minimal_analysis), mock.patch(
        "os.path.abspath", return_value="/abs"
    ), mock.patch("os.path.dirname", return_value="/abs"):
        _generate_readable_report("empty.json")

    handle = mock_open_and_load()
    written = "".join(call.args[0] for call in handle.write.call_args_list)
    assert "*No code metrics found.*" in written
    assert "*No duplicated code was found.*" in written


def test_report_handles_path_safely(mock_open_and_load):
    with mock.patch("os.path.abspath", return_value="/project"), mock.patch(
        "os.path.dirname", return_value="/project"
    ):
        result = _generate_readable_report("test/path/abc.json")

    assert "report_abc_readable.md" in result


FUNC_DICT = {
    "foo": {"text": "def foo():\n    return 42", "start": 1, "end": 2},
    "bar": {"text": "def bar():\n    return 0", "start": 4, "end": 5},
}

DEBUG_DICT = {
    "functions": {"foo": {"start": 1, "end": 2, "text": "def foo():\n    return 42"}},
    "tokens": {"foo": ["def", "foo", "(", ")", ":", "return", "42"]},
    "similarities": [[["foo", "bar"], 0.85]],
    "duplicates": [{"block1": "foo", "block2": "bar"}],
}

# === TEST CASES ===


def test_pretty_print_output(capsys):
    _pretty_print(FUNC_DICT)
    captured = capsys.readouterr().out

    assert '"foo": {' in captured
    assert '"bar": {' in captured
    assert '"""' in captured
    assert '    "end": 5' in captured
    assert captured.strip().endswith("]")


def test_pretty_print_debug_dict_output(capsys):
    _pretty_print_debug_dict(DEBUG_DICT)
    captured = capsys.readouterr().out

    assert '"functions": {' in captured
    assert '"foo": {' in captured
    assert '"tokens": {' in captured
    assert '"similarities": [' in captured
    assert '"duplicates": [' in captured
    assert "def foo():" in captured


# =============================================================================================================

# =========================================== CODE METRICS ====================================================

# logger to avoid unwanted output during tests
logging.getLogger("code_metrics_logger").setLevel(logging.CRITICAL)


def test_classify_lines_of_code_various_cases():
    source = """
# Single-line comment

def foo():
    '''This is
    a multi-line
    comment'''
    x = 42  # Inline comment
    y = "string with # not a comment"

    \"\"\"Another multi-line
    comment with triple double quotes\"\"\"
    return x

\"\"\"Standalone multi-line comment on one line\"\"\"

# Another single-line comment
    """

    result = _classify_lines_of_code(source)

    assert isinstance(result, dict)
    assert set(result.keys()) == {"code", "comments", "blank_lines"}

    # Check counts
    assert len(result["blank_lines"]) > 0
    assert len(result["comments"]) > 0
    assert len(result["code"]) > 0

    # Specific line checks
    all_comments = "\n".join(result["comments"])
    assert "# Single-line comment" in all_comments
    assert "'''This is" in all_comments
    assert '"""Another multi-line' in all_comments
    assert '"""Standalone multi-line comment on one line"""' in all_comments
    assert (
        "# Inline comment" not in all_comments
    )  # Inline comment shouldn't count as a full comment line

    all_code = "\n".join(result["code"])
    assert "def foo():" in all_code
    assert "x = 42" in all_code
    assert 'y = "string with # not a comment"' in all_code
    assert "return x" in all_code

    all_blanks = result["blank_lines"]
    assert any(line.strip() == "" for line in all_blanks)


def test_empty_input():
    result = _classify_lines_of_code("")
    assert result == {"comments": [], "blank_lines": [], "code": []}


def test_inline_comment_only():
    result = _classify_lines_of_code("x = 1  # comment")
    assert result["code"] == ["x = 1  # comment"]
    assert not result["comments"]
    assert not result["blank_lines"]


# =============================================================================================================

# =========================================== HALSTEAD METRICS ====================================================

@pytest.mark.parametrize("code,expected_keys", [
    ("a = b + c", {"unique_operators", "unique_operands", "total_operators", "total_operands"}),
    ("if a == b:\n    pass", {"unique_operators", "unique_operands", "total_operators", "total_operands"}),
])
def test_extract_operators_and_operands_valid(code, expected_keys):
    result = _extract_operators_and_operands(code)
    assert isinstance(result, dict)
    assert set(result.keys()) == expected_keys
    assert all(isinstance(v, (set, list)) for v in result.values())

def test_extract_operators_and_operands_empty_input():
    with pytest.raises(CodeProcessingError, match="No valid code content found"):
        _extract_operators_and_operands("   \n  ")

def test_calculate_halstead_metrics_typical_case():
    info = {
        "unique_operators": {"+", "="},
        "unique_operands": {"a", "b", "c"},
        "total_operators": ["=", "+"],
        "total_operands": ["a", "b", "c"]
    }
    metrics = _calculate_halstead_metrics(info)

    assert isinstance(metrics, dict)
    assert metrics["n1"] == 2
    assert metrics["n2"] == 3
    assert metrics["N1"] == 2
    assert metrics["N2"] == 3
    assert metrics["N"] == 5
    assert metrics["n"] == 5
    assert metrics["V"] == round(5 * math.log2(5), 3)


@patch("core.halstead._read_file_contents")
def test_fetch_halstead_metrics(mock_read):
    mock_read.return_value = "x = y + z"

    metrics = fetch_halstead_metrics("fake/path.py")
    assert isinstance(metrics, dict)
    assert all(key in metrics for key in ("V", "D", "E", "T", "B", "M"))

# =============================================================================================================

# =========================================== CODE SMELLS =====================================================

FIND_SMELLS = [
    (TEST_PATHS["9"],  True),
    (TEST_PATHS["1"],  True),
    (TEST_PATHS["32"], True),
    (TEST_PATHS["22"], True),
    (TEST_PATHS["11"], True),
    (TEST_PATHS["17"], True),
    (TEST_PATHS["5"],  True)
    ]

@pytest.mark.parametrize("source_code, expected_non_empty", FIND_SMELLS,
                         ids=generate_ids(FIND_SMELLS))
def test_find_code_smells_success(source_code, expected_non_empty):
    smells, path = find_code_smells(source_code)

    assert isinstance(smells, dict)
    assert (smells != {}) == expected_non_empty

    assert re.search(r"report_report_\w+_\d{8}_\d{6}_readable\.md", path), f"Unexpected path: {path}"

# =============================================================================================================
