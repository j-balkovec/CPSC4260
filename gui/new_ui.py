# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sat Apr 19th, 2025
#
# __file__: new_gui.py
#
# __brief__: TODO

# =========
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# =========

from pathlib import Path
import json

from textual import events
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import (
    Header, Footer, Static, Button, Input, Label,
    TextArea, Log, RichLog, DirectoryTree
)
from textual.message import Message
from textual.reactive import reactive
from textual.screen import ModalScreen

from rich.markdown import Markdown

from core.file_saver import save_refactored_file
from core.code_metrics import fetch_code_metrics
from core.halstead import fetch_halstead_metrics
from core.refactor import refactor_duplicates
from core.code_smells import find_code_smells

from utils.utility import _read_file_contents
from utils.logger import setup_logger

# ==========
new_ui = setup_logger(name="new_ui.py_logger", log_file="new_ui.log")
# ==========

new_ui.info("new_ui")

is_being_graded = False

class FilePicker(ModalScreen):

    # IMPORTANT: When being graded, probably need to change
    def compose(self):
        if is_being_graded:
            project_root = Path.home()
        else:
            project_root = Path(__file__).resolve().parent.parent
        yield Vertical(
            Input(placeholder="Filter filenames..."),
            DirectoryTree(project_root, id="directory_tree", name="Directory Tree"),
        )

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected):
        self.app.pop_screen()
        self.app.post_message(UploadFileSelected(event.path))
        
class UploadFileSelected(Message):
    def __init__(self, path: Path):
        self.path = path
        super().__init__()


class CodeSmellApp(App):
    CSS_PATH = "textual_ui.css"
    BINDINGS = [("q", "quit", "Quit")]

    filename: reactive[str | None] = reactive(None)
    theme_dark: reactive[bool] = reactive(True)

    def compose(self) -> ComposeResult:
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
                    yield Button("❌ Exit", id="exit")
                yield Label("", id="file_info")

            with Vertical(id="right-pane"):
                yield Label("Code Editor")
                yield TextArea.code_editor(language="python", id="code_editor")
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        btn = event.button.id
        if btn == "upload":
            await self.push_screen(FilePicker())
        elif btn == "analyze":
            self.analyze()
        elif btn == "refactor":
            self.refactor()
        elif btn == "save":
            self.save()
        elif btn == "clear":
            self.clear()
        elif btn == "exit":
            self.exit()
    
    
    async def on_upload_file_selected(self, message: UploadFileSelected) -> None:
        self.filename = str(message.path)

        try:
            content = Path(self.filename).read_text()
        except Exception as e:
            self.query_one("#log", RichLog).write(f"❌ Failed to read file: {e}")
            return

        self.query_one("#code_editor", TextArea).value = content
        self.query_one("#log", RichLog).write(f"📂 Loaded: {Path(self.filename).name}")
        self.query_one("#file_info", Label).update(f"📄 {Path(self.filename).name}")


    def analyze(self):
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
            
            # ========== CODE ============
            raw_code = _read_file_contents(self.filename)
            
            if not raw_code.strip():
                log.write("❌ No code found in the file.")
            else:
                code_editor.insert(raw_code)
            # ========== CODE ============
            
        except Exception as e:
            new_ui.error(f"error: {e}", exc_info=True, stack_info=True)
            log.write(f"❌ Error: {e}")

    def refactor(self):
        log = self.query_one("#log", RichLog)
        code_editor = self.query_one("#code_editor", TextArea)
        
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
        except Exception as e:
            new_ui.error(f"error: {e}", exc_info=True, stack_info=True)
            log.write(f"❌ Refactor failed: {e}")

    def save(self):
        log = self.query_one("#log", RichLog)
        if not self.filename:
            log.write("⛔️ No file selected.")
            return
        content = self.query_one("#code_editor", TextArea).value
        try:
            out_path = save_refactored_file(content, self.filename)
            log.write(f"💾 Saved to {out_path}")
        except Exception as e:
            new_ui.error(f"error: {e}", exc_info=True, stack_info=True)
            log.write(f"❌ Save failed: {e}")

    def clear(self):
        self.query_one("#code_editor", TextArea).clear()
        self.query_one("#log", RichLog).clear()

if __name__ == "__main__":
    app = CodeSmellApp()
    app.run()