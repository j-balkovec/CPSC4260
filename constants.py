# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sun Apr 20th, 2025
#
# __file__: constants.py
#
# __brief__: TODO

from typing import Set
"""__constants__"""
WINDOW_SIZE: str = "1800x960"
WINDOW_TITLE: str = "Code Smell Detector"

FONT_FAMILY: str = "Menlo"
FONT_SIZE: int = 12

UNI_WIDTH: int = 650
HEIGHT: int = 800

CODE_EDITOR_WIDTH: int = 800

# -- Deprecated
CTK_ENTRY_X_PADDING: int = 50
CTK_ENTRY_Y_PADDING: int = 30
# -- Deprecated

CTK_TEXTBOX_X_PADDING: int = 20
CTK_TEXTBOX_Y_PADDING: int = 20
CTK_BUTTON_X_PADDING: int = 10
CTK_BUTTON_Y_PADDING: int = 10
CTK_LABEL_Y_PADDING: int = 20

# -- Deprecated
ENTER_KEY: str = "<Return>"
# -- Deprecated


# Add guide on how to resolve errors
ERROR_CODES: dict = {
    "file_read": 1001,           
    "corrupt_file": 1002,         
    "file_not_found": 1003,       
    "file_empty": 1004,           
    "file_type_unsupported": 1005,  
    "file_decode_error": 1006,   
    "file_locked": 1007,         
    "file_too_large": 1008,      
    "file_open_error": 1009,     
}

YELLOW_TEXT: str = "\033[33m"
RESET_TEXT: str = "\033[0m"
RED_TEXT: str = "\033[31m"

SIZE_LIMIT: int = 10 * 1024 * 1024  # 10 MB

# Could cause issues
ALLOWED_OPERATORS = {
    '+', '-', '*', '**', '*=', '**=',
    '/', '//', '/=', '//=', '%', '%=',
    '=', '==', '!=', ':=', '<', '>', '<=', '>=',
    '&', '&=', '|', '|=', '^', '^=', '~',
    '<<', '<<=', '>>', '>>=',
    '->', '@', '@='
}

PARAMS_THRESHOLD: int = 3
LENGTH_THRESHOLD: int = 15
DUPS_THRESHOLD: float = 0.76

LOG_COLORS = {
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'bold_red',
    }

CLEANUP_PATHS = {
    "log_analyze": "/Users/jbalkovec/Desktop/CPSC4260/Project/logs/log_analyze.log",
    "file_info": "/Users/jbalkovec/Desktop/CPSC4260/Project/file_info",
    "analysis_report": "/Users/jbalkovec/Desktop/CPSC4260/Project/analysis_report",
    "output": "/Users/jbalkovec/Desktop/CPSC4260/Project/output",
    "readable_report": "/Users/jbalkovec/Desktop/CPSC4260/Project/readable_report"
}