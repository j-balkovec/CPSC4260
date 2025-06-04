# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sat Apr 19th, 2025
#
# __file__: new_gui.py
#
# __brief__: Terminal user interface for the Code Smell Detector

import os
# =========
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# =========

import json
import argparse

from core.file_info_extractor import extract_file_info, save_to_json

from core.file_saver import save_refactored_file
from core.code_smells import find_code_smells
from core.refactor import refactor_duplicates

from utils.utility import _read_file_contents

from utils.exceptions import (
    FileReadError,
    CorruptFileError,
    FileNotFoundError,
    FileEmptyError,
    FileTypeUnsupportedError,
    FileDecodeError,
    FileLockedError,
    FileTooLargeError,
    FileOpenError,
)


class TerminalUI:
    """_summary_
    Terminal user interface.
    """

    def __init__(self):
        """_summary_
        Constructor for the TerminalUI class.
        """
        self.filepath = None
        self.metadata = None
        self.report_path = None
        self.code = None
        self.json_path = None

    def upload_file(self, path):
        """Uploads a file and extracts its metadata.

        Args:
            path (str): path or filename of the file to be uploaded
        """
        resolved_path = os.path.abspath(path)

        if not os.path.isfile(resolved_path):
            print(f"File not found: {path}")
            print(
                "Hint: Try using a relative path or place the file in the current directory."
            )
            return

        try:
            self.code = _read_file_contents(resolved_path)
            with open(resolved_path, "r", encoding="utf-8") as f:
                self.metadata = extract_file_info(f)
                self.json_path = save_to_json(self.metadata)
                self.filepath = resolved_path
                print(
                    f"File '{os.path.basename(resolved_path)}' uploaded successfully."
                )

        except (
                FileReadError,
                CorruptFileError,
                FileNotFoundError,
                FileEmptyError,
                FileTypeUnsupportedError,
                FileDecodeError,
                FileLockedError,
                FileTooLargeError,
                FileOpenError,
        ) as e:
            print(f"Error opening file: {e.what()}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def analyze_file(self):
        """_summary_

        Analyzes the uploaded file for code smells and metrics.

        """
        if not self.filepath:
            print("Please upload a file first.")
            return

        print("\nAnalyzing file...")
        try:
            code_smells, report_path = find_code_smells(self.filepath)
            self.report_path = report_path

            print("\n[*] Code Metrics:")
            for key, val in code_smells.get("code_metrics", {}).items():
                print(f"  - {key}: {val}")

            print("\n[*] Halstead Metrics:")
            for key, val in code_smells.get("halstead_metrics", {}).items():
                print(f"  - {key}: {val}")

            print("\n[*] Code Smells Found:")
            for category in ["long_parameter_list", "long_method", "duplicated_code"]:
                issues = code_smells.get(category, [])
                print(f"\n[+] {category.replace('_', ' ').title()}:")
                if not issues:
                    print(" - None Found")
                else:
                    for i, issue in enumerate(issues, start=1):
                        print(f"  {i}.")
                        if isinstance(issue, dict):
                            for key, val in issue.items():
                                if isinstance(val, dict):
                                    print(f"\n    - {key}:")
                                    for sub_key, sub_val in val.items():
                                        if (
                                                sub_key == "text"
                                                and val.get("type") == "code"
                                        ):
                                            print(
                                                "\n        +---------------- CODE ----------------+"
                                            )
                                            for line in sub_val.splitlines():
                                                print(f"        | {line}")
                                            print(
                                                "        +--------------------------------------+\n"
                                            )
                                        print(f"        {sub_key}: {repr(sub_val)}")
                                else:
                                    print(f"    - {key}: {repr(val)}")
                        else:
                            print(f"    - {issue}")

            print(f"\nMarkdown report saved at: {report_path}")

        except Exception as e:
            print(f"Error analyzing file: {e}")

    def refactor_code(self):
        """_summary_

        Refactors the uploaded file to remove duplicate code.

        Returns:
            str: Refactored code content
        """
        if not self.filepath:
            print("Please upload a file first.")
            return

        print("Refactoring duplicate code...")
        try:
            refactored, _ = refactor_duplicates(
                self.filepath
            )  # discard did_work return obj
            self.code = refactored
            save_refactored_file(refactored, self.filepath)
            print("Refactoring complete.")
        except Exception as e:
            print(f"Error during refactoring: {e}")

    def save_results(self):
        """_summary_

        Saves the refactored code and metadata to a JSON file

        """
        if not self.code:
            print(
                "No code content available to save. Run upload and refactor/analyze first."
            )
            return

        try:
            updated_code_file = save_refactored_file(self.code, self.filepath)
            print(f"Refactored code saved to: {updated_code_file}")

            if not self.json_path or not os.path.isfile(self.json_path):
                print("JSON metadata file missing; cannot save results.")
                return

            with open(self.json_path, "r", encoding="utf-8") as infile:
                json.load(infile)

        except Exception as e:
            print(f"Error saving results: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Code Smell Detector CLI")
    parser.add_argument("-u", "--upload", metavar="FILE", help="Upload file")
    parser.add_argument("-a", "--analyze", action="store_true", help="Analyze file")
    parser.add_argument(
        "-rd", "--refactor-duplicates", action="store_true", help="Refactor duplicates"
    )
    parser.add_argument("-s", "--save", action="store_true", help="Save file")

    args = parser.parse_args()
    ui = TerminalUI()

    if args.upload:
        ui.upload_file(args.upload)

    if args.analyze:
        ui.analyze_file()

    if args.refactor_duplicates:
        # need to pass in the flag
        ui.refactor_code()

    if args.save:
        ui.save_results()
