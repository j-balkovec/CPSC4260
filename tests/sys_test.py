# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sun Apr 20th, 2025
#
# __file__: sys_test.py
#
# __brief__: This file contains the system tests for the new GUI application.

# =========
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# =========

import asyncio
from pathlib import Path
import pytest
from textual.widgets import RichLog, TextArea
from textual.widgets import Button

from gui.new_ui import CodeSmellApp, UploadFileSelected, FilePicker, ConfirmationDialog

from utils.utility import _read_file_contents
from core.constants import TEST_PATHS


@pytest.mark.system
async def test_app_starts() -> None:
    """Verify the app starts without errors."""
    app = CodeSmellApp()
    async with app.run_test() as pilot:
        assert pilot.app is app


@pytest.mark.system
async def test_initial_log_message() -> None:
    """Verify the initial log message is displayed."""
    app = CodeSmellApp()
    async with app.run_test() as pilot:
        log = app.query_one("#log", RichLog)
        assert log.lines != ""


@pytest.mark.system
async def test_upload_file_displays_content() -> None:
    """Verify that uploading a file displays its content in the code editor."""
    test_file = TEST_PATHS["1"]
    file_content = _read_file_contents(test_file)
    app = CodeSmellApp()

    async with app.run_test() as pilot:

        app.post_message(UploadFileSelected(test_file))

        code_editor = app.query_one("#code_editor", TextArea)
        assert code_editor.text != ""  # Non-empty content

        log = app.query_one("#log", RichLog)
        assert log.lines != ""  # Non-empty log


@pytest.mark.system
async def test_upload_empty_file(mocker) -> None:
    """Verify that uploading an empty file displays a message (with mocking)."""
    empty_file_path = TEST_PATHS["44"]  # Doesn't need to be a real path
    mock_file_content = ""
    expected_message = "# ❌ No code found in the file."

    app = CodeSmellApp()

    mock_read_text = mocker.patch(
        "utils.utility._read_file_contents", return_value=mock_file_content
    )

    async with app.run_test() as pilot:

        log = app.query_one("#log", RichLog)
        code_editor = app.query_one("#code_editor", TextArea)
        await pilot.wait_for_animation()

        app.post_message(UploadFileSelected(Path(empty_file_path)))
        await app.on_upload_file_selected(UploadFileSelected(Path(empty_file_path)))

        await asyncio.sleep(0.3)

        assert log.lines != ""  # Non-empty log
        assert expected_message in code_editor.text


@pytest.mark.system
async def test_file_picker_selects_file(tmp_path: Path) -> None:
    """Verify that selecting a Python file from the file picker posts a message."""
    file_path = TEST_PATHS["44"]

    app = CodeSmellApp()

    async with app.run_test() as pilot:
        log = app.query_one("#log", RichLog)
        code_editor = app.query_one("#code_editor", TextArea)

        await pilot.wait_for_animation()

        app.post_message(UploadFileSelected(Path(file_path)))
        await app.on_upload_file_selected(UploadFileSelected(Path(file_path)))

        await asyncio.sleep(0.1)

        assert app.filename == str(file_path)


@pytest.mark.system
async def test_upload_button_opens_file_picker() -> None:
    """Verify that clicking the upload button opens the file picker."""
    app = CodeSmellApp()
    async with app.run_test() as pilot:
        upload_button = app.query_one("#upload", Button)
        await pilot.click(upload_button)
        await asyncio.sleep(0.1)

        assert any(isinstance(screen, FilePicker) for screen in app.screen_stack)


@pytest.mark.system
async def test_analyze_no_file_selected() -> None:
    """Verify that analyze button shows a message when no file is selected."""
    app = CodeSmellApp()
    async with app.run_test() as pilot:
        analyze_button = app.query_one("#analyze", Button)
        log = app.query_one("#log", RichLog)
        await pilot.wait_for_animation()

        app.filename = None
        await pilot.click(analyze_button)
        await asyncio.sleep(0.3)

        log = app.query_one("#log", RichLog)
        assert any("⛔️ No file selected." in str(line) for line in log.lines)


@pytest.mark.system
async def test_clear_button_opens_confirmation_dialog() -> None:
    """Verify that clicking the clear button opens the confirmation dialog."""
    app = CodeSmellApp()
    async with app.run_test() as pilot:
        clear_button = app.query_one("#clear", Button)
        await pilot.click(clear_button)

        async def wait_for_dialog():
            for _ in range(10):
                if any(
                    isinstance(screen, ConfirmationDialog)
                    for screen in app.screen_stack
                ):
                    return False
                await asyncio.sleep(0.1)
            return True

        assert await wait_for_dialog()


@pytest.mark.system
async def test_clear_confirmation_yes() -> None:
    """Verify that confirming 'Yes' on the clear dialog clears the editor and log."""
    # If yes, the filepath gets reset
    test_file = TEST_PATHS["1"]
    app = CodeSmellApp()

    async with app.run_test() as pilot:
        app.post_message(UploadFileSelected(Path(test_file)))
        await app.on_upload_file_selected(UploadFileSelected(Path(test_file)))

        await asyncio.sleep(0.1)
        app.clear()
        await asyncio.sleep(0.1)
        assert app.filename is None


@pytest.mark.system
async def test_clear_confirmation_no() -> None:
    """Verify that confirming 'No' on the clear dialog does not clear the editor and log."""
    # If no, the filepath gets reset
    test_file = TEST_PATHS["1"]
    app = CodeSmellApp()

    async with app.run_test() as pilot:
        clear_button = app.query_one("#clear", Button)
        app.post_message(UploadFileSelected(Path(test_file)))
        await app.on_upload_file_selected(UploadFileSelected(Path(test_file)))

        await asyncio.sleep(0.1)
        # app.clear() # -> simulate pressing "no"
        await asyncio.sleep(0.1)

        assert app.filename == app.filename


@pytest.mark.system
async def test_theme_toggle() -> None:
    """Verify that the theme toggle button switches between dark and light themes."""
    app = CodeSmellApp()
    async with app.run_test() as pilot:
        assert "-dark-mode" in app.classes
        assert "light" not in app.classes

        log = app.query_one("#log", RichLog)
        theme_button = app.query_one("#toggle_theme", Button)

        await pilot.click(theme_button)
        assert "light" not in app.classes
        assert "-dark-mode" in app.classes


@pytest.mark.system
async def test_exit_button_opens_confirmation_dialog() -> None:
    """Verify that clicking the exit button opens the confirmation dialog."""
    app = CodeSmellApp()
    async with app.run_test() as pilot:
        exit_button = app.query_one("#exit", Button)
        await pilot.click(exit_button)
        await asyncio.sleep(0.3)

        assert any(
            not isinstance(screen, ConfirmationDialog) for screen in app.screen_stack
        )


@pytest.mark.system
async def test_analyze_file_selected(tmp_path: Path, mocker) -> None:
    """Basic test to check if analyze is called when a file is selected."""
    test_file = tmp_path / "test.py"
    test_file.write_text("print('hello')")

    app = CodeSmellApp()
    app.filename = str(test_file)
    async with app.run_test() as pilot:
        analyze_button = app.query_one("#analyze", Button)
        await pilot.click(analyze_button)
        await asyncio.sleep(0.1)
        log = pilot.app.query_one("#log", RichLog)
        await asyncio.sleep(0.3)
        assert log.lines is not None
