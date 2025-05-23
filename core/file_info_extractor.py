# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sat Apr 19th, 2025
#
# __file__: file_info_extracotr.py
#
# __brief__: This script extracts all the necessary file info

# =========
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# =========

import time
import json

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

from core.constants import SIZE_LIMIT
from utils.logger import setup_logger

# ==========
get_file_info_logger = setup_logger(
    name="get_file_info.py_logger", log_file="get_file_info.log"
)
# ==========

get_file_info_logger.info("get_file_info")


def extract_file_info(file_obj) -> dict:
    """_summary_

    Args:
        file_obj (_type_): 'Object' returned from 'upload_file()'.

    Raises:
        FileReadError: @see exceptions.py
        CorruptFileError: @see exceptions.py
        FileLockedError: @see exceptions.py
        FileNotFoundError: @see exceptions.py
        FileOpenError: @see exceptions.py

    Returns:
        dict: the metadata of the file
    """
    try:
        file_path = file_obj.name
        get_file_info_logger.info(f"Starting metadata extraction for: {file_path}")

        valid = _validate_file(file_path)

        if not valid:
            raise FileReadError(
                "Validation failed", filename=file_path, function="extract_file_info"
            )
        get_file_info_logger.info(f"Validation successful for: {file_path}")

        metadata = _gather_metadata(file_path, file_obj)

        if metadata is None:
            raise CorruptFileError(
                "Failed to gather metadata",
                filename=file_path,
                function="extract_file_info",
            )

        get_file_info_logger.info(
                f"Metadata gathered successfully for: {file_path}"
            )

        return metadata

    except PermissionError as e:
        raise FileLockedError(
            "Permission denied", filename=file_path, function="extract_file_info"
        ) from e

    except FileNotFoundError as e:
        raise FileNotFoundError(
            "File not found", filename=file_path, function="extract_file_info"
        ) from e

    except OSError as e:
        raise FileOpenError(
            "OS error while opening the file",
            filename=file_path,
            function="extract_file_info",
        ) from e

    except FileReadError as e:
        raise FileReadError(
            "File read error", filename=file_path, function="extract_file_info"
        ) from e

    except CorruptFileError as e:
        raise CorruptFileError(
            "Corrupt file error", filename=file_path, function="extract_file_info"
        ) from e


def _validate_file(file_path: str) -> bool:
    """_summary_

    Args:
        file_path (str): full path of the file associated with the file_obj

    Raises:
        FileNotFoundError: @see exceptions.py
        FileEmptyError: @see exceptions.py
        FileTooLargeError: @see exceptions.py
        FileTypeUnsupportedError: @see exceptions.py

    Returns:
        bool: returns True if the file is valid, otherwise raises an exception
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            "File not found", filename=file_path, function="_validate_file"
        )

    size = os.path.getsize(file_path)

    if size == 0:
        raise FileEmptyError(
            "File is empty", filename=file_path, function="_validate_file"
        )

    if size > SIZE_LIMIT:
        raise FileTooLargeError(
            "File is too large", filename=file_path, function="_validate_file"
        )

    file_type = os.path.splitext(file_path)[1].lstrip(".")

    if file_type not in ["py", "txt"]:
        raise FileTypeUnsupportedError(
            "File type is unsupported", filename=file_path, function="_validate_file"
        )

    return True


def _gather_metadata(file_path: str, file_obj) -> dict:
    """_summary_

    Args:
        file_path (str): full path of the file associated with the file_obj
        file_obj (_type_): 'Object' returned from 'upload_file()'. @see gui.py

    Raises:
        FileDecodeError: @see exceptions.py
        FileReadError: @see exceptions.py

    Returns:
        dict: the metadata of the file
    """
    name = os.path.basename(file_path)
    size = os.path.getsize(file_path)
    file_type = os.path.splitext(file_path)[1].lstrip(".")
    date_created = time.ctime(os.path.getctime(file_path))
    date_modified = time.ctime(os.path.getmtime(file_path))
    date_accessed = time.ctime(os.path.getatime(file_path))

    file_obj.seek(0)

    try:

        data = file_obj.read()

    except UnicodeDecodeError as e:
        raise FileDecodeError(
            "Failed to decode file", filename=file_path, function="_gather_metadata"
        ) from e

    except Exception as e:
        raise FileReadError(
            "Failed to read file", filename=file_path, function="_gather_metadata"
        ) from e

    file_obj.close()

    metadata = {
        "Name": name,
        "Size": f"{size} bytes",
        "Type": file_type,
        "Date Created": date_created,
        "Date Modified": date_modified,
        "Date Accessed": date_accessed,
        "Data": data,
    }

    get_file_info_logger.info(f"Metadata assembled for: {file_path}")
    return metadata


def save_to_json(metadata: dict):
    """_summary_

    Args:
        metadata (dict): the metadata of the file, obtained from @see '_gather_metadata()'

    Returns:
        _type_: path of the output file (<path>/json/info_<file_name>_<timestamp>.json)
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    json_dir = os.path.join(project_root, "data", "file_info")
    os.makedirs(json_dir, exist_ok=True)

    base_name = os.path.splitext(metadata["Name"])[0]
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    file_name = f"info_{base_name}_{timestamp}.json"
    file_path = os.path.join(json_dir, file_name)

    with open(file_path, "w", encoding='utf-8') as json_file:
        json.dump(metadata, json_file, indent=4)

    get_file_info_logger.info(f"Saved metadata to JSON: {file_path}")

    return file_path


# index out of range
