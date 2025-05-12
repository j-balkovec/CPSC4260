# Documentation

**Project Name**: Code Smell App  
**Class**: CPSC 4260 - Software Refactoring  
**Name**: Jakob Balkovec  
**Date**: May 11, 2025  

This document provides comprehensive documentation for the **CodeSmellApp** project, detailing each module, class, and function. It serves as a guide for users, developers, and evaluators to understand the codebase, its functionality, and its structure.

## Project Structure

The following outlines the key files and directories in the **CodeSmellApp** repository, organized by directory with brief descriptions of each file's purpose.

- [**Directory: `core/`**](#directory-core)
  - [`code_metrics.py`](#file-code-metricspy): Calculates code quality metrics for analysis.
  - [`code_smells.py`](#file-code-smellspy): Detects code smells in Python files.
  - [`constants.py`](#file-constantspy): Defines constants used across the application.
  - [`duplicated_finder.py`](#file-duplicated-finderpy): Identifies duplicated code segments.
  - [`file_info_extractor.py`](#file-file-info-extractorpy): Extracts metadata from source files.
  - [`file_saver.py`](#file-file-saverpy): Handles saving refactored code to files.
  - [`halstead.py`](#file-halsteadpy): Computes Halstead complexity metrics.
  - [`method_length.py`](#file-method-lengthpy): Analyzes method length for code smell detection.
  - [`param_length.py`](#file-param-lengthpy): Evaluates parameter list lengths in functions.
  - [`refactor.py`](#file-refactorpy): Performs code refactoring, such as removing duplicates.
<br>

- [**Directory: `gui/`**](#directory-gui)
  - [`new_ui.py`](#file-new-uipy): Implements the main Textual-based GUI for the app.
  - [`terminal_ui.py`](#file-terminal-uipy): Provides a terminal-based UI alternative.
  - [`textual_ui.css`](#file-textual-uicss): CSS styles for the Textual GUI.
<br>

- [**Directory: `playground/`**](#directory-playground)
  - [`playground.py`](#file-playgroundpy): Experimental scripts for testing and prototyping.
<br>

- [**Directory: `utils/`**](#directory-utils)
  - [`exceptions.py`](#file-exceptionspy): Defines custom exceptions for the application.
  - [`utility.py`](#file-utilitypy): Utility functions for file operations and helpers.
  - [`logger.py`](#file-loggerpy): Configures logging for the application.
<br>

- [**Directory: `tests/`**](#directory-tests)
  - [`Makefile`](#file-makefile): Build script for running tests and other tasks.
  - [`unit_tests.py`](#file-unit-testspy): Unit tests for individual components.
  - [`sys_tests.py`](#file-sys-testspy): System-level integration tests.
  - [`test<n>.py`](#file-testnpy): Additional test files (e.g., `test1.py`, `test2.py`).
  - [`pytest.ini`](#file-pytestini): Configuration file for pytest.
  - [`conftest.py`](#file-conftestpy): Pytest fixtures and setup for testing.
<br>

- [**Directory: `docs/`**](#directory-docs)
  - [`DOCUMENTATION.md`](#file-documentationmd): This documentation file.
  - [`duplicated_code_guide.md`](#file-duplicated-code-guidemd): Guide for understanding duplicated code detection.
<br>

- [**Directory: Project Root**](#directory-project-root)
  - [`README.md`](#file-readmemd): Project overview and setup instructions.
  - [`requirements.txt`](#file-requirementstxt): Python package dependencies.
  - [`LICENSE`](#file-license): License information for the project.
<br>

---

## Directory: `core/`

### `code_metrics.py`

#### Overview
Brief description of what this file is responsible for.

#### Functions

##### function_name(args)
- **Args:**
  - `arg1 (type)`: Description.
  - `arg2 (type, optional)`: Description. Default is X.
- **Returns:**
  - (type): What the function returns.
- **Throws:**
  - ExceptionType: When it’s thrown and why.
- **Yields:**
  - (type): If it’s a generator, what it yields.
- **Brief:**
  One-sentence purpose of the function.
- **Notes:**
  Any implementation quirks, assumptions, or caveats.

#### Classes

##### class ClassName
- **Attributes:**
  - `attr1 (type)`: What it represents.
- **Methods:**
  Document them just like functions.
- **Notes:**
  Anything about inheritance, expected usage, or limitations.

#### Constants / Globals
List and briefly describe constants or config variables.

#### Usage Notes
If there’s something unique about using this file/module, document it here.

---

### `code_smells.py`

#### Overview
Brief description of what this file is responsible for.

#### Functions

##### function_name(args)
- **Args:**
  - `arg1 (type)`: Description.
  - `arg2 (type, optional)`: Description. Default is X.
- **Returns:**
  - (type): What the function returns.
- **Throws:**
  - ExceptionType: When it’s thrown and why.
- **Yields:**
  - (type): If it’s a generator, what it yields.
- **Brief:**
  One-sentence purpose of the function.
- **Notes:**
  Any implementation quirks, assumptions, or caveats.

#### Classes

##### class ClassName
- **Attributes:**
  - `attr1 (type)`: What it represents.
- **Methods:**
  Document them just like functions.
- **Notes:**
  Anything about inheritance, expected usage, or limitations.

#### Constants / Globals
List and briefly describe constants or config variables.

#### Usage Notes
If there’s something unique about using this file/module, document it here.

---

### `constants.py`

#### Overview
Brief description of what this file is responsible for.

#### Constants / Globals
List and briefly describe constants or config variables.

#### Usage Notes
If there’s something unique about using this file/module, document it here.

---

### `duplicated_finder.py`

#### Overview
Brief description of what this file is responsible for.

#### Functions

##### function_name(args)
- **Args:**
  - `arg1 (type)`: Description.
  - `arg2 (type, optional)`: Description. Default is X.
- **Returns:**
  - (type): What the function returns.
- **Throws:**
  - ExceptionType: When it’s thrown and why.
- **Yields:**
  - (type): If it’s a generator, what it yields.
- **Brief:**
  One-sentence purpose of the function.
- **Notes:**
  Any implementation quirks, assumptions, or caveats.

#### Classes

##### class ClassName
- **Attributes:**
  - `attr1 (type)`: What it represents.
- **Methods:**
  Document them just like functions.
- **Notes:**
  Anything about inheritance, expected usage, or limitations.

#### Constants / Globals
List and briefly describe constants or config variables.

#### Usage Notes
If there’s something unique about using this file/module, document it here.

---

### `file_info_extractor.py`

#### Overview
Brief description of what this file is responsible for.

#### Functions

##### function_name(args)
- **Args:**
  - `arg1 (type)`: Description.
  - `arg2 (type, optional)`: Description. Default is X.
- **Returns:**
  - (type): What the function returns.
- **Throws:**
  - ExceptionType: When it’s thrown and why.
- **Yields:**
  - (type): If it’s a generator, what it yields.
- **Brief:**
  One-sentence purpose of the function.
- **Notes:**
  Any implementation quirks, assumptions, or caveats.

#### Classes

##### class ClassName
- **Attributes:**
  - `attr1 (type)`: What it represents.
- **Methods:**
  Document them just like functions.
- **Notes:**
  Anything about inheritance, expected usage, or limitations.

#### Constants / Globals
List and briefly describe constants or config variables.

#### Usage Notes
If there’s something unique about using this file/module, document it here.

---

### `file_saver.py`

#### Overview
Brief description of what this file is responsible for.

#### Functions

##### function_name(args)
- **Args:**
  - `arg1 (type)`: Description.
  - `arg2 (type, optional)`: Description. Default is X.
- **Returns:**
  - (type): What the function returns.
- **Throws:**
  - ExceptionType: When it’s thrown and why.
- **Yields:**
  - (type): If it’s a generator, what it yields.
- **Brief:**
  One-sentence purpose of the function.
- **Notes:**
  Any implementation quirks, assumptions, or caveats.

#### Classes

##### class ClassName
- **Attributes:**
  - `attr1 (type)`: What it represents.
- **Methods:**
  Document them just like functions.
- **Notes:**
  Anything about inheritance, expected usage, or limitations.

#### Constants / Globals
List and briefly describe constants or config variables.

#### Usage Notes
If there’s something unique about using this file/module, document it here.

---

### `halstead.py`

#### Overview
Brief description of what this file is responsible for.

#### Functions

##### function_name(args)
- **Args:**
  - `arg1 (type)`: Description.
  - `arg2 (type, optional)`: Description. Default is X.
- **Returns:**
  - (type): What the function returns.
- **Throws:**
  - ExceptionType: When it’s thrown and why.
- **Yields:**
  - (type): If it’s a generator, what it yields.
- **Brief:**
  One-sentence purpose of the function.
- **Notes:**
  Any implementation quirks, assumptions, or caveats.

#### Classes

##### class ClassName
- **Attributes:**
  - `attr1 (type)`: What it represents.
- **Methods:**
  Document them just like functions.
- **Notes:**
  Anything about inheritance, expected usage, or limitations.

#### Constants / Globals
List and briefly describe constants or config variables.

#### Usage Notes
If there’s something unique about using this file/module, document it here.

---

### `method_length.py`

#### Overview
Brief description of what this file is responsible for.

#### Functions

##### function_name(args)
- **Args:**
  - `arg1 (type)`: Description.
  - `arg2 (type, optional)`: Description. Default is X.
- **Returns:**
  - (type): What the function returns.
- **Throws:**
  - ExceptionType: When it’s thrown and why.
- **Yields:**
  - (type): If it’s a generator, what it yields.
- **Brief:**
  One-sentence purpose of the function.
- **Notes:**
  Any implementation quirks, assumptions, or caveats.

#### Classes

##### class ClassName
- **Attributes:**
  - `attr1 (type)`: What it represents.
- **Methods:**
  Document them just like functions.
- **Notes:**
  Anything about inheritance, expected usage, or limitations.

#### Constants / Globals
List and briefly describe constants or config variables.

#### Usage Notes
If there’s something unique about using this file/module, document it here.

---

### `param_length.py`

#### Overview
Brief description of what this file is responsible for.

#### Functions

##### function_name(args)
- **Args:**
  - `arg1 (type)`: Description.
  - `arg2 (type, optional)`: Description. Default is X.
- **Returns:**
  - (type): What the function returns.
- **Throws:**
  - ExceptionType: When it’s thrown and why.
- **Yields:**
  - (type): If it’s a generator, what it yields.
- **Brief:**
  One-sentence purpose of the function.
- **Notes:**
  Any implementation quirks, assumptions, or caveats.

#### Classes

##### class ClassName
- **Attributes:**
  - `attr1 (type)`: What it represents.
- **Methods:**
  Document them just like functions.
- **Notes:**
  Anything about inheritance, expected usage, or limitations.

#### Constants / Globals
List and briefly describe constants or config variables.

#### Usage Notes
If there’s something unique about using this file/module, document it here.

---

### `refactor.py`

#### Overview
Brief description of what this file is responsible for.

#### Functions

##### function_name(args)
- **Args:**
  - `arg1 (type)`: Description.
  - `arg2 (type, optional)`: Description. Default is X.
- **Returns:**
  - (type): What the function returns.
- **Throws:**
  - ExceptionType: When it’s thrown and why.
- **Yields:**
  - (type): If it’s a generator, what it yields.
- **Brief:**
  One-sentence purpose of the function.
- **Notes:**
  Any implementation quirks, assumptions, or caveats.

#### Classes

##### class ClassName
- **Attributes:**
  - `attr1 (type)`: What it represents.
- **Methods:**
  Document them just like functions.
- **Notes:**
  Anything about inheritance, expected usage, or limitations.

#### Constants / Globals
List and briefly describe constants or config variables.

#### Usage Notes
If there’s something unique about using this file/module, document it here.

---

## Directory: `gui/`

### `new_ui.py`

#### Overview
Brief description of what this file is responsible for.

#### Functions

##### function_name(args)
- **Args:**
  - `arg1 (type)`: Description.
  - `arg2 (type, optional)`: Description. Default is X.
- **Returns:**
  - (type): What the function returns.
- **Throws:**
  - ExceptionType: When it’s thrown and why.
- **Yields:**
  - (type): If it’s a generator, what it yields.
- **Brief:**
  One-sentence purpose of the function.
- **Notes:**
  Any implementation quirks, assumptions, or caveats.

#### Classes

##### class ClassName
- **Attributes:**
  - `attr1 (type)`: What it represents.
- **Methods:**
  Document them just like functions.
- **Notes:**
  Anything about inheritance, expected usage, or limitations.

#### Constants / Globals
List and briefly describe constants or config variables.

#### Usage Notes
If there’s something unique about using this file/module, document it here.

---

### `terminal_ui.py`

#### Overview
Brief description of what this file is responsible for.

#### Functions

##### function_name(args)
- **Args:**
  - `arg1 (type)`: Description.
  - `arg2 (type, optional)`: Description. Default is X.
- **Returns:**
  - (type): What the function returns.
- **Throws:**
  - ExceptionType: When it’s thrown and why.
- **Yields:**
  - (type): If it’s a generator, what it yields.
- **Brief:**
  One-sentence purpose of the function.
- **Notes:**
  Any implementation quirks, assumptions, or caveats.

#### Classes

##### class ClassName
- **Attributes:**
  - `attr1 (type)`: What it represents.
- **Methods:**
  Document them just like functions.
- **Notes:**
  Anything about inheritance, expected usage, or limitations.

#### Constants / Globals
List and briefly describe constants or config variables.

#### Usage Notes
If there’s something unique about using this file/module, document it here.

---

### `textual_ui.css`

#### Overview
Brief description of what this file is responsible for.

#### Styles
List and briefly describe CSS classes or rules.

#### Usage Notes
If there’s something unique about using this file, document it here.

---

## Directory: `playground/`

### `playground.py`

#### Overview
Brief description of what this file is responsible for.

#### Functions

##### function_name(args)
- **Args:**
  - `arg1 (type)`: Description.
  - `arg2 (type, optional)`: Description. Default is X.
- **Returns:**
  - (type): What the function returns.
- **Throws:**
  - ExceptionType: When it’s thrown and why.
- **Yields:**
  - (type): If it’s a generator, what it yields.
- **Brief:**
  One-sentence purpose of the function.
- **Notes:**
  Any implementation quirks, assumptions, or caveats.

#### Classes

##### class ClassName
- **Attributes:**
  - `attr1 (type)`: What it represents.
- **Methods:**
  Document them just.Concurrent users like functions.
- **Notes:**
  Anything about inheritance, expected usage, or limitations.

#### Constants / Globals
List and briefly describe constants or config variables.

#### Usage Notes
If there’s something unique about using this file/module, document it here.

---

## Directory: `utils/`

### `exceptions.py`

#### Overview
Brief description of what this file is responsible for.

#### Classes

##### class ExceptionName
- **Attributes:**
  - `attr1 (type)`: What it represents.
- **Methods:**
  Document them just like functions.
- **Notes:**
  Anything about inheritance, expected usage, or limitations.

#### Constants / Globals
List and briefly describe constants or config variables.

#### Usage Notes
If there’s something unique about using this file/module, document it here.

---

### `utility.py`

#### Overview
Brief description of what this file is responsible for.

#### Functions

##### function_name(args)
- **Args:**
  - `arg1 (type)`: Description.
  - `arg2 (type, optional)`: Description. Default is X.
- **Returns:**
  - (type): What the function returns.
- **Throws:**
  - ExceptionType: When it’s thrown and why.
- **Yields:**
  - (type): If it’s a generator, what it yields.
- **Brief:**
  One-sentence purpose of the function.
- **Notes:**
  Any implementation quirks, assumptions, or caveats.

#### Classes

##### class ClassName
- **Attributes:**
  - `attr1 (type)`: What it represents.
- **Methods:**
  Document them just like functions.
- **Notes:**
  Anything about inheritance, expected usage, or limitations.

#### Constants / Globals
List and briefly describe constants or config variables.

#### Usage Notes
If there’s something unique about using this file/module, document it here.

---

### `logger.py`

#### Overview
Brief description of what this file is responsible for.

#### Functions

##### function_name(args)
- **Args:**
  - `arg1 (type)`: Description.
  - `arg2 (type, optional)`: Description. Default is X.
- **Returns:**
  - (type): What the function returns.
- **Throws:**
  - ExceptionType: When it’s thrown and why.
- **Yields:**
  - (type): If it’s a generator, what it yields.
- **Brief:**
  One-sentence purpose of the function.
- **Notes:**
  Any implementation quirks, assumptions, or caveats.

#### Classes

##### class ClassName
- **Attributes:**
  - `attr1 (type)`: What it represents.
- **Methods:**
  Document them just like functions.
- **Notes:**
  Anything about inheritance, expected usage, or limitations.

#### Constants / Globals
List and briefly describe constants or config variables.

#### Usage Notes
If there’s something unique about using this file/module, document it here.

---

## Directory: `tests/`

### `Makefile`

#### Overview
Brief description of what this file is responsible for.

#### Targets
List and briefly describe Makefile targets (e.g., `test`, `clean`).

#### Usage Notes
If there’s something unique about using this file, document it here.

---

### `unit_tests.py`

#### Overview
Brief description of what this file is responsible for.

#### Functions

##### test_function_name(args)
- **Args:**
  - `arg1 (type)`: Description.
  - `arg2 (type, optional)`: Description. Default is X.
- **Returns:**
  - (type): What the function returns.
- **Throws:**
  - ExceptionType: When it’s thrown and why.
- **Brief:**
  One-sentence purpose of the test function.
- **Notes:**
  Any specific test cases or dependencies.

#### Classes

##### class TestClassName
- **Attributes:**
  - `attr1 (type)`: What it represents.
- **Methods:**
  Document them just like functions.
- **Notes:**
  Anything about test setup or scope.

#### Constants / Globals
List and briefly describe constants or config variables.

#### Usage Notes
If there’s something unique about using this file/module, document it here.

---

### `sys_tests.py`

#### Overview
Brief description of what this file is responsible for.

#### Functions

##### test_function_name(args)
- **Args:**
  - `arg1 (type)`: Description.
  - `arg2 (type, optional)`: Description. Default is X.
- **Returns:**
  - (type): What the function returns.
- **Throws:**
  - ExceptionType: When it’s thrown and why.
- **Brief:**
  One-sentence purpose of the test function.
- **Notes:**
  Any specific test cases or dependencies.

#### Classes

##### class TestClassName
- **Attributes:**
  - `attr1 (type)`: What it represents.
- **Methods:**
  Document them just like functions.
- **Notes:**
  Anything about test setup or scope.

#### Constants / Globals
List and briefly describe constants or config variables.

#### Usage Notes
If there’s something unique about using this file/module, document it here.

---

### `test<n>.py`

#### Overview
Brief description of what this file is responsible for (e.g., specific test cases).

#### Functions

##### test_function_name(args)
- **Args:**
  - `arg1 (type)`: Description.
  - `arg2 (type, optional)`: Description. Default is X.
- **Returns:**
  - (type): What the function returns.
- **Throws:**
  - ExceptionType: When it’s thrown and why.
- **Brief:**
  One-sentence purpose of the test function.
- **Notes:**
  Any specific test cases or dependencies.

#### Classes

##### class TestClassName
- **Attributes:**
  - `attr1 (type)`: What it represents.
- **Methods:**
  Document them just like functions.
- **Notes:**
  Anything about test setup or scope.

#### Constants / Globals
List and briefly describe constants or config variables.

#### Usage Notes
If there’s something unique about using this file/module, document it here.

---

### `pytest.ini`

#### Overview
Brief description of what this file is responsible for.

#### Configuration
List and briefly describe pytest configuration settings.

#### Usage Notes
If there’s something unique about using this file, document it here.

---

### `conftest.py`

#### Overview
Brief description of what this file is responsible for.

#### Functions

##### fixture_name(args)
- **Args:**
  - `arg1 (type)`: Description.
  - `arg2 (type, optional)`: Description. Default is X.
- **Returns:**
  - (type): What the fixture returns.
- **Brief:**
  One-sentence purpose of the fixture.
- **Notes:**
  Any specific setup or scope.

#### Constants / Globals
List and briefly describe constants or config variables.

#### Usage Notes
If there’s something unique about using this file/module, document it here.

---

## Directory: `docs/`

### `DOCUMENTATION.md`

#### Overview
Brief description of what this file is responsible for.

#### Sections
List and briefly describe the main sections of the documentation.

#### Usage Notes
If there’s something unique about using this file, document it here.

---

### `duplicated_code_guide.md`

#### Overview
Brief description of what this file is responsible for.

#### Sections
List and briefly describe the main sections of the guide.

#### Usage Notes
If there’s something unique about using this file, document it here.

---

## Directory: Project Root

### `README.md`

#### Overview
Brief description of what this file is responsible for.

#### Sections
List and briefly describe the main sections of the README.

#### Usage Notes
If there’s something unique about using this file, document it here.

---

### `requirements.txt`

#### Overview
Brief description of what this file is responsible for.

#### Dependencies
List and briefly describe the Python packages required.

#### Usage Notes
If there’s something unique about using this file, document it here.

---

### `LICENSE`

#### Overview
Brief description of what this file is responsible for.

#### License Details
Briefly describe the license type and key terms.

#### Usage Notes
If there’s something unique about using this file, document it here.

---