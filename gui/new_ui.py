# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sat Apr 19th, 2025
#
# __file__: new_gui.py
#
# STATUS: Stable
# __brief__: This file defines and implements the new UI for the CodeSmellApp.

# =========
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# =========

from pathlib import Path

from textual import events
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import (
    Header, Footer, Button, Input, Label,
    TextArea, RichLog, DirectoryTree
)
from textual.message import Message
from textual.reactive import reactive
from textual.screen import ModalScreen

from rich.markdown import Markdown

from core.file_saver import save_refactored_file
from core.refactor import refactor_duplicates
from core.code_smells import find_code_smells

from utils.utility import _read_file_contents
from utils.logger import setup_logger

# ==========
new_ui = setup_logger(name="new_ui.py_logger", log_file="new_ui.log")
# ==========

new_ui.info("new_ui")

# =========== IN-PROGRESS ===========
# A little risky, from a security perspective
is_being_graded = False

def set_project_root():
    os.environ["CPSC4260_GRADING"] = Path.home()
    
# Set env var to the root repo, use that in the file picker
# ===================================

class ConfirmationDialog(ModalScreen[bool]):
    """_summary_

    Args:
        ModalScreen (_type_): screen with the dialog
    """
    def __init__(self, message: str):
        """_summary_

        Args:
            message (str): message to display in the dialog
        """
        super().__init__()
        self.message = message
        self.add_class("confirmation-dialog")


    def compose(self) -> ComposeResult:
        """_summary_

        Returns:
            ComposeResult: irrelevant...

        Yields:
            Iterator[ComposeResult]: packs the dialog into a container
        """
        yield Vertical(
            Label("Confirmation", id="dialog-title"),
            Label(self.message, id="dialog-message"),
            Container(
                Horizontal(
                    Button("Yes", id="confirm_yes"),
                    Button("No", id="confirm_no"),
                ),
            id="button-container"
        ),
        id="dialog-container"
    )


    def on_button_pressed(self, event: Button.Pressed) -> None:
        """_summary_

        Args:
            event (Button.Pressed): button pressed event
        """
        self.dismiss(event.button.id == "confirm_yes")


class FilePicker(ModalScreen):
    """_summary_

    Args:
        ModalScreen (_type_): screen with the dialog

    Yields:
        _type_: packs the dialog into a container
    """

    # IMPORTANT: When being graded, need to change root repo
    def compose(self):
        """_summary_

        Yields:
            _type_: packs the dialog into a container
        """
        if is_being_graded:
            project_root = Path.home()
        else:
            project_root = Path(__file__).resolve().parent.parent
        yield Vertical(
            Input(placeholder="Filter filenames..."),
            DirectoryTree(project_root, id="directory_tree", name="Directory Tree"),
        )


    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected):
        """_summary_

        Args:
            event (DirectoryTree.FileSelected): file selected event
        """
        if event.path.suffix != ".py":
            self.app.query_one("#log", RichLog).write(
                f"⛔️ Please select a Python file (*.py). Got: {event.path.suffix}"
            )
            new_ui.warning(f"Unsupported file type: {event.path.suffix}")
            return
        
        else:
            self.app.pop_screen()
            self.app.post_message(UploadFileSelected(event.path))
        
                
class UploadFileSelected(Message):
    """_summary_

    Args:
        Message (_type_): message to be sent to the app
    """
    def __init__(self, path: Path):
        self.path = path
        super().__init__()

        
