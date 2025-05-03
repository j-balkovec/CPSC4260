# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sat Apr 19th, 2025
#
# __file__: save_refactored.py
#
# # __brief__: TODO

import os
import time

from exceptions import (FileEmptyError)
from logger import setup_logger

# ==========
save_refactored_logger = setup_logger(name="save_refactored.py_logger", log_file="save_refactored.log")
# ==========

save_refactored_logger.info("save_refactored_logger")

def save_refactored_file(file_content: str, original_filename: str) -> str:
    """_summary_

    Args:
        file_content (str): The refactored code to be saved to the new file
        original_filename (str): The original filename from which the new filename is derived

    Raises:
        FileEmptyError: @see "exceptions.py"

    Returns:
        str: the new updated filename (<file>.refactored.<extension>)
    """
    
    if not file_content.strip():
        raise FileEmptyError("File content is empty", filename=original_filename, function="save_refactored_file()")

    out_dir = "refactored"
    os.makedirs(out_dir, exist_ok=True)

    name, ext = os.path.splitext(os.path.basename(original_filename))
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    new_filename = f"refactored_{name}_{timestamp}{ext}"
    out_path = os.path.join(out_dir, new_filename)

    # Save the file
    with open(out_path, "w") as f:
        f.write(file_content)

    save_refactored_logger.info(f"Refactored file saved as: {out_path}")
    return out_path
