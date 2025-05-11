# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sun Apr 20th, 2025
#
# __file__: error_handler.py
#
# __brief__: This file defines custom errors used throughout this project

# =========
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# =========

from core.constants import (ERROR_CODES, 
                       YELLOW_TEXT, 
                       RESET_TEXT, 
                       RED_TEXT)


class CustomExceptionSuper(Exception):
    """_summary_

    Args:
        Exception (_type_): Parent class

    Returns:
        _type_: This class provides a base for all the other child classes
    """
    
    error_key: str = "unknown_error"
    error_name: str = "CustomExceptionSuper"

    def __init__(self, message="[DEFAULT]", **context):
        super().__init__(message)
        self.context = context

    # Yields the raw error message, if the user wishes to store it in a file
    def __repr__(self) -> str:
        return (f"{self.error_name}: {self.args[0]} "
                f"(code: {ERROR_CODES.get(self.error_key, 'N/A')})")

    # Yields a formatted error message for the user
    def what(self) -> str: # TODO: propagate this to the GUI
        context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
        return ("\n" + 
                RED_TEXT + f"[error]" + RESET_TEXT + f": {self.error_name.lower()} occurred" + 
                YELLOW_TEXT + f"\n[error code]" + RESET_TEXT + f": {ERROR_CODES.get(self.error_key, 'N/A')}" +
                YELLOW_TEXT + f"\n[message]" + RESET_TEXT + f": {self.args[0]}" +
                YELLOW_TEXT + f"\n[context]" + RESET_TEXT + f": {context_str}" +
                "\n")
    

class FileReadError(CustomExceptionSuper):
    """_summary_

    Args:
        CustomExceptionSuper (_type_): Parent class
        
    Error Code:
        1001: FileReadError
    
    How to resolve this error:
        Check if the file exists and is accessible. 
        Ensure you have the necessary permissions to 
        read the file (check with ls -l).
        Check if the file is not corrupted or empty.
        
        This serves as the most general error, and is 
        used when no other error is specified. The client
        should always try and use a more specific error first.
    """
    error_key = "file_read"
    error_name = "FileReadError"

class CorruptFileError(CustomExceptionSuper):
    """_summary_

    Args:
        CustomExceptionSuper (_type_): Parent class
        
    Error Code:
        1002: CorruptFileError
        
    How to resolve this error:
        This usually happens if the mode is not set right.
        Look at the 'open()' function in the code.
        Ensure that the file is not empty and contains 
        valid data. If the file is a binary file, ensure it is 
        opened in binary mode.
        
        This error is used when the file is corrupted
        or not in a readable format.
    """
    error_key = "corrupt_file"
    error_name = "CorruptFileError"

class FileNotFoundError(CustomExceptionSuper):
    """_summary_

    Args:
        CustomExceptionSuper (_type_): Parent class
        
    Error Code:
        1003: FileNotFoundError
        
    How to resolve this error:
        Check if the file exists and is accessible. 
        Ensure you have the necessary permissions to 
        read the file (check with ls -l).
        
        This error is used when the file is not found
        or does not exist.
    """
    error_key = "file_not_found"
    error_name = "FileNotFoundError"

class FileEmptyError(CustomExceptionSuper):
    """_summary_

    Args:
        CustomExceptionSuper (_type_): Parent class
        
    How to resolve this error:
        Check if the file is empty. 
        Ensure that the file contains valid data.
        
        This error is used when the file is empty
        or does not contain any data.
    """
    error_key = "file_empty"
    error_name = "FileEmptyError"

class FileTypeUnsupportedError(CustomExceptionSuper):
    """_summary_

    Args:
        CustomExceptionSuper (_type_): Parent class
        
    How to resolve this error:
        Check if the file type is supported. 
        Ensure that the file is of a valid type.
        
        This error is used when the file type is not
        supported or recognized.
    """
    error_key = "file_type_unsupported"
    error_name = "FileTypeUnsupportedError"

class FileDecodeError(CustomExceptionSuper):
    """_summary_

    Args:
        CustomExceptionSuper (_type_): Parent class
        
    How to resolve this error:
        Check if the file is encoded properly. 
        Ensure that the file is not corrupted or empty.
        
        This error is used when the file cannot be
        decoded or read properly.
    """
    error_key = "file_decode_error"
    error_name = "FileDecodeError"

class FileLockedError(CustomExceptionSuper):
    """_summary_

    Args:
        CustomExceptionSuper (_type_): Parent class
        
    How to resolve this error:
        Check if the file is locked by another process. 
        Ensure that the file is not being used by another program.
        
        This error is used when the file is locked
        or cannot be accessed.
    """
    error_key = "file_locked"
    error_name = "FileLockedError"

class FileTooLargeError(CustomExceptionSuper):
    """_summary_

    Args:
        CustomExceptionSuper (_type_): Parent class
        
    How to resolve this error:
        Check if the file is too large. 
        Ensure that the file is not exceeding the size limit.
        
        This error is used when the file is too large
        or exceeds the size limit.
    """
    error_key = "file_too_large"
    error_name = "FileTooLargeError"

class FileOpenError(CustomExceptionSuper):
    """_summary_

    Args:
        CustomExceptionSuper (_type_): Parent class
        
    How to resolve this error:
        Check if the file is open. 
        Ensure that the file is not being used by another program.
        
        This error is used when the file cannot be
        opened or accessed.
    """
    error_key = "file_open_error"
    error_name = "FileOpenError"
    
class CodeProcessingError(CustomExceptionSuper):
    """_summary_

    Args:
        CustomExceptionSuper (_type_): Parent class
        
    How to resolve this error:
        Check if the code is valid. 
        Ensure that the code is not corrupted or empty.
        
        If that doesn't work then you are shit out of luck.
        This bug came up during development and I fixed it
        by adding a guard clause...what I am trying to say 
        is that IDK how to solve it nor do I know when it happens
    """
    error_key = "code_processing"
    error_name = "CodeProcessingError"