class CodeSmellApp(App):
    """_summary_

    Args:
        App (_type_): Parent class | Super class

    Yields:
        _type_: packs everything into a container, code editor + TextArea
    """
    SCREENS = {"file_picker": FilePicker}
    CSS_PATH = "textual_ui.css"
    BINDINGS = [ # bindings don't work in the app
        ("q", "quit", "Quit"),
        ("c", "clear", "Clear"),
        ("e", "exit", "Exit"),
    ]

    filename: reactive[str | None] = reactive(None)
    theme_dark: reactive[bool] = reactive(True)

    chosen_path = None
    
    
    def compose(self) -> ComposeResult:
        """_summary_

        Returns:
            ComposeResult: irrelevant...

        Yields:
            Iterator[ComposeResult]: packs everything into a container
        """
        yield Header()
        with Horizontal(id="main-pane"):
            with Vertical(id="left-pane"):
                yield Label("Console")
                yield RichLog(id="log")
                with Horizontal(id="buttons"):
                    yield Button("📂 Upload", id="upload")
                    yield Button("🧠 Analyze", id="analyze")
                    yield Button("🛠️  Refactor", id="refactor")
                    yield Button("💾 Save", id="save")
                    yield Button("🧹 Clear", id="clear")
                    yield Button("🌗 Theme", id="toggle_theme")
                    yield Button("❌ Exit", id="exit")
                yield Label("", id="file_info")
            with Vertical(id="right-pane"):
                yield Label("Code Editor")
                yield TextArea.code_editor(language="python", id="code_editor")
        yield Footer()


    def on_mount(self) -> None:
        """
        Brief: 
            Triggers on mounting the app, to display the welcome message.
        """
        code_editor = self.query_one("#code_editor", TextArea)
        code_editor.text = (
            "# ============================================\n"
            "# ===== Your code will be displayed here =====\n"
            "# ============================================\n\n"
        )

        log = self.query_one("#log", RichLog)
        log.write(
            "🚀 Welcome to CodeSmellApp!\n"
            "==================================================\n"
            "Please resize your terminal window to fit the app.\n"
            "==================================================\n\n"
            "Options:\n"
            "\t1. Click 'Upload' to select a Python file (*.py).\n"
            "\t2. Use 'Analyze' to detect code smells and get a Markdown Report.\n"
            "\t3. Use 'Refactor' to clean up duplicates.\n"
            "\t4. Save or clear your work as needed.\n"
        )
        
        
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """_summary_

        Args:
            event (Button.Pressed): button pressed event
        """
        btn = event.button.id
        if btn == "upload":
            await self.push_screen(FilePicker())
        elif btn == "analyze":
            self.analyze()
        elif btn == "refactor":
            self.refactor()
        elif btn == "save":
            await self.save()
        elif btn == "clear":
            await self.push_screen(
                ConfirmationDialog("Are you sure you want to clear the editor and console?"),
                callback=lambda result: self.clear() if result else None
            )
            # self.clear()
        elif btn == "toggle_theme":
            self.theme_dark = not self.theme_dark
            # self.set_class(self.theme_dark, "dark")
            # self.set_class(not self.theme_dark, "light")
            
            if self.theme_dark:
                self.remove_class("light")  
                self.set_class(True, "dark")
            else:
                self.remove_class("dark")   
                self.set_class(True, "light")
                
            self.query_one("#log", RichLog).write(
                f"🌗 Switched to {'dark' if self.theme_dark else 'light'} theme."
            )
        elif btn == "exit":
            await self.push_screen(
                    ConfirmationDialog("Are you sure you want to exit?"),
                    callback=lambda result: self.exit() if result else None
                )
            # self.exit()
    
    
    async def on_key(self, event: events.Key) -> None:
        """_summary_

        Args:
            event (events.Key): key pressed event
        """
        code_editor = self.query_one("#code_editor", TextArea)
        if self.focused == code_editor:
            event.stop()
    
    
    async def on_upload_file_selected(self, message: UploadFileSelected) -> None:
        """_summary_

        Args:
            message (UploadFileSelected): file selected message
        """
        self.filename = str(message.path)
        code_editor = self.query_one("#code_editor", TextArea)
        log = self.query_one("#log", RichLog)

        try:
            content = Path(self.filename).read_text()
        except Exception as e:
            self.log.write(f"❌ Failed to read file: {e}")
            return

        code_editor.clear()

        if not content.strip():
            code_editor.text = "# ❌ No code found in the file."
            log.write(f"📂 Loaded: {Path(self.filename).name} (empty file)")
        else:
            code_editor.text = "\n\n#=============== ORIGINAL ===============\n\n" + \
                                                                           content + \
                               "\n\n#=============== ORIGINAL ===============\n\n"
            log.write(f"📂 Loaded: {Path(self.filename).name}")

        self.query_one("#file_info", Label).update(f"📄 {Path(self.filename).name}")


    def analyze(self):
        """_summary_
        
        Brief:
            Triggers the analysis of the selected file for code smells.
            Displays the results in the log and updates the code editor.
        """
        log = self.query_one("#log", RichLog)
        code_editor = self.query_one("#code_editor", TextArea)
        
        if not self.filename:
            log.write("⛔️ No file selected.")
            return
        try:
            # ========== MD REPORT ============
            (code_smells, report_path) = find_code_smells(self.filename)
            report_str = _read_file_contents(report_path)
            md = Markdown(report_str)
            log.write(md)
            # ========== MD REPORT ============
            
        except FileNotFoundError:
                log.write(f"❌ Report file not found: {self.filename}")
                new_ui.error(f"Report file not found: {self.filename}", exc_info=True)
        except PermissionError:
                log.write(f"❌ Permission denied accessing: {self.filename}")
                new_ui.error(f"Permission denied: {self.filename}", exc_info=True)
        except Exception as e:
                log.write(f"❌ Analysis failed: {str(e)}")
                new_ui.error(f"Unexpected error during analysis: {e}", exc_info=True)


    def refactor(self):
        """_summary_
        
        Brief:
            Triggers the refactoring of the selected file to remove duplicates.
            Displays the results in the log and updates the code editor.
        """
        log = self.query_one("#log", RichLog)
        code_editor = self.query_one("#code_editor", TextArea)
        
        log.clear()
        
        if not self.filename:
            log.write("⛔️ No file selected.")
            return
        try:
            refactored, did_work = refactor_duplicates(self.filename)
            
            if did_work:
                code_editor.insert("\n\n\n#=============== REFACTORED ===============\n\n")
                code_editor.insert(refactored)
                code_editor.insert("\n\n#=============== REFACTORED ===============\n\n")
                
            else:
                code_editor.clear()
                code_editor.insert("\n\n\n#=============== NONE ===============\n\n")
                code_editor.insert(refactored)
                code_editor.insert("\n\n#=============== NONE ===============\n\n")
            
            self.query_one("#code_editor", TextArea).value = refactored
            log.write("✅ Refactor complete.")
            
        except FileNotFoundError:
            log.write(f"❌ File not found: {self.filename}")
            new_ui.error(f"File not found: {self.filename}", exc_info=True)
        except PermissionError:
            log.write(f"❌ Permission denied accessing: {self.filename}")
            new_ui.error(f"Permission denied: {self.filename}", exc_info=True)
        except Exception as e:
            log.write(f"❌ Refactor failed: {str(e)}")
            new_ui.error(f"Unexpected error during refactoring: {e}", exc_info=True)
                        
                             
    async def save(self):
        """_summary_
        
        Brief:
            Saves the refactored code to a file.
            Displays the save path in the log.
        """
        code_editor = self.query_one("#code_editor", TextArea)
        log = self.query_one("#log", RichLog)
        content = code_editor.value

        try:
            out_path = save_refactored_file(content, self.filename)
            log.write(f"\n\n💾 Saved to default path:\n\t{out_path}")
        except Exception as e:
            new_ui.error(f"error: {e}", exc_info=True, stack_info=True)
            log.write(f"\n\n❌ Save failed: {e}")


    def clear(self):
        """_summary_
        
        Brief:
            Clears the code editor and log.
            Displays a confirmation message.
        """
        self.filename = None # reset filename
        self.query_one("#code_editor", TextArea).clear()
        self.query_one("#log", RichLog).clear()


# ========================== RUN ==========================
if __name__ == "__main__":
    app = CodeSmellApp()
    app.run()
# =========================================================