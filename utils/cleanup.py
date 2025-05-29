# The purpose of this script is to clean up the project directory by removing unnecessary files and directories.
#   This mostly targets temporary files, cache directories, and other artifacts that are not needed for the project to run or be tested.

# USE WITH CAUTION: This script will permanently delete files and directories.

# =========
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# =========

import shutil

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

CLEANUP_PATHS = {
    "file_info": os.path.join(BASE_DIR, "file_info"),
    "info": os.path.join(BASE_DIR, "info"),
    "json": os.path.join(BASE_DIR, "json"),
    "logs": os.path.join(BASE_DIR, "logs"),
    "output": os.path.join(BASE_DIR, "output"),
    "readable": os.path.join(BASE_DIR, "readable"),
    "refactored": os.path.join(BASE_DIR, "refactored"),
    "report": os.path.join(BASE_DIR, "report"),
    "plots": os.path.join(BASE_DIR, "plots"),
}


def clean_dirs(are_you_sure: bool = False):
    if are_you_sure:
        for name, path in CLEANUP_PATHS.items():
            print(f"Cleaning: {name.ljust(12)} -> {path}")
            if os.path.exists(path):
                for f in os.listdir(path):
                    full_path = os.path.join(path, f)
                    try:
                        if os.path.isfile(full_path) or os.path.islink(full_path):
                            os.unlink(full_path)
                        elif os.path.isdir(full_path):
                            shutil.rmtree(full_path)
                    except Exception as e:
                        print(f"  Failed to delete {full_path}: {e}")
            else:
                print(f"  Path does not exist: {path}")
    else:
        # to avoid accidents
        print("Cleanup aborted. Please run with are_you_sure=True to confirm deletion.")


clean_dirs(True)
