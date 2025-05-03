# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sun Apr 20th, 2025
#
# __file__: code_metrics.py
#
# __brief__: TODO -> log

import re

from logger import setup_logger
from utility import (_read_file_contents)


# ==========
code_metrics_logger = setup_logger(name="code_metrics.py_logger", log_file="code_metrics.log")
# ==========

code_metrics_logger.info("code_metrics_logger")

def _classify_lines_of_code(source_code: str) -> dict:
  """_summary_
  
  Args:
      source_code (str): The source code as a string.
      
  Returns:
      dict: A dictionary containing the lines of code, comments, and blank lines.
      
  Notes:
      - The function groups lines of code into comments, blank lines, and actual code.
      - It handles single-line comments, multi-line comments, and blank lines.
        
      flag (in_multiline_comment): if in a multiline comment or not
      delimiter (multiline_delimiter): to track if it starts with either \'\'\' or \"\"\"
  """
  
  in_multiline_comment = False
  multiline_delimiter = None
  
  grouped = {
    "comments": [],
    "blank_lines": [],
    "code": []
  }
  
  for line_number, line in enumerate(source_code.splitlines(), start=1):
      stripped_line = line.strip()
 
      if in_multiline_comment:
          grouped["comments"].append(line)
          code_metrics_logger.debug(f"[Line {line_number}] Inside multi-line comment.")

          if multiline_delimiter in stripped_line:
              in_multiline_comment = False
              multiline_delimiter = None
              code_metrics_logger.debug(f"[Line {line_number}] Exiting multi-line comment.")
          continue

      if stripped_line.startswith("#"):
          grouped["comments"].append(line)
          code_metrics_logger.debug(f"[Line {line_number}] Single-line comment.")
          continue

      if any(delim in stripped_line for delim in ('"""', "'''")):
          grouped["comments"].append(line)
          code_metrics_logger.debug(f"[Line {line_number}] Multi-line comment start.")

          if (stripped_line.count('"""') == 2) or (stripped_line.count("'''") == 2):
              code_metrics_logger.debug(f"[Line {line_number}] Complete multi-line comment on same line.")
              in_multiline_comment = False
              multiline_delimiter = None
          else:
              in_multiline_comment = True
              if '"""' in stripped_line:
                  multiline_delimiter = '"""'
              else:
                  multiline_delimiter = "'''"
          continue
        
      line_without_comment = re.sub(r'\s*#.*$', '', line).strip()

      if stripped_line == "":
          grouped["blank_lines"].append(line)
          code_metrics_logger.debug(f"[Line {line_number}] Blank line.")
      elif line_without_comment:
          grouped["code"].append(line)
          code_metrics_logger.debug(f"[Line {line_number}] Code line.")
          
  code_metrics_logger.info(f"Line classification completed: "
                           f"{len(grouped['code'])} code, "
                           f"{len(grouped['comments'])} comments, "
                           f"{len(grouped['blank_lines'])} blank lines.")
  return grouped


def _calculate_code_metrics(info_dict: dict) -> dict:
  """_summary_

  Args:
      info_dict (dict): dictionary containing the lines of code, comments, and blank lines. 
                        Returned by get_lines_dict()

  Returns:
      dict: dictionary with the metrics
  """
  code_metrics_logger.debug("Calculating code metrics.")

  metrics = {
      "LOC": 0,
      "SLOC": 0,
      "Comment Density": 0,
      "Blank Line Density": 0
    }

  metrics["LOC"] = len(info_dict["code"])
  metrics["SLOC"] = len(info_dict["comments"]) + len(info_dict["blank_lines"]) + metrics["LOC"]

  if metrics["SLOC"] > 0:
     metrics["Comment Density"] = round(len(info_dict["comments"]) / metrics["SLOC"], ndigits=3)
     metrics["Blank Line Density"] = round(len(info_dict["blank_lines"]) / metrics["SLOC"], ndigits=3)

  code_metrics_logger.info(f"Metrics calculated: {metrics}")
  return metrics

def fetch_code_metrics(file_name: str) -> dict:
  """_summary_
  
  Note:
      Abstract the details from the client
  
  Args:
      file_name (str): _description_
  Returns:
      _type_: @see _calculate_code_metrics()
  """
  code_metrics_logger.info(f"Fetching metrics for file: {file_name}")

  raw_code = _read_file_contents(file_name)
  code_metrics_logger.debug(f"Read {len(raw_code.splitlines())} lines from file.")

  classified_lines = _classify_lines_of_code(raw_code)
  code_metrics = _calculate_code_metrics(classified_lines)

  code_metrics_logger.info(f"Completed metrics extraction for file: {file_name}")

  return code_metrics

