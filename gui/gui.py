# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sat Apr 19th, 2025
#
# __file__: gui.py
#
# __brief__: TODO

# TRASH

"""__imports__"""
import tkinter as tk
import customtkinter as ctk
from tkcode import CodeEditor
from tkinter import filedialog

import threading
import os
import json

from CPSC4260.project_root.core.file_info_extractor import (extract_file_info,
                           save_to_json)

from CPSC4260.project_root.core.file_saver import (save_refactored_file)

from core.code_metrics import (fetch_code_metrics)
from CPSC4260.project_root.core.halstead import (fetch_halstead_metrics)

from CPSC4260.project_root.utils.exceptions import (FileReadError,
                        CorruptFileError,
                        FileNotFoundError,
                        FileEmptyError,
                        FileTypeUnsupportedError,
                        FileDecodeError,
                        FileLockedError,
                        FileTooLargeError,
                        FileOpenError)
            
from core.constants import (WINDOW_SIZE,
                       WINDOW_TITLE,
                       FONT_FAMILY,
                       FONT_SIZE,
                       UNI_WIDTH,
                       HEIGHT,
                       CTK_TEXTBOX_X_PADDING,
                       CTK_TEXTBOX_Y_PADDING,
                       CTK_BUTTON_X_PADDING,
                       CTK_BUTTON_Y_PADDING,
                       CTK_LABEL_Y_PADDING,
                       CODE_EDITOR_WIDTH)

