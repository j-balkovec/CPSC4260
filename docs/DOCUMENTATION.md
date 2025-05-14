# Documentation

**Project Name**: Code Smell App  
**Class**: CPSC 4260 - Software Refactoring  
**Name**: Jakob Balkovec  
**Date**: May 11, 2025  

This document provides comprehensive documentation for the **Code Smell App** project, detailing each module, class, and function. It serves as a guide for users, developers, and evaluators to understand the codebase, its functionality, and its structure.

>**Note**: A pilar of this project was "**Abstraction From the Client**", meaning that a lot of internal operations are hidden from the client, but not strictly enforced through classes and interfaces. This is to allow for a more flexible and extensible codebase, where the client can focus on high-level operations without needing to understand the underlying implementation details.

## Project Structure

The following outlines the key files and directories in the **CodeSmellApp** repository, organized by directory with brief descriptions of each file's purpose.

- [**Directory: `core/`**](#directory-core)
  - [`code_metrics.py`](#code_metricspy): Calculates code quality metrics for analysis.
  - [`code_smells.py`](#code_smellspy): Detects code smells in Python files.
  - [`constants.py`](#constantspy): Defines constants used across the application.
  - [`duplicated_finder.py`](#duplicated_finderpy): Identifies duplicated code segments.
  - [`file_info_extractor.py`](#file_info_extractorpy): Extracts metadata from source files.
  - [`file_saver.py`](#file_saverpy): Handles saving refactored code to files.
  - [`halstead.py`](#halsteadpy): Computes Halstead complexity metrics.
  - [`method_length.py`](#method_lengthpy): Analyzes method length for code smell detection.
  - [`param_length.py`](#param_lengthpy): Evaluates parameter list lengths in functions.
  - [`refactor.py`](#refactorpy): Performs code refactoring, such as removing duplicates.
<br>

- [**Directory: `gui/`**](#directory-gui)
  - [`new_ui.py`](#new_uipy): Implements the main Textual-based GUI for the app.
  - [`terminal_ui.py`](#terminal_uipy): Provides a terminal-based UI alternative.
  - [`textual_ui.css`](#textual_uicss): CSS styles for the Textual GUI.
<br>

- [**Directory: `playground/`**](#directory-playground)
  - [`playground.py`](#playgroundpy): Experimental scripts for testing and prototyping.
<br>

- [**Directory: `utils/`**](#directory-utils)
  - [`exceptions.py`](#exceptionspy): Defines custom exceptions for the application. **TODO**
  - [`utility.py`](#utilitypy): Utility functions for file operations and helpers. **TODO**
  - [`logger.py`](#loggerpy): Configures logging for the application.
<br>

- [**Directory: `tests/`**](#directory-tests)
  - [`Makefile`](#makefile): Build script for running tests and other tasks.
  - [`unit_tests.py`](#unit_testspy): Unit tests for individual components. **TODO**
  - [`sys_tests.py`](#sys_testspy): System-level integration tests. **TODO**
  - [`test<n>.py`](#testnpy): Additional test files (e.g., `test1.py`, `test2.py`).
  - [`pytest.ini`](#pytestini): Configuration file for pytest.
  - [`conftest.py`](#conftestpy): Pytest fixtures and setup for testing.
<br>

- [**Directory: `docs/`**](#directory-docs)
  - [`DOCUMENTATION.md`](#documentationmd): This documentation file.
  - [`duplicated_code_guide.md`](#duplicated-code-guidemd): Guide for understanding duplicated code detection.
<br>

- [**Directory: Project Root**](#directory-project-root)
  - [`README.md`](#readmemd): Project overview and setup instructions.
  - [`requirements.txt`](#requirementstxt): Python package dependencies.
  - [`LICENSE`](#license): License information for the project.
<br>

---

## **Directory: `core/`**

### **`code_metrics.py`**

### **Overview**

This file contains the functions that calculate the LOC/SLOC code metrics for a given file.

> **Note**: Functions prefixed with an underscore (`_`) are intended to be private and must not be accessed or invoked outside this directory. They are exclusively used internally by the corresponding public functions.
> 

### **Functions**

#### **`def _classify_lines_of_code(source_code: str) -> dict:`**

- **Brief:** Classifies lines of code into lines of code, comments, and blank lines.
- **Args:**
    - `source_code (str)`: The source code to analyze, passed in as a string.
- **Returns:**
    - `dict`: A dictionary containing the lines of code, comments, and blank lines.
- **Notes:**
    - The function groups lines of code into comments, blank lines, and actual code.
    - It handles single-line comments, multi-line comments, and blank lines.
    - flag (`in_multiline_comment`): if in a multiline comment or not
    - delimiter (`multiline_delimiter`): to track if it starts with either `\'\'\'` or `\"\"\"`

#### **`def _calculate_code_metrics(info_dict: dict) -> dict:`**

- **Brief:** Calculates the lines of code (`LOC`) and source lines of code (`SLOC`) for a given file.
- **Args:**
    - `info_dict (dict)`: dictionary containing the lines of code, comments, and blank lines.Returned by `_classify_lines_of_code`
- **Returns:**
    - `dict`: A dictionary containing the metrics

#### **`def fetch_code_metrics(file_name: str) -> dict:`**

- **Brief:** Serves as the public interface to fetch code metrics for a given file.
- **Args:**
    - `file_name (str)`: Name of the file to analyze.
- **Returns:**
    - `dict`: A dictionary containing the metrics

> **Note:** This is a wrapper function
> 

> **Note:** `fetch_code_metrics` returns a dictionary to allow for further processing of the metrics. The dictionary is in JSON serializable format, and contains the following keys:
> 
> - `LOC`: Lines of code
> - `SLOC`: Source lines of code
> - `Comment Density`: Number of comment lines
> - `Blank Line Density`: Number of blank lines

---

### **`code_smells.py`**

### **Overview**

This file serves as the interface for finding code smells 

> **Note**: Functions prefixed with an underscore (`_`) are intended to be private and must not be accessed or invoked outside this directory. They are exclusively used internally by the corresponding public functions.
> 

### **Functions**

#### `def find_code_smells(file_name: str) -> Tuple[Dict, str]:`

- **Brief:** This function invokes a bunch of internal functions (defined with the `_` prefix) to find all the code smells in a given file containing source code.
- **Args:**
    - `file_name: str`: The name of the file to be processes/analyzed
- **Returns:**
    - `Tuple[Dict, str]`: A tuple containing all the code smells found in the file (`dict`) and a path (`str`) to the readable report to be rendered in the GUI.
- **Internally Calls:**
    - `_read_file_contents()`
    - `_find_long_parameter_list()`
    - `_find_duplicated_code()`
    - `fetch_code_metrics()`
    - `fetch_halstead_metrics()`

> **Note:** If this function throws or propagates an error, or if bugs arise during future development, examining the stack trace can help identify the origin of the issue.
> 

---

### **`constants.py`**

### **Overview**

This file contains all constants used across the codebase. Centralizing these values is intentional, as it simplifies maintenance and prevents shotgun surgery when modifying thresholds, bounds, or other shared parameters.

> **Note**: If you wish to introduce any new constants to the codebase, please add them to this file and import them using `from core.constants import <constant>`
>

#### **Error Codes**

- `ERROR_CODES: dict`  
Defines custom error codes for exception handling. These are used in conjunction with the custom exceptions defined in `utils/exceptions.py`.

<style>
  table {
    width: 100%;
    table-layout: auto;
  }
</style>

| **Error Code** | **Description**          |
|----------------|--------------------------|
| `1001`         | File Read                |
| `1002`         | Corrupt File             |
| `1003`         | File Not Found           |
| `1004`         | File Empty               |
| `1005`         | File Type Unsupported    |
| `1006`         | File Decode Error        |
| `1007`         | File Locked              |
| `1008`         | File Too Large           |
| `1009`         | File Open Error          |

> **Note:** For resolution guidance, refer to the [`exceptions.py`](#exceptionspy) source code.

#### **Terminal Formatting**

Color codes for standardized CLI output:
```python
YELLOW_TEXT: \033[33m
RED_TEXT: \033[31m
RESET_TEXT: \033[0m  # reset to default
```


These are used to highlight warnings and errors in a cross-platform compatible way (primarily on Unix-based systems).

#### **Size Limit**

- `SIZE_LIMIT: int = 10 * 1024 * 1024`  
Defines the maximum allowed file size for analysis (10 MB). Files larger than this will raise a `file_too_large` error.

#### **Allowed Operators**

- `ALLOWED_OPERATORS: Set[str]`  
Defines the set of tokenized operators considered during analysis. This set supports arithmetic, comparison, bitwise, assignment, and function-related operators. Any operator not in this list may be flagged during static analysis or ignored by the parser.

#### **Thresholds**

Threshold constants used to trigger refactor suggestions or flags:
- `PARAMS_THRESHOLD`: Maximum number of function parameters before triggering a complexity warning (default: `3`)
- `LENGTH_THRESHOLD`: Maximum number of lines in a function before it's considered "long" (default: `15`)
- `DUPS_THRESHOLD`: Jaccard similarity threshold for identifying duplicated code blocks (default: `0.75`)

#### **Logging Color Config**

`LOG_COLORS: dict`  
Maps logging levels to color tags used in log rendering or CLI output.

```python
LOG_COLORS = {
    'DEBUG':    'cyan',
    'INFO':     'green',
    'WARNING':  'yellow',
    'ERROR':    'red',
    'CRITICAL': 'bold_red',
}
```

#### **Cleanup Paths**

- `CLEANUP_PATHS: dict`
File system paths to intermediate or output files that may need to be cleared between runs or before deployment.

**Example**:
- `log_analyze`: path to log output
- `file_info, report, output`: analysis data directories

All paths are absolute and should be validated if moved to another environment.

#### **Environment Flag**

- `i_am_local: bool = False`
Set to `True` when working in a local development environment. This toggles specific behavior such as using local file paths that don’t exist in remote environments.

#### **Test File Paths**

- `TEST_PATHS: dict`
Maps test IDs (as strings) to absolute paths of test files used during development and regression testing. This dictionary supports Python and Java files and switches pathing for certain tests based on the `i_am_local flag`.

---

### **`duplicated_finder.py`**

### **Overview**

This file contains the logic for finding duplicated blocks of code in a given source code. As of right now it only supports Python files, but it can be extended to support other languages in the future. On top of that it is **only** capable of finding Type 1, Type 2, and Type 3 duplicates. Type 4 duplicates are not within the scope of this class, but an extension in the future is planned.

> **Note**: Functions prefixed with an underscore (`_`) are intended to be private and must not be accessed or invoked outside this directory. They are exclusively used internally by the corresponding public functions.
> 

### **Functions**

#### **`def _normalize_block(text: str) -> str:`**
- **Brief:** This function normalizes a block of code by removing any trailing whitespace or newlines (`"\n"`)
- **Args:**
    - `text: str`: String to be normalized
- **Returns:**
    - `(str)`: The normalized string (No trailing whitespace or newlines)

> **Note**: Invoked to compare two blocks of code.

#### **`def _split_into_blocks(source_code: str) -> list:`**
- **Brief:** This function splits the source code into logical blocks to prepare them for comparison. It looks for statements like: `def, class, for, while, if, else, elif, try, except, finally, with, ...`, and splits them accordingly.
- **Args:**
    - `source_code (str)`: Source code to process
- **Returns:**
    - `list`: List of (code_block_text, starting_line_number) tuples

> **Note**: The function is invoked to prepare the data. The internally defined function `flush_block()` is only meant to be invoked **once**. Invoking it more than once will result in unexpected behavior (This has been tested). Exercise caution when calling the function.
>

#### **`def _remove_comments(source_code: str) -> str:`**
- **Brief:** This function uses a regular expression to find single line, and multi-line comments in the source code and removes them. It also removes any comments that appear after a statement.
- **Args:**
    - `source_code (str)`: source code to be processed
- **Returns:**
    - `str`: raw source code without comments

#### **`def _tokenize_block(block: str) -> list:`**
- **Brief:** This function tokenizes a block of code into a set of tokens. This set of tokens is used later to determine the Jaccard similarity between two blocks of code. This is done through a series of regular expressions. Tokens used:
    ```
    STR
    NUM
    FLOAT
    TIME
    DATE
    DATETIME
    ```
- **Args:**
    - `block (str)`: block of code to be tokenized
- **Returns:**
    - `list`: list of tokens

> **Note**: If you wish, you can modify the return type to `set` to remove duplicates. This is not done in the current implementation, as all the tokens are needed to find Type 3 duplicates.

#### **`def _generate_ngrams(tokens: list, n: int = 3) -> set:`**
- **Brief:** This function generates n-grams (tri-grams by default) from a list of tokens. N-grams are contiguous sequences of `n` items from the input sequence. This is used to find Type 3 duplicates.

- **Args:**
    - `tokens (list)`: A list of tokens to be processed and re-structured into n-grams
    - `n (int, optional)`: size of the ngram, defaults to 3 (trigram).
- **Returns:**
    - `set`: set of ngrams to be used for comparison in `_jaccard_similarity()`

#### **`def _jaccard_similarity(tokens1: list, tokens2: list, ngram_size: int = 3) -> float:`**
- **Brief:** This function generates the similarity index between two sets of tokens using the [Jaccard similarity coefficient](https://en.wikipedia.org/wiki/Jaccard_index). This is done by generating n-grams from the tokens and then calculating the similarity between the two sets.

- **Args:**
    - `set1 (set)`: set of tokens A
    - `set2 (set)`: set of tokens B
- **Returns:**
    - `float`: Jaccard Similarity similarity score

- **Internally Calls:**
    - `_generate_ngrams()`

> **Note:** If this function throws or propagates an error, or if bugs arise during future development, examining the stack trace can help identify the origin of the issue.
> 

#### **`def _find_duplicated_code(source_code: str) -> list:`**

- **Brief:** This function identifies pairs of duplicated code blocks in the given source string by comparing their token similarity using the Jaccard metric. Filters out comments before processing and returns only block pairs with similarity above the defined threshold.

- **Args:**  
  `source_code (str)`: Raw source code string, typically obtained from `_read_file_contents()`.

- **Returns:**  
  `list`: A list of dictionaries, each representing a pair of duplicated code blocks that exceeded the `DUPS THRESHOLD` (see [`constants.py`](#constantspy)).

  ```python
  # Dictionary Returned
  {
    'block1': {'index': i,
                'text': block_i,
                'type': 'code', # formatting purposes 
                'tokens': list(tokens_i),
                'line_number': line_i},
    
    'block2': {'index': j,
                'text': block_j,
                'type': 'code', # formatting purposes
                'tokens': list(tokens_j),
                'line_number': line_j},
    'similarity': sim,
    'threshold': 0.75
  }
  ```

---

### **`file_info_extractor.py`**

### **Overview**

This script extracts all the necessary file info

> **Note**: Functions prefixed with an underscore (`_`) are intended to be private and must not be accessed or invoked outside this directory. They are exclusively used internally by the corresponding public functions.
> 

### **Functions**

#### **`extract_file_info(file_obj) -> dict`**

- **Brief:** Extracts validated metadata from a file object uploaded via GUI, handling all major file-related exceptions.

- **Args:**  
  - `file_obj (_type_)`: File object returned by `on_upload_file()`. See [`new_ui.py`](#new_uipy).

- **Returns:**  
  - `dict`: Dictionary of extracted metadata including file name, size, type, timestamps, and content.

- **Internally Calls:**
  - `_validate_file()`
  - `_gather_metadata()`

> **Note:** If this function throws or propagates an error, or if bugs arise during future development, examining the stack trace can help identify the origin of the issue.
> 

- **Throws:**  

    | Exception            | Description                                          |
    |----------------------|------------------------------------------------------|
    | `FileReadError`      | If the file fails validation or cannot be read.      |
    | `CorruptFileError`   | If metadata cannot be extracted.                     |
    | `FileLockedError`    | If OS-level permission is denied.                    |
    | `FileNotFoundError`  | If the file no longer exists.                        |
    | `FileOpenError`      | If any OS error occurs during file operations.       |
 
> **Note:** Exceptions are re-raised with enhanced context for better traceability.
> For resolution guidance, refer to the [`exceptions.py`](#exceptionspy) source code.
---

#### **`_validate_file(file_path: str) -> bool`**

- **Brief:** Ensures a file exists, is readable, is within size limits, and has an accepted extension.

- **Args:**  
  - `file_path (str)`: Absolute path to the file.

- **Returns:**  
  - `bool`: True if the file passes all validation checks.

- **Throws:**  

    | Exception                  | Description                                             |
    |----------------------------|---------------------------------------------------------|
    | `FileNotFoundError`        | If file does not exist.                                 |
    | `FileEmptyError`           | If file has 0 bytes.                                    |
    | `FileTooLargeError`        | If file exceeds `SIZE_LIMIT`.                           |
    | `FileTypeUnsupportedError` | If file extension is not allowed.                       |

> **Note:** Exceptions are re-raised with enhanced context for better traceability.
> For resolution guidance, refer to the [`exceptions.py`](#exceptionspy) source code.

- **Notes:**  
  Currently supports `.py` and `.txt` file types only.
---

#### **`_gather_metadata(file_path: str, file_obj) -> dict`**

- **Brief:**  
  Collects file metadata (name, size, type, timestamps, contents) from the validated file object.

- **Args:**  
  - `file_path (str)`: Absolute path to the file.  
  - `file_obj (_type_)`: File object returned from `upload_file()`. See `gui.py`.

- **Returns:**  
  - `dict`: Dictionary of extracted file metadata.

- **Throws:**  

    | Exception                  | Description                                             |
    |----------------------------|---------------------------------------------------------|
    | `FileDecodeError`          | If file reading fails due to encoding.                  |
    | `FileReadError`            | For other read failures.                                |

> **Note:** Exceptions are re-raised with enhanced context for better traceability.
> For resolution guidance, refer to the [`exceptions.py`](#exceptionspy) source code.

- **Notes:**  
  File content is read in full and stored under the `"Data"` key. Caller is responsible for ensuring memory usage.
---

#### **`save_to_json(metadata: dict)`**

- **Brief:**  
  Saves extracted file metadata into a JSON file with a timestamped filename under the `/data/file_info/` directory.

- **Args:**  
  - `metadata (dict)`: Metadata dictionary returned from `_gather_metadata()`.

- **Returns:**  
  - `str`: Path to the saved JSON file.

> **Note**: The directory is auto-created if missing. JSON files are named using: `info_<file_name>_<timestamp>.json`

---

### **`file_saver.py`**

### **Overview**

This script is used for saving the refactored code to a new file. It handles the file writing process and ensures that the file is saved in the correct format.

### **Functions**

#### **`def save_refactored_file(file_content: str, original_filename: str) -> str:`**
- **Brief:** Saves the refactored code to a new file with a timestamped filename. The new filename is derived from the original filename, and the file is saved in the same directory as the original file.
- **Args:**
    - `file_content (str):` The refactored code to be saved to the new file
    - `original_filename (str):` The original filename from which the new filename is derived
- **Returns:**
    - `str`: the new updated filename (Format: `refactored_<file_name>_<timestamp>.<extension>`)
- **Throws:**
    | Exception                  | Description                                             |
    |----------------------------|---------------------------------------------------------|
    | `FileEmptyError`           | If file has 0 bytes.                                    |

> **Note:** Exceptions are re-raised with enhanced context for better traceability.
> For resolution guidance, refer to the [`exceptions.py`](#exceptionspy) source code.
---

### **`halstead.py`**

### **Overview**

This file contains the logic for calculating the Halstead complexity metrics for a given source code. The Halstead complexity metrics are a set of software metrics that measure the complexity of a program based on the number of operators and operands in the code.

> **Note**: Functions prefixed with an underscore (`_`) are intended to be private and must not be accessed or invoked outside this directory. They are exclusively used internally by the corresponding public functions.
> 

### **Functions**

#### **`def _extract_operators_and_operands(source_code: str) -> dict:`**

- **Brief:** This function extracts the operators and operands from the source code using a regular expression. It returns a dictionary containing the operators and operands.
- **Args:**
    - `source_code (str)`: The source code to analyze, passed in as a string.
- **Returns:**
    - `dict`: Returns a dictionary with operators and operands as keys and their assignment as values (see below).
    ```python
    grouped = {
        "unique_operators": set(), # set = unique
        "unique_operands": set(),  # set = unique
        "total_operators": [],     # list = all
        "total_operands": [],      # list = all
    }
    ```
- **Throws:**
    | Exception                       | Description                                             |
    |---------------------------------|---------------------------------------------------------|
    | `CodeProcessingError`           | If the source code cannot be processed                  |

> **Note:** Exceptions are re-raised with enhanced context for better traceability.
> For resolution guidance, refer to the [`exceptions.py`](#exceptionspy) source code.


#### **`def _calculate_halstead_metrics(info_dict: dict) -> dict:`**

- **Brief:** Uses the extracted operators and operands to calculate the Halstead complexity metrics based on the formulas defined by [Maurice H. Halstead](https://en.wikipedia.org/wiki/Halstead_complexity_measures). It returns a dictionary containing the metrics.

- **Args:**
    - `info_dict (dict)`: The dictionary containing the total number, and unique number of operators and operands, returned by `_extract_operators_and_operands()`.
- **Returns:**
    - `dict`: dictionary with Halstead complexity metrics as keys and their assignment as values (see below).
    ```python
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
    ```

#### **`def fetch_halstead_metrics(file_name: str) -> dict:`**

- **Brief:** This function serves as the public interface to fetch the Halstead complexity metrics for a given file. It first extracts the operators and operands from the source code, and then calculates the Halstead complexity metrics based on the extracted operators and operands.

- **Args:**
    - `file_name: str`: The name of the file to be processed.
- **Returns:**
    - `dict`: dictionary with Halstead complexity metrics as keys and their assignment as values (see below).
    ```python
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
    ```

- **Internally Calls:**
    - `_read_file_contents()`
    - `_extract_operators_and_operands()`
    - `_calculate_halstead_metrics()`

> **Note:** If this function throws or propagates an error, or if bugs arise during future development, examining the stack trace can help identify the origin of the issue.
> 
---

### **`method_length.py`**

### **Overview**

This file contains the logic for analyzing the length of methods in a given source code.

> **Note**: Functions prefixed with an underscore (`_`) are intended to be private and must not be accessed or invoked outside this directory. They are exclusively used internally by the corresponding public functions.
> 

### **Functions**

#### **`_find_long_method(source_code: str) -> list:`**

- **Brief:** This function finds all the methods in the source code that exceed a certain length threshold. It returns a list of dictionaries containing the method name, start line, end line, length and the threshold.
- **Args:**
    - `source_code (str)`: The source code to analyze, passed in as a string.
- **Returns:**
    - `list`: A list of dictionaries containing the method name, start line, end line, length and the threshold, where a method has more that `LENGTH_THRESHOLD` lines (see [`constants.py`](#constantspy)).
    ```python
    # Dictionary Returned
    {
      "function": function_name,
      "start_line": start_line + 1,
      "end_line": end_line + 1,
      "length": method_length,
      "threshold": LENGTH_THRESHOLD
    }
    ```
> **Note**: The `start_line` and `end_line` are 0-indexed, so they are incremented by 1 to match the line numbers in the source code.

> **Note**: Is able to detect `async` methods, and methods with decorators. It does this by using a regular expression to find the method name, and then using the `ast` module to find the start and end line numbers of the method.
---

### **`param_length.py`**

### **Overview**

This file is responsible for analyzing the length of parameter lists in functions. It identifies functions with an excessive number of parameters, which can indicate potential code smells or design issues.

> **Note**: Functions prefixed with an underscore (`_`) are intended to be private and must not be accessed or invoked outside this directory. They are exclusively used internally by the corresponding public functions.
> 

### **Functions**

#### **`def _find_long_parameter_list(source_code: str) -> list:`**
- **Brief:** This function identifies functions with a number of parameters exceeding the defined threshold. It returns a list of dictionaries containing the function name, start line, end line, number of parameters, and the threshold.
- **Args:**
    - `source_code (str)`: The source code to analyze, passed in as a string.
- **Returns:**
    - `list`: A list of dictionaries, that hold all instances where a method has more than `PARAMS_THRESHOLD` parameters (see [`constants.py`](#constantspy))
    ```python
    # Dictionary Returned
    {
        "function": function_name,
        "position": i,
        "params_count": num_params,
        "threshold": PARAMS_THRESHOLD
    }
    ```
> **Note**: The `position` is 0-indexed, so it is incremented by `1` to match the line numbers in the source code.

---

# `refactor.py`

## Overview

This module is responsible for automatically refactoring Python source code by identifying duplicated function bodies, extracting the common logic into a new helper function, and replacing the original code with calls to this helper. The refactoring is driven by Abstract Syntax Tree (AST) transformations, ensuring structural correctness. Similarity detection uses token-based Jaccard similarity.

> **Note**: Functions prefixed with an underscore (`_`) are intended to be private and must not be accessed or invoked outside this directory. They are exclusively used internally by the corresponding public functions.

> **Note:** The module is not intended to run standalone; it should be invoked via a CLI tool or integrated pipeline Designed to work only on `.py` source files that use function-based logic. Assumes that function names are unique within the file and do not include decorators or nested definitions.

---

## Functions

#### `def _make_helper_node(func_name, args, body) -> ast.FunctionDef:`
- **Brief:** Creates a helper function node encapsulating common logic.

- **Args:**
  - `func_name (str)`: Name of the function to generate a helper from.
  - `args (list)`: List of argument names.
  - `body (list)`: List of AST statements representing the function body.

- **Returns:**
  - `ast.FunctionDef`: An AST node representing the helper function.

> **Note:** The name is derived by hashing the original name to avoid collisions.

---

#### `def _refactor_with_ast(source_code, duplicates) -> str:`
- **Brief:** Transforms code using AST to replace duplicate functions with a helper call.

- **Args:**
  - `source_code (str)`: Raw source code to refactor.
  - `duplicates (list)`: List of tuples of duplicate function names and similarity scores.

- **Returns:**
  - `str`: The refactored source code.


- **Throws:** 

    | Exception                       | Description                                             |
    |---------------------------------|---------------------------------------------------------|
    | `ValueError`                    | If duplicate function is not found in parsed AST.       |

---

#### `def _extract_functions(source_code) -> dict`
- **Brief:** Extracts all function definitions and tracks source offsets.

- **Args:**
  - `source_code (str)`: Raw Python code to scan.
- **Returns:**
  - `dict`: Mapping of function names to their metadata including positions and text.
  ```python
  {
      "name": node.name,
      "start": start_offset,
      "end": end_offset,
      "text": func_text
  }
  ```
- **Internally Calls:**
  - `_remove_comments()`
> **Note:** If this function throws or propagates an error, or if bugs arise during future development, examining the stack trace can help identify the origin of the issue.

> **Note:** Capable of handling cases where `end_lineno` is missing.

---

#### `def _find_duplicates(func_map) -> list:`
- **Brief:** Identifies pairs of functions with high token similarity.

- **Args:**
  - `func_map (dict)`: Map of function names to their metadata.

- **Returns:**
  - `list`: List of (func1, func2, similarity) tuples where similarity exceeds threshold.

- **Internally Calls:**
  - `_tokenize_block()`
  - `_jaccard_similarity()`

> **Note:** If this function throws or propagates an error, or if bugs arise during future development, examining the stack trace can help identify the origin of the issue.

> **Note:** Uses Jaccard similarity on tokenized functions.

---

#### `refactor_duplicates(filepath)`
- **Brief:** Main callable function to refactor a file.

- **Args:**
  - `filepath (str)`: Path to the Python file to be processed.
- **Returns:**
  - `(str, bool)`: Tuple of either the refactored code or message, and a success flag.

- **Internally Calls:**
  - `_tokenize_block()`
  - `_jaccard_similarity()`

> **Note:** If this function throws or propagates an error, or if bugs arise during future development, examining the stack trace can help identify the origin of the issue.

- **Throws:**

    | Exception                       | Description                                             |
    |---------------------------------|---------------------------------------------------------|
    | `CodeProcessingError`           | If the file cannot be read or parsed.                   |
  

> **Note:** Exits early iff no duplicates are found, to save processing time.

---

#### `_debug_dict(source_code, threshold=0.85)`
- **Brief:** Debugging utility for inspecting token similarity and matches.

- **Args:**
  - `source_code (str)`: Raw source code to analyze.
  - `threshold (float, optional)`: Similarity threshold to apply. Default is 0.85.

- **Returns:**
  - `dict`: Contains parsed functions, token maps, similarity data, and duplicates.

- **Internally Calls:**
  - `_extract_functions()`
  - `_tokenize_block()`
  - `_jaccard_similarity()`
  - `_find_duplicates()`

> **Note:** If this function throws or propagates an error, or if bugs arise during future development, examining the stack trace can help identify the origin of the issue.

> **Note**: Temporarily overrides the global similarity threshold.

> **Note**: It's purpose is to provide more information on how the refactoring process works, and to help debug any issues that may arise during the refactoring process. It is not intended to be used in production code.

---

## Classes

#### `DuplicateRefactorer(ast.NodeTransformer)`

- **Attributes:**
  - `dup_funcs (set)`: Set of duplicated function names.
  - `helper (ast.FunctionDef)`: AST node of the generated helper function.

- **Methods:**

  #### `visit_Module(node)`
  - **Brief:** Inserts helper function into the module body.
  - **Args:**
    - `node (ast.Module)`: The root module node.
  - **Returns:**
    - `ast.Module`: Transformed node with helper function injected.


  #### `visit_FunctionDef(node)`
  - **Brief:** Replaces duplicate function body with a helper call if applicable.
  - **Args:**
    - `node (ast.FunctionDef)`: The function to potentially replace.
  - **Returns:**
    - `ast.FunctionDef`: Modified or untouched function.

> **Note:** Automatically invoked by `_refactor_with_ast` to transform AST in place.

---

## **Directory: `gui/`**

### **`new_ui.py`**

### **Overview**

This file defines the graphical user interface (GUI) for the **Code Smell App**, a refactoring tool built with the [Textual](https://github.com/Textualize/textual) TUI framework. It handles user interaction for uploading, analyzing, refactoring, and saving Python files. It also manages themes, logs, modal dialogs, and reactive state.

---

### **Functions**

#### **`def set_project_root():`**
- **Brief**: Sets the `CPSC4260_GRADING` environment variable to the user’s home directory.

> **Note:** `STATUS: In development`

> **Note:** This function supports a grading use-case where the root directory for file browsing must be constrained. Called during development or testing under special flags.

---

### **Classes**

#### **class `ConfirmationDialog`**
- **Brief**: Modal dialog screen asking the user to confirm an action (e.g., exit, clear).
- **Attributes**:
  - `message (str)`: The message displayed in the dialog box.
- **Methods**:
  - `__init__(message: str)`
    - Initializes the dialog with a given message.
  - `compose()`
    - **Brief**: Yields layout components that make up the dialog UI.
    - **Returns**: `ComposeResult`
    - **Yields**: A vertical layout containing labels and two buttons: “Yes” and “No”.
  - `on_button_pressed(event: Button.Pressed)`
    - **Brief**: Handles the user’s selection. Dismisses the screen with a boolean value.
    - **Args**:
      - `event (Button.Pressed)`: The event representing which button was clicked.

> **Note:** Intended to be pushed as a modal on top of the main app. Uses `ModalScreen[bool]` to return a typed response to the app.

---

#### **class `FilePicker`**
- **Brief**: Modal file picker for selecting `.py` files from the file system.
- **Methods**:
  - `compose()`
    - **Brief**: Renders a vertical layout with an input for filtering and a directory tree rooted at the project directory.
    - **Yields**: A container with `Input` and `DirectoryTree`.
  - `on_directory_tree_file_selected(event: DirectoryTree.FileSelected)`
    - **Brief**: Validates the selected file and notifies the app.
    - **Args**:
      - `event (DirectoryTree.FileSelected)`: Event fired when the user picks a file.

> **Note:** The root directory is dynamic based on the `is_being_graded` flag. Only `.py` files are accepted; otherwise, the user is warned (enforced by `file_info_extractor.py`).

---

#### **class `UploadFileSelected`**
- **Brief**: Message class used to send selected file paths to the main app.
- **Attributes**:
  - `path (Path)`: Absolute path to the selected Python file.
- **Methods**:
  - `__init__(path: Path)`
    - **Args**: `path` representing the selected file.
    - Calls the superclass initializer.

> **Note:** Used for decoupled communication between modal and main app.

---

#### **class `CodeSmellApp`**
- **Brief**: Main application class handling UI layout, event responses, and interaction logic.
- **Attributes**:
  - `SCREENS (dict)`: Mapping screen names to modal classes.
  - `CSS_PATH (str)`: Path to external stylesheet.
  - `BINDINGS (list[tuple])`: Keyboard shortcuts.
  - `filename (reactive[str | None])`: Path to the selected file.
  - `theme_dark (reactive[bool])`: Theme state.
- **Methods**:

---

#### **`compose()`**
- **Brief**: Constructs and yields the full UI layout of the app.
- **Returns**: `ComposeResult`  
- **Yields**: Header, footer, left pane (log and buttons), right pane (code editor).

---

#### **`on_mount()`**
- **Brief**: Initializes editor with welcome message and logs usage instructions.
> **Note:** Displays a welcome message and instructions to the app upon user startup.

---

#### **`on_button_pressed(event)`**
- **Brief**: Central event handler for all toolbar buttons.
- **Args**:
  - `event (Button.Pressed)`: Button event with `id` to determine action.
- **Internally Calls**:
  - `analyze()`, 
  - `refactor()`, 
  - `save()`, 
  - `clear()` 
  - screen push/pop methods.
> **Note:** Theme toggling is handled here and switches between `light` and `dark` classes.

---

#### **`on_key(event)`**
- **Brief**: Stops key propagation when the code editor is focused to prevent shortcut conflicts.
- **Args**:
  - `event (events.Key)`

---

#### **`on_upload_file_selected(message)`**
- **Brief**: Loads selected Python file into the editor and displays info in log.
- **Args**:
  - `message (UploadFileSelected)`

- **Throws**:

    | Exception            | Description                                          |
    |----------------------|------------------------------------------------------|
    | `FileReadError`      | If the file cannot be read.                          |

- **Internally Calls**: 
  - `Path.read_text()`

> **Note:** Also updates file info label and handles empty files gracefully.

---

#### **`analyze()`**
- **Brief**: Analyzes selected file for code smells and displays Markdown report in the log.
- **Internally Calls**:
  - `find_code_smells`, 
  - `_read_file_contents`, 
  - `Markdown`, 
  - `RichLog.write`

- **Throws**:
    | Exception            | Description                                          |
    |----------------------|------------------------------------------------------|
    | `PermissionError`    | If OS-level permission is denied.                    |
    | `FileNotFoundError`  | If the file no longer exists.                        |
    | `Exception`          | Everything else                                      |

> **Note:** Output is Markdown-rendered in the `RichLog`.

---

#### **`refactor()`**
- **Brief**: Invokes backend refactoring logic and appends the result to the editor.
- **Internally Calls**:
  - `refactor_duplicates`

- **Throws**:
    | Exception            | Description                                          |
    |----------------------|------------------------------------------------------|
    | `PermissionError`    | If OS-level permission is denied.                    |
    | `FileNotFoundError`  | If the file no longer exists.                        |
    | `Exception`          | Everything else                                      |

> **Note:** Will replace code in editor with refactored version if found. 

> **Note:** Logs success/failure message to `RichLog`.

---

#### **`save()`**
- **Brief**: Saves the refactored code to a new file and logs the save path.
- **Internally Calls**:
  - `save_refactored_file`

- **Throws**:
    | Exception            | Description                                          |
    |----------------------|------------------------------------------------------|
    | `Exception`          | Generic Exception                                    |

> **Note:** File name/path is generated based on current working state.

---

#### **`clear()`**
- **Brief**: Clears editor and log content. Resets state.
- **Internally Calls**:
  - `TextArea.clear`, 
  - `RichLog.clear`
> **Note:** Triggers only after user confirms via `ConfirmationDialog`.

---

> **Note:** All user-triggered logic is separated into modal screens and event-driven handlers for better maintainability.

> **Note:** Light/dark theme toggling is implemented but relies on stylesheet classes being properly defined in `textual_ui.css`.

> **Note:** File access is mildly sandboxed via `is_being_graded`, but this is not secure against adversarial users.

> **Note:** Easily supports new toolbar buttons or modal dialogs due to `Textual`'s reactive component model.

> **Note:**  Log pane uses `rich.markdown.Markdown`, allowing detailed analysis reports with formatting.

---

### **`terminal_ui.py`**

### **Overview**

This file defines the terminal user interface (TUI) for the **Code Smell App**. It handles user interaction for uploading, analyzing, refactoring, and saving Python files. It also manages themes, logs, modal dialogs, and reactive state.

> **Note**: Functions prefixed with an underscore (`_`) are intended to be private and must not be accessed or invoked outside this directory. They are exclusively used internally by the corresponding public functions.

> **Note**: `STATUS: In development`

<!-- 
#### **Functions**

### **function_name(args)**

- **Args:**
    - `arg1 (type)`: Description.
    - `arg2 (type, optional)`: Description. Default is X.
- **Returns:**
    - (type): What the function returns.
- **Throws:**
    - ExceptionType: When it’s thrown and why.
- **Yields:**
    - (type): If it’s a generator, what it yields.
- **Brief:**One-sentence purpose of the function.
- **Notes:**Any implementation quirks, assumptions, or caveats.
-->

---

### **`textual_ui.css`**

### **Overview**

This file defines the styles for the Textual-based **Code Smell App** user interface. It customizes the layout, color themes, and behavior of UI components like panes, buttons, editors, logs, and modal dialogs. The file supports both light and dark themes and ensures accessibility and a clean, readable layout.

> **Note:** This stylesheet uses the [Textual CSS dialect](https://textual.textualize.io/) with some custom variables (e.g., `$accent`, `$panel`, `$success`) defined in the project or inherited from the framework.

> **Note:** If you make changes to this file, ensure the CSS is valid Textual CSS. You can use the `textual` command-line tool to validate your CSS.

---

### **Styles**

#### **Main Layout Containers**
- `#main-pane`
  - Full height container with horizontal layout splitting left and right panes.

- `#left-pane`, `#right-pane`
  - Vertically-stacked columns, each taking up 50% width.
  - `min-width: 20` ensures usability on narrow terminals.

#### **Log Panel**
- `#log`
  - Scrollable container styled with:
    - Rounded yellow border
    - Black background
    - Padding for spacing
  - Dynamically themed via `.dark` and `.light`.

#### **Code Editor**
- `#code_editor`
  - Dedicated area for code display or editing.
  - Styled with green border and dark background.
  - Responsive to theme changes for contrast/readability.

#### **Buttons and Controls**
- `#buttons`
  - Horizontally-aligned container for action buttons.
  - Centrally positioned at the top of the layout.
  - Responsive spacing (`margin`, `padding`) for clean alignment.

- `#buttons Button`
  - Minimum width enforced to maintain visual balance.
  - Margins ensure separation between buttons.

- `#file_info`
  - Displays current filename and file-related metadata.
  - Styled in gray italics for non-dominant visual presence.

---

#### **Themes**

##### **Dark Theme (`.dark`)**
- Base background: `#1e1e1e` or `#2e2e2e`
- Text color: White (`#ffffff`)
- Used for:
  - App shell background
  - Log panel
  - Code editor
  - Dialog elements

##### **Light Theme (`.light`)**
- Base background: White (`#ffffff`) or off-white (`#f5f5f5`)
- Text color: Black (`#000000`)
- Used for:
  - App shell background
  - Log panel
  - Code editor
  - Dialog elements

---

#### **Confirmation Dialogs**

- `.confirmation-dialog`
  - Modal overlay centered both horizontally and vertically.
  - Bounded dimensions (`width`, `height`, `max-width`) for consistent sizing.
  - Transparent background allows it to appear as a floating modal.

- `#dialog-title`
  - Top label for modal dialog
  - Styled with border and centered text
  - Color varies by theme (`#4CAF50` in dark, `#F5F5F5` in light)

- `#dialog-container`
  - Main body of the dialog box
  - Uses theme-dependent background and border styling
  - Provides internal padding and fixed dimensions

- `#dialog-message`
  - Styled text section showing the confirmation prompt
  - Responsive text alignment and color

- `#button-container` and `#dialog-container Horizontal`
  - Controls layout for dialog action buttons
  - Aligns buttons centrally with dynamic sizing

---

#### **Confirmation Buttons**

- `#confirm_yes` and `#confirm_no`
  - Theme-colored backgrounds to indicate intent:
    - Yes: Success green shades
    - No: Error red shades
  - Fixed size buttons with tall borders
  - On hover:
    - Brightens background color to give user feedback

- **Dark Theme Button Styles**
  - `#confirm_yes`: `#4CAF50` background, `#388E3C` border
  - `#confirm_no`: `#F44336` background, `#D32F2F` border
  - White text for contrast

- **Light Theme Button Styles**
  - `#confirm_yes`: `#388E3C` background, `#2E7D32` border
  - `#confirm_no`: `#D32F2F` background, `#C62828` border
  - White text for contrast

---

> **Note:** Uses `layout` attributes for fluid resizing in text-based environments.

> **Note:** Toggled via `.dark` or `.light` class on the root widget. Automatically propagates styling to relevant subcomponents.

> **Note:** `$success`, `$error`, `$panel`, `$accent`, and `$text` are symbolic tokens to map to project-wide color schemes.

> **Note:** Custom confirmation modal is purpose-built for clarity and accessibility with centered alignment, visual borders, and consistent color usage.

> **Note:** Styles are grouped logically and target unique IDs or class names—avoiding global overrides and improving maintainability.

---

## **Directory: `playground/`**

### **`playground.py`**

### **Overview**

> **Note:** The sole purpose of this file is to serve as a playground for testing and debugging code snippets. It is not intended for production use and should be excluded from any deployment or distribution.

---

## **Directory: `utils/`**

### **`exceptions.py`**

### **Overview**

Brief description of what this file is responsible for.

> **Note**: Functions prefixed with an underscore (`_`) are intended to be private and must not be accessed or invoked outside this directory. They are exclusively used internally by the corresponding public functions.
> 

### **Classes**

#### **class ExceptionName**

- **Attributes:**
    - `attr1 (type)`: What it represents.
- **Methods:**Document them just like functions.
- **Notes:**Anything about inheritance, expected usage, or limitations.

### **Constants / Globals**

List and briefly describe constants or config variables.

### **Usage Notes**

If there’s something unique about using this file/module, document it here.

---

### **`utility.py`**

### **Overview**

Brief description of what this file is responsible for.

> **Note**: Functions prefixed with an underscore (`_`) are intended to be private and must not be accessed or invoked outside this directory. They are exclusively used internally by the corresponding public functions.
> 

### **Functions**

#### **function_name(args)**

- **Args:**
    - `arg1 (type)`: Description.
    - `arg2 (type, optional)`: Description. Default is X.
- **Returns:**
    - (type): What the function returns.
- **Throws:**
    - ExceptionType: When it’s thrown and why.
- **Yields:**
    - (type): If it’s a generator, what it yields.
- **Brief:**One-sentence purpose of the function.
- **Notes:**Any implementation quirks, assumptions, or caveats.

### **Classes**

### **class ClassName**

- **Attributes:**
    - `attr1 (type)`: What it represents.
- **Methods:**Document them just like functions.
- **Notes:**Anything about inheritance, expected usage, or limitations.

### **Constants / Globals**

List and briefly describe constants or config variables.

### **Usage Notes**

If there’s something unique about using this file/module, document it here.

---

### **`logger.py`**

### **Overview**

This file defines and configures a reusable logging utility app. It enables color-coded console logs and persistent file logging with standardized formatting, timestamps, and log levels. It supports flexible integration into different modules by allowing toggling of console output and specification of log file destinations.

> **Note**: This logger setup uses the `colorlog` package to enable colored output in the console, improving readability during debugging. It supports both runtime and persistent logging behavior.

---

### **Functions**

#### **`def setup_logger(name: str, log_file: str = None, level: int = logging.DEBUG, enable_console = False) -> logging.Logger`**
- **Brief:** Initializes a logger with optional colored console output and/or file output. Prevents duplicate log propagation.

- **Args:**
  - `name (str)`: Identifier for the logger instance (typically the calling module’s `__name__`).
  - `log_file (str, optional)`: Relative name of the file to which logs should be written. If `None`, file logging is disabled. The log file will be created under `data/logs/` with a `log_` prefix.
  - `level (int, optional)`: Logging threshold. Defaults to `logging.DEBUG`, capturing all logs at `DEBUG` level and above.
  - `enable_console (bool, optional)`: Whether to enable colored logs in the console. Defaults to `False`.

- **Returns:**
  - `logging.Logger`: A fully configured Python `Logger` instance ready for use.


> **Note:** Prevents double logging by setting `logger.propagate = False`.

> **Note:** Ensures the `logs` directory exists before writing to file.

> **Note:** Automatically appends timestamps to each log entry.

> **Note:** Uses `LOG_COLORS` from [`core.constants`](#constantspy) to define log-level-specific colors.

> **Note:** File logs are not colored to maintain readability in text editors or automated systems.

---

### **Constants / Globals**

- **`LOG_COLORS (dict)`**  
  - Imported from `core.constants`.
  - Maps log levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`) to terminal-friendly color names for console output via `colorlog.ColoredFormatter`.

---

### **Usage**

- To use the logger in any module:
  ```python
  from logger import setup_logger
  logger = setup_logger(__name__, log_file="module_name.log", enable_console=True)
  logger.info("Logger initialized.")
  ```

- Log messages are consistently formatted as:
  ```
  2025-04-20 13:42:55 | INFO     | Logger initialized.
  ```

> **Note:** File logging is optional but recommended for debugging "historical" behavior.

> **Note:** Console output can be enabled for development and disabled in production or automated scripts.

> **Note:** This module prepends the `data/logs/` directory path to all log file names passed via `log_file`. Do **not** provide absolute paths.

> **Note:** Multiple handlers (console and file) are attached only if requested. No redundant handlers are created on repeated calls due to Python's `getLogger` behavior.

> **Note:** Timestamps follow the format `YYYY-MM-DD HH:MM:SS`.

> **Note:** Color coding applies only to console output and uses the configured mapping in `LOG_COLORS`.

---

## **Directory: `tests/`**

### **`Makefile`**

### **Overview**

This file automates the execution of test commands for the project. It defines shortcuts for running specific sets of tests—unit, system, or all—using consistent Pytest options. The Makefile streamlines repetitive tasks and ensures reproducibility across environments.

---

### **Targets**

- **`test-all`**  
  Runs both unit and system tests using Pytest.  
  - Output is verbose (`-vs`)  
  - Displays short tracebacks (`--tb=short`)  
  - Suppresses warnings (`--disable-warnings`)  
  - Stops after the first failure (`--maxfail=1`)  
  - Forces colored output (`--color=yes`)  
  - Runs `unit_tests.py` and `sys_test.py`

- **`unit`**  
  Runs only unit tests (i.e., tests not marked as system).  
  - Same Pytest flags as `test-all`  
  - Filter: `-m "not system"`  
  - File: `unit_tests.py`

- **`sys`**  
  Runs only system tests (i.e., tests marked with `@pytest.mark.system`).  
  - Same Pytest flags as above  
  - Filter: `-m "system"`  
  - File: `sys_test.py`

---

### **Usage Notes**

- Run targets from the root of the project directory using `make`, for example:
  
  ```bash
  make test-all
  make unit
  make sys
  ```

> **Note:** You can extend this file with additional targets like `lint`, `format`, or `clean` to support other dev workflows.

> **Note:** If Pytest or `make` is not installed, the commands will fail. Ensure your development environment is properly set up.

---

### **`unit_tests.py`**

### **Overview**

Brief description of what this file is responsible for.

### **Functions**

#### **test_function_name(args)**

- **Args:**
    - `arg1 (type)`: Description.
    - `arg2 (type, optional)`: Description. Default is X.
- **Returns:**
    - (type): What the function returns.
- **Throws:**
    - ExceptionType: When it’s thrown and why.
- **Brief:**One-sentence purpose of the test function.
- **Notes:**Any specific test cases or dependencies.

### **Classes**

### **class TestClassName**

- **Attributes:**
    - `attr1 (type)`: What it represents.
- **Methods:**Document them just like functions.
- **Notes:**Anything about test setup or scope.

### **Constants / Globals**

List and briefly describe constants or config variables.

### **Usage Notes**

If there’s something unique about using this file/module, document it here.

---

### **`sys_tests.py`**

### **Overview**

Brief description of what this file is responsible for.

### **Functions**

#### **test_function_name(args)**

- **Args:**
    - `arg1 (type)`: Description.
    - `arg2 (type, optional)`: Description. Default is X.
- **Returns:**
    - (type): What the function returns.
- **Throws:**
    - ExceptionType: When it’s thrown and why.
- **Brief:**One-sentence purpose of the test function.
- **Notes:**Any specific test cases or dependencies.

### **Classes**

### **class TestClassName**

- **Attributes:**
    - `attr1 (type)`: What it represents.
- **Methods:**Document them just like functions.
- **Notes:**Anything about test setup or scope.

### **Constants / Globals**

List and briefly describe constants or config variables.

### **Usage Notes**

If there’s something unique about using this file/module, document it here.

---

### **`test<n>.py`**

### Testing Overview

#### Directory Structure & File Usage

- **Files 01–10**: Test cases for **Long Method** detection  
- **Files 11–20**: Test cases for **Long Parameter List** detection  
- **Files 21–30**: Test cases for **Duplicated Code** detection  
- **Files 31–40**: Test cases for **Refactoring Long Methods**  
- **Files 31–40**: (Overlap) Also used for **Refactoring** scenarios
- **File 41**: Larger file used to test all 3
- **File 42**: Java file used to test the system's ability to handle non-Python files

#### Project Tree

```
.
├── Makefile
├── README.md
├── __pycache__
│   ├── conftest.cpython-312-pytest-8.3.5.pyc
│   ├── sys_test.cpython-312-pytest-8.3.5.pyc
│   └── unit_tests.cpython-312-pytest-8.3.5.pyc
├── conftest.py
├── out
│   └── test_log.log
├── pytest.ini
├── sys_test.py
├── test1.py
├── test10.py
├── test11.py
├── test12.py
├── test13.py
├── test14.py
├── test15.py
├── test16.py
├── test17.py
├── test18.py
├── test19.py
├── test2.py
├── test20.py
├── test21.py
├── test22.py
├── test23.py
├── test24.py
├── test25.py
├── test26.py
├── test27.py
├── test28.py
├── test29.py
├── test3.py
├── test30.py
├── test31.py
├── test32.py
├── test33.py
├── test34.py
├── test35.py
├── test36.py
├── test37.py
├── test38.py
├── test39.py
├── test4.py
├── test40.py
├── test41.py
├── test42.java
├── test43.py
├── test44.py
├── test5.py
├── test6.py
├── test7.py
├── test8.py
├── test9.py
└── unit_tests.py
```

---

### **`pytest.ini`**

### **Overview**

This file defines global configuration settings for `Pytest`. It controls test behavior, fixtures, and categorization for the app. The file ensures consistent test execution and enables advanced `Pytest` features such as `asyncio` support and custom markers.

---

### **Configuration**

- **`asyncio_mode = auto`**  
  - Automatically selects the appropriate asyncio mode for tests using async code. Ensures compatibility with Python’s async event loop during test execution.

- **`asyncio_default_fixture_loop_scope = function`**  
  - Sets the default lifecycle scope of the asyncio event loop fixture to **function** level. A new loop is created for each test function to isolate state and avoid leakage between tests.

- **`markers`**  
  - Custom test markers defined for categorizing and filtering tests:
  
    -   `long_method`: Tests for identifying long methods in code.
    -   `long_param`: Tests for detecting functions with too many parameters.
    -   `duplicated_code`: Tests focused on detecting and handling code duplication.
    -   `refactor`: Tests targeting automated code refactoring features.

---

### **Usage Notes**

- To run only a specific category of tests, use the `-m` flag. For example:
  
  ```bash
  pytest -m duplicated_code
  ```

> **Note:** Pytest will issue warnings or errors if tests use markers not defined here. This file registers all custom markers to avoid that.

> **Note:** Async test functions (`async def`) will work without needing manual event loop setup.

> **Note:** Fixture scoping for asyncio can be overridden manually in tests but defaults to per-function isolation for safety.

---

### **`conftest.py`**

### **Overview**

This file configures Pytest behavior for the app's test suite. It adds rich console output with theming, reorders and categorizes test displays, and prints styled summaries to enhance readability and developer experience during testing. This configuration enhances how Pytest outputs test collection, results, and summaries.

---

### **Functions**

#### **`pytest_collection_modifyitems(config, items)`**

- **Brief:** Reorders tests so that unit tests run before system tests, and displays them under themed headings in the terminal.

- **Args:**
  - `config (_type_)`: The Pytest configuration object.
  - `items (_type_)`: List of test items collected by Pytest.

> **Note:** Uses `rich.console.Console` to pretty-print test names grouped by type. It inspects the `keywords` of each test item to determine its category.

---

#### **`pytest_runtest_logreport(report)`**

- **Brief:** Logs the result of each test case immediately after it's executed using themed formatting.

- **Args:**
  - `report (_type_)`: The Pytest test report object for an individual test call.

> **Note:** This only processes the `call` phase (not setup/teardown). Emoji and color-coding indicate pass, skip, and fail states.

---

#### **`_display_test_item(item)`**
- **Brief:** Pretty-prints the file and function name of a test using rich formatting.
- **Args:**
  - `item (_type_)`: A single collected Pytest test item.

> **Note:** This is a helper function used internally by `pytest_collection_modifyitems`. Not registered as a Pytest hook.

---

#### **`pytest_terminal_summary(terminalreporter, exitstatus, config)`**
- **Brief:** Displays a summary of test results at the end of the test run with color-coded status counts.

- **Args:**
  - `terminalreporter (_type_)`: The Pytest terminal reporter.
  - `exitstatus (_type_)`: Exit code of the test session.
  - `config (_type_)`: The Pytest configuration object.

> **Note:** Prints total counts for passed, skipped, failed, and errored tests. Ends with a themed footer.

---

### **Constants / Globals**

- **`custom_theme (Theme)`**  
  - A `rich.theme.Theme` object defining custom text styles for headings, test names, skip/warn, and fail statuses.

- **`console (Console)`**  
  - A `rich.console.Console` instance initialized with the `custom_theme`, used for all styled output during test collection and execution.

---

### **Usage Notes**

- Output includes:
  - Themed section headers (unit vs system)
  - Per-test result icons (`✅`, `❌`, `🟡`)
  - A final summary table
  - Emojis are terminal-safe and chosen to enhance UX

> **Note:** This file is automatically loaded by Pytest when placed at the root of the test directory or project.

> **Note:** To categorize a test as a system test, add the `@pytest.mark.system` decorator.

> **Note:** Unit tests (i.e., those without `unit` or `system` markers) are printed and run first by design.


> **Note:** No additional imports or setup required when running `pytest`.

---

### **`duplicated_code_guide.md`**

### **Overview**

This file is a guide I developed before diving into the development of a refactoring tool. It includes a list of all known types, their definitions, and examples. It serves as a reference for understanding the types of code smells that the tool aims to address.

> **Note:** This guide is not intended to be exhaustive or definitive. It is a living document that I hope will evolve as the tool and its capabilities are developed further.

---

## **Directory: Project Root**

### **`README.md`**

### **Overview**

This file provides an overview of the project, including its purpose, features, and how to set it up.

---

### **`requirements.txt`**

### **Overview**

This file lists the Python packages required for the project, along with their versions.

> **Note:** Run `pip install -r requirements.txt` to install all dependencies.

---

### **`LICENSE`**

### **Overview**

MIT License

### **License Details**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Written by *Jakob Balkovec*