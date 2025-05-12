# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sun Apr 20th, 2025
#
# __file__: conftest.py
#
# __brief__: This file contains the configuration for pytest and the test suite.

# =========
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# =========

import pytest
from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({
    "heading": "bold bright_cyan",
    "test_name": "italic green",
    "skip": "dim yellow",
    "fail": "bold bright_red",
})
console = Console(theme=custom_theme)

def pytest_collection_modifyitems(config, items):
    """_summary_

    Args:
        config (_type_): config object
        items (_type_): list of test items
    """
    unit_tests = [item for item in items if "unit" not in item.keywords and "system" not in item.keywords]
    sys_tests = [item for item in items if "system" in item.keywords]

    if unit_tests:
        console.print("[heading]\n🛠️ --- Unit Tests --- 🧪[/heading]")
        for item in unit_tests:
            _display_test_item(item)

    if sys_tests:
        console.print("[heading]\n⚙️ --- System Tests --- 🚀[/heading]")
        for item in sys_tests:
            _display_test_item(item)
            
    items[:] = unit_tests + sys_tests

def pytest_runtest_logreport(report):
    """_summary_

    Args:
        report (_type_): report object
    """
    if report.when == "call": 
        if report.passed:
            console.print(f"[test_name]✅ {report.nodeid.split('::')[-1]}[/test_name]", end="  ")
        elif report.skipped:
            console.print(f"[skip]🟡 Skipped: {report.nodeid.split('::')[-1]}[/skip]", end="  ")
        elif report.failed:
            console.print(f"[fail]❌ Failed: {report.nodeid.split('::')[-1]}[/fail]", end="  ")

def _display_test_item(item):
    """_summary_

    Args:
        item (_type_): test item
    """
    test_name_parts = item.nodeid.split("::")
    file_name = test_name_parts[0]
    test_function_or_class = test_name_parts[-1]
    console.print(f"  [test_name]📄 {file_name} :: {test_function_or_class}[/test_name]")


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """_summary_

    Args:
        terminalreporter (_type_): reporter object
        exitstatus (_type_): exit status
        config (_type_): config object
    """
    console.print("[heading]\n📊 --- Test Summary --- 📊[/heading]")
    if terminalreporter.stats.get("passed"):
        num_passed = len(terminalreporter.stats["passed"])
        console.print(f"[green]✅ Passed:[/green] {num_passed}", end="  ")
    if terminalreporter.stats.get("skipped"):
        num_skipped = len(terminalreporter.stats["skipped"])
        console.print(f"[yellow]🟡 Skipped:[/yellow] {num_skipped}", end="  ")
    if terminalreporter.stats.get("failed"):
        num_failed = len(terminalreporter.stats["failed"])
        console.print(f"[bold red]❌ Failed:[/bold red] {num_failed}", end="  ")
    if terminalreporter.stats.get("error"):
        num_error = len(terminalreporter.stats["error"])
        console.print(f"[bold bright_red]🚨 Errors:[/bold bright_red] {num_error}")
        
    console.print("\n[heading]🔚 --- End of Test Report --- 🔚\n\n[/heading]")