"""__class: CodeSmellGUI__"""
class CodeSmellGUI(ctk.CTkFrame):
    def __init__(self, root):
        root.geometry(WINDOW_SIZE)
        root.title(WINDOW_TITLE)
        root.minsize(1800, 750)
        self.filename = ""
        self.lock = threading.Lock()

        # Main layout frame
        self.master = ctk.CTkFrame(root)
        self.master.pack(expand=True, fill="both")
        self.master.pack_propagate(False)

        # Font
        self.my_font = ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZE)

        # ===== TEXT FRAME (LEFT + RIGHT PANES) =====
        self.text_frame = ctk.CTkFrame(self.master, height=HEIGHT)
        self.text_frame.pack(side=tk.TOP, fill=tk.X, padx=CTK_TEXTBOX_X_PADDING, pady=CTK_TEXTBOX_Y_PADDING)
        self.text_frame.pack_propagate(False)

        # === LEFT ===: Output Text
        self.output_text = ctk.CTkTextbox(self.text_frame, width=CODE_EDITOR_WIDTH//2, height=HEIGHT, font=self.my_font)
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        
        # Fill
        self.output_text.insert(tk.END, "\n👋 Welcome to the Code Smell Detector!\n\n", "welcome")
        self.output_text.insert(tk.END, "📂 Upload a file to get started.\n", "center")
        self.output_text.insert(tk.END, "🧠 Click 'Analyze' to check for code smells.\n", "center")
        self.output_text.insert(tk.END, "🛠️ Click 'Refactor Duplicates' to refactor the code.\n", "center")
        self.output_text.insert(tk.END, "💾 Click 'Save Results' to save the output.\n", "center")
        self.output_text.insert(tk.END, "🧹 Click 'Clear Output' to clear the output.\n", "center")
        self.output_text.insert(tk.END, "❌ Click 'Exit' to close the application.\n", "center")
        self.output_text.insert(tk.END, "🧑‍💻 Should you encounter any issues, please check the \n   terminal for error messages.\n", "center")

        # === RIGHT ===: Code Editor
        self.code_editor = CodeEditor(self.text_frame, width=UNI_WIDTH//2, height=HEIGHT, font=self.my_font)
        self.code_editor.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

        # ===== BUTTON FRAME =====
        self.button_frame = ctk.CTkFrame(self.master)
        self.button_frame.pack(side=tk.TOP, pady=10)

        # ===== BUTTONS =====
        self.upload_button = ctk.CTkButton(self.button_frame, text="📂 Upload File", command=self.upload_file, font=self.my_font)
        self.upload_button.grid(row=0, column=0, padx=CTK_BUTTON_X_PADDING, pady=CTK_BUTTON_Y_PADDING)

        self.analyze_button = ctk.CTkButton(self.button_frame, text="🧠 Analyze", command=self.analyze_file, font=self.my_font)
        self.analyze_button.grid(row=0, column=1, padx=CTK_BUTTON_X_PADDING, pady=CTK_BUTTON_Y_PADDING)

        self.refactor_button = ctk.CTkButton(self.button_frame, text="🛠️ Refactor Duplicates", command=self.refactor_code, font=self.my_font)
        self.refactor_button.grid(row=0, column=2, padx=CTK_BUTTON_X_PADDING, pady=CTK_BUTTON_Y_PADDING)

        self.save_button = ctk.CTkButton(self.button_frame, text="💾 Save Results", command=self.save_results, font=self.my_font)
        self.save_button.grid(row=0, column=3, padx=CTK_BUTTON_X_PADDING, pady=CTK_BUTTON_Y_PADDING)

        self.clear_button = ctk.CTkButton(self.button_frame, text="🧹 Clear Output", command=self.clear_output, font=self.my_font)
        self.clear_button.grid(row=0, column=4, padx=CTK_BUTTON_X_PADDING, pady=CTK_BUTTON_Y_PADDING)

        self.exit_button = ctk.CTkButton(self.button_frame, text="❌ Exit", command=self.exit, font=self.my_font)
        self.exit_button.grid(row=0, column=5, padx=CTK_BUTTON_X_PADDING, pady=CTK_BUTTON_Y_PADDING)

        # ===== FOOTER =====
        self.made_by_label = ctk.CTkLabel(self.master, text="Made by JB", font=self.my_font, fg_color="transparent", text_color="lightgray")
        self.made_by_label.pack(side=tk.BOTTOM, pady=CTK_LABEL_Y_PADDING)
        
        # Text box  
        
    def upload_file(self):
        self.upload_button.configure(state=tk.DISABLED)
        
        self.filename = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Select Code File",
              
            filetypes=[("Code files", "*.py *.txt"), ("All files", "*.*")]
        )
        
        upload_thread = threading.Thread(target=self.run_file_upload)
        upload_thread.start()
        
        
    def run_file_upload(self):
        if self.filename:
            self.output_text.insert(tk.END, f"\n📂 File uploaded: {os.path.basename(self.filename)}\n")
            
            try:
                file_obj = open(self.filename, "r")
                metadata = extract_file_info(file_obj)
                
                self.code_editor.after(0, self.update_code_editor, metadata["Data"])
                
                save_to_json(metadata)
                
                self.upload_button.configure(state=tk.NORMAL)
                return metadata

            except (FileReadError, CorruptFileError,
                    FileNotFoundError,FileEmptyError,
                    FileTypeUnsupportedError, FileDecodeError, 
                    FileLockedError, FileTooLargeError,
                    FileOpenError) as e:
                self.output_text.insert(tk.END, f"❌ Error opening file, check terminal\n")
                print(e.what())
            
            except Exception as e:
                self.output_text.insert(tk.END, f"❌ Error opening file: {e}\n")
                self.upload_button.configure(state=tk.NORMAL)
                return None
        else:
            self.output_text.insert(tk.END, "\n⛔️ No file selected.\n")
            self.upload_button.configure(state=tk.NORMAL)
            return None

    def update_code_editor(self, metrics_str):
        self.code_editor.delete("1.0", tk.END)
        self.code_editor.insert("1.0", metrics_str)
        self.output_text.insert(tk.END, "✅ Complete.\n")
        
    def analyze_file(self):
        if not self.filename:
            self.output_text.insert(tk.END, "⛔️ Please upload a file first.\n")
            return 

        self.analyze_button.configure(state=tk.DISABLED) 
        
        analysis_thread = threading.Thread(target=self.run_analysis)
        analysis_thread.start()
                
    def run_analysis(self):

        code_m = fetch_code_metrics(self.filename)
        halstead_m = fetch_halstead_metrics(self.filename)

        loc_sloc_metr = {
            "LOC": {"value": code_m["LOC"], "description": "Lines of Code"},
            "SLOC": {"value": code_m["SLOC"], "description": "Source Lines of Code"},
            "Comment Density": {"value": code_m["Comment Density"], "description": "Percentage of lines dedicated to comments", "recommended_range": "Recommended: 20% to 30%"},
            "Blank Line Density": {"value": code_m["Blank Line Density"], "description": "Percentage of blank lines for readability", "recommended_range": "Recommended: 15% to 25%"}
        }

        halstead_metr = {
            "n1": {"value": halstead_m["n1"], "description": "Number of distinct operators"},
            "n2": {"value": halstead_m["n2"], "description": "Number of distinct operands"},
            "N1": {"value": halstead_m["N1"], "description": "Total number of operators"},
            "N2": {"value": halstead_m["N2"], "description": "Total number of operands"},
            "N": {"value": halstead_m["N"], "description": "Total number of operators and operands", "recommended_range": "Lower is better"},
            "n": {"value": halstead_m["n"], "description": "Total number of operators"},
            "V": {"value": halstead_m["V"], "description": "Volume - Measures the size of the program"},
            "D": {"value": halstead_m["D"], "description": "Difficulty - Measures how difficult the program is to understand", "recommended_range": "Lower is better (under 10)"},
            "HN": {"value": halstead_m["HN"], "description": "Halstead's Effort - Measures the effort required to understand the program", "recommended_range": "Lower values indicate easier code"},
            "E": {"value": halstead_m["E"], "description": "Estimated time to understand the program in seconds", "recommended_range": "Lower is better"},
            "T": {"value": halstead_m["T"], "description": "Time to implement the program in seconds"},
            "B": {"value": halstead_m["B"], "description": "Bugs - The number of bugs that might exist", "recommended_range": "Lower is better (typically < 5)"},
            "M": {"value": halstead_m["M"], "description": "Maintainability Index - Reflects how maintainable the program is", "recommended_range": "Higher is better (above 60 is good)"}
        }

        combined_metrics = {
            "Loc/SLOC Metrics": loc_sloc_metr,
            "Halstead Metrics": halstead_metr,
        }

        metrics_str = json.dumps(combined_metrics, indent=4)
        
        self.code_editor.after(0, self.update_code_editor, metrics_str)
        
        self.analyze_button.configure(state=tk.NORMAL)         
        
        
        
        
    # ***************************************************************************************************
    def refactor_code(self):
        
        # Prevent multiple clicks
        self.refactor_button.configure(state=tk.DISABLED)
        
        if not self.filename:
            self.output_text.insert(tk.END, "⛔️ Upload a file before attempting refactor.\n")
            return
        
        # Prevent multiple clicks
        self.refactor_button.configure(state=tk.NORMAL)
    # ***************************************************************************************************




    def save_results(self):
        
        # Prevent multiple clicks
        self.save_button.configure(state=tk.DISABLED)
        
        output = self.output_text.get("1.0", tk.END)
        
        if not output.strip():
            self.output_text.insert(tk.END, "⛔️ Nothing to save.\n")
            return
        
        if not self.filename:
            self.output_text.insert(tk.END, "⛔️ No file associated with output. Please upload a file first.\n")
            return

        try:
            out_path = save_refactored_file(output, self.filename)
            self.output_text.insert(tk.END, f"💾 Output saved to {out_path}\n")
            
        except FileEmptyError as e:
            print(e.what())
            self.output_text.insert(tk.END, "❌ Error saving output: file is empty.\n")
            
        except Exception as e:
            self.output_text.insert(tk.END, f"❌ Error saving output: {e}\n")
        
        # Prevent multiple clicks
        self.save_button.configure(state=tk.NORMAL)

    def clear_output(self):
        # Prevent multiple clicks
        self.clear_button.configure(state=tk.DISABLED)
        
        self.code_editor.delete("1.0", tk.END)
        
        # Prevent multiple clicks
        self.clear_button.configure(state=tk.NORMAL)
        
    def exit(self):
        # Prevent multiple clicks
        self.exit_button.configure(state=tk.DISABLED)
        
        self.master.quit()
        self.master.destroy()
        
        # Prevent multiple clicks
        self.exit_button.configure(state=tk.NORMAL)

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    root = ctk.CTk()
    gui = CodeSmellGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()