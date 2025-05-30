# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sat Apr 19th, 2025
#
# __file__: save_refactored.py
#
# __brief__: This script is used for saving the refactored code to a new file

import os
# =========
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# =========

import time

from utils.exceptions import FileEmptyError
from utils.logger import setup_logger

# ==========
save_refactored_logger = setup_logger(
    name="save_refactored.py_logger", log_file="save_refactored.log"
)
# ==========

save_refactored_logger.info("save_refactored_logger")


def save_refactored_file(
        file_content: str, original_filename: str, make_copy: bool = False
) -> str:
    """_summary_

    Args:
        file_content (str): The refactored code to be saved to the new file
        original_filename (str): The original filename from which the new filename is derived
        make_copy (bool): If True, saves a copy of the refactored file; if False, saves in place.

    Raises:
        FileEmptyError: @see "exceptions.py"

    Returns:
        str: the new updated filename (<file>.refactored.<extension>)
    """

    # need the ability to save a copy or save in place...
    # Testing it out:

    out_path = "\0"

    if not file_content.strip():
        raise FileEmptyError(
            "File content is empty",
            filename=original_filename,
            function="save_refactored_file()",
        )

    if not make_copy:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        refactored_dir = os.path.join(project_root, "data", "refactored")
        os.makedirs(refactored_dir, exist_ok=True)

        name, ext = os.path.splitext(os.path.basename(original_filename))
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        new_filename = f"refactored_{name}_{timestamp}{ext}"
        out_path = os.path.join(refactored_dir, new_filename)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(file_content)

        save_refactored_logger.info(f"Refactored file saved as: {out_path}")

    else:
        with open(original_filename, "w", encoding="utf-8") as f:
            f.write(file_content)

        save_refactored_logger.info(
            f"Refactored file saved in place: {original_filename}"
        )
        out_path = original_filename

    print('I can access " out_path " from here:', out_path)
    return out_path
