# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sun Apr 20th, 2025
#
# __file__: analyze.py
#
# __brief__: TODO

import re
import math
from constants import (ALLOWED_OPERATORS,
                       PARAMS_THRESHOLD,
                       LENGTH_THRESHOLD,
                       DUPS_THRESHOLD)
import keyword
import json
import os
import time
import textwrap
from exceptions import (CodeProcessingError)
from logger import setup_logger

# ==========
analyze_py_logger = setup_logger(name="analyze.py_logger", log_file="analyze.log")
# ==========

analyze_py_logger.info("hey")

def _read_file_contents(file_name: str) -> str:
    """_summary_

    Args:
        filename (str): The name of the file to read.

    Returns:
        str: The contents of the file.
    """
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            return file.read()
    except ValueError as e:
        with open(file_name, 'rb') as file:
            content = file.read()
            content = content.replace(b'\0', b'')
            return content.decode('utf-8', errors='ignore')
  

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
  
  for line in source_code.splitlines():
      stripped_line = line.strip()
 
      if in_multiline_comment:
          grouped["comments"].append(line)

          if multiline_delimiter in stripped_line:
              in_multiline_comment = False
              multiline_delimiter = None
          continue

      if stripped_line.startswith("#"):
          grouped["comments"].append(line)

      if any(delim in stripped_line for delim in ('"""', "'''")):
          grouped["comments"].append(line)

          if (stripped_line.count('"""') == 2) or (stripped_line.count("'''") == 2):
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
      elif line_without_comment:
          grouped["code"].append(line)
  
  return grouped


def _calculate_code_metrics(info_dict: dict) -> dict:
  """_summary_

  Args:
      info_dict (dict): dictionary containing the lines of code, comments, and blank lines. 
                        Returned by get_lines_dict()

  Returns:
      dict: dictionary with the metrics
  """
  metrics = {
    "LOC": 0,
    "SLOC": 0,
    "Comment Density": 0,
    "Blank Line Density": 0
  }
  
  metrics["LOC"] = len(info_dict["code"])
  metrics["SLOC"] = len(info_dict["comments"]) + len(info_dict["blank_lines"]) + metrics["LOC"]
  metrics["Comment Density"] = round(len(info_dict["comments"]) / metrics["SLOC"], ndigits=3)
  metrics["Blank Line Density"] = round(len(info_dict["blank_lines"]) / metrics["SLOC"], ndigits=3)

  return metrics


def _extract_operators_and_operands(source_code: str) -> dict:
    """_summary_

    Args:
        source_code (str): A long string with all the lines of code.

    Returns:
        dict: A dictionary with the following keys:
            * unique_operators -> set
            * unique_operands  -> set
            * total_operators  -> list
            * total_operands   -> list
    """
    grouped = {
        "unique_operators": set(),
        "unique_operands": set(),
        "total_operators": [],
        "total_operands": [],
    }
    
    inside_multiline_comment = False
    inside_singleline_comment = False

    fstring_pattern = r'f"[^"]*"|f\'[^\']*\''
    multi_operators_pattern = r'(==|!=|<=|>=|&&|\|\|)'    
    
    for line in source_code.splitlines():
        stripped_line = line.strip()
        
        if stripped_line == "":
            continue
        
        if stripped_line.startswith("#"):
            inside_singleline_comment = True
            continue
        
        if stripped_line.startswith(('"""', "'''")):
            inside_multiline_comment = not inside_multiline_comment
            continue

        if inside_multiline_comment:
            continue
        
        line = re.sub(fstring_pattern, "", line)
        line = re.sub(r'"""([^"]|"(?!""))+"""|\'\'\'([^\']|\'(?!\'\'))+\'\'\'', "", line)

        # Remove comment part at the end of the line
        code_part = re.sub(r'\s*#.*$', '', line).strip()
        
        if code_part.strip():
          multi_ops = re.findall(multi_operators_pattern, code_part)
          for op in multi_ops:
              grouped["total_operators"].append(op)
              grouped["unique_operators"].add(op)

          for char in code_part:
              if char in ALLOWED_OPERATORS:
                grouped["total_operators"].append(char)
                grouped["unique_operators"].add(char)
                
          tokens = re.findall(r'\b\w+\b', code_part)

          for token in tokens:
              if token in keyword.kwlist or token.isdigit():
                  continue
              grouped["total_operands"].append(token)
              grouped["unique_operands"].add(token)

        else:
          raise CodeProcessingError("Failed to parse the code", function="_extract_operators_and_operands", source_code=source_code)
          
    return grouped


def _calculate_halstead_metrics(info_dict: dict) -> dict:
  """_summary_

  Args:
      info_dict (dict): dictionary returned from group_lines() 
                        with all the necessary parameters

  Returns:
      dict: dictionary with halstead metrics
      
  Formulas:      
      Length (N) = N1 + N2
      Vocabulary (n) = n1 + n2
      Volume (V) = N * log2(n)
      Difficulty (D) = (n1/2) * (N2/n2)
      Program Length (HN) = n1 * log2(n1) + n2 * log2(n2)
      Effort (E) = D * V
      Time (T) = E / 18
      Bugs (B) = E / 3000
      Maintainability (M) = 171 - 5.2 * log2(V) - 0.23 * D - 16.2 * log2(N)
  """

  halstead_metrics = {
    "n1": len(info_dict["unique_operators"]),
    "n2": len(info_dict["unique_operands"]),
    "N1": len(info_dict["total_operators"]),
    "N2": len(info_dict["total_operands"]),
    
    "N": 0,
    "n": 0,
    "V": 0,
    "D": 0,
    "HN": 0,
    "E": 0,
    "T": 0,
    "B": 0,
    "M": 0,
  }
  
  n1 = halstead_metrics["n1"]
  n2 = halstead_metrics["n2"]
  N1 = halstead_metrics["N1"]
  N2 = halstead_metrics["N2"]
  
  length = N1 + N2
  vocabulary = n1 + n2
  volume = length * math.log2(vocabulary) if vocabulary > 0 else 0
  difficulty = (n1 / 2) * (N2 / n2) if n2 > 0 else 0
  program_length = n1 * math.log2(n1) + n2 * math.log2(n2) if n1 > 0 and n2 > 0 else 0
  effort = difficulty * volume
  time = effort / 18
  bugs = effort / 3000
  maintainability = 171 - 5.2 * math.log2(volume) - 0.23 * difficulty - 16.2 * math.log2(length) if length > 0 and volume > 0 else 0
  
  halstead_metrics["N"] = length
  halstead_metrics["n"] = vocabulary
  halstead_metrics["V"] = round(volume, ndigits=3)
  halstead_metrics["D"] = round(difficulty, ndigits=3)
  halstead_metrics["HN"] = round(program_length, ndigits=3)
  halstead_metrics["E"] = round(effort, ndigits=3)
  halstead_metrics["T"] = round(time, ndigits=3)
  halstead_metrics["B"] = round(bugs, ndigits=3)
  halstead_metrics["M"] = round(maintainability, ndigits=3)
  
  return halstead_metrics


def code_metrics(file_name: str) -> dict:
  """_summary_
  
  Note:
      Abstract the details from the client
  
  Args:
      file_name (str): _description_
  Returns:
      _type_: @see _calculate_code_metrics()
  """
  raw_code = _read_file_contents(file_name)
  classified_lines = _classify_lines_of_code(raw_code)
  code_metrics = _calculate_code_metrics(classified_lines)
  
  return code_metrics
  
  
def halstead_metrics(file_name: str) -> dict:
  """_summary_

  Note:
      Abstract the details from the client
  
  Args:
      file_name (str): _description_
      
  Returns:
      _type_: @see _calculate_halstead_metrics()
  """
  raw_code = _read_file_contents(file_name)
  lines = _extract_operators_and_operands(raw_code)
  halstead_metrics = _calculate_halstead_metrics(lines)
  
  return halstead_metrics
 
 
def _find_long_parameter_list(source_code: str) -> list:
    """_summary_

    Args:
        source_code (str): code returned form "_read_file_contents()"

    Returns:
        list: list of all instances where a method has more than <PARAMS_THRESHOLD> parameters
    """
    tokens = re.findall(r'\w+|[()]', source_code)
    long_parameter_methods = []
    
    i = 0
    while i < len(tokens):
        if tokens[i] == "def":
            if i + 1 < len(tokens):
                function_name = tokens[i + 1]
            else:
                function_name = "<NOT FOUND>"
                
            while i < len(tokens) and tokens[i] != "(":
                i += 1
            if i >= len(tokens):
                break  
            
            i += 1
            num_params = 0
            
            while i < len(tokens) and tokens[i] != ")":
                if tokens[i] not in (',',):
                    num_params += 1
                i += 1
            
            if num_params > PARAMS_THRESHOLD:
                found_method = f"Function: \n\tposition: {i}, \n\tname: {function_name}, \n\tparameters: {num_params},\n which exceeds the threshold of {PARAMS_THRESHOLD}"
                long_parameter_methods.append({
                        "function": function_name,
                        "position": i,
                        "params_count": num_params,
                        "threshold": PARAMS_THRESHOLD
                    })
        i += 1
    
    return long_parameter_methods


def _find_long_method(source_code: str) -> list:
    """_summary_

    Args:
        source_code (str): code returned form "_read_file_contents()"

    Returns:
        list: list of all instances where a method is longer than <LENGTH_THRESHOLD>
    """
    long_methods = []
    lines = source_code.split('\n')
    
    in_function = False
    start_line = 0
    function_indent = 0
    function_name = ""
    
    for idx, line in enumerate(lines):
        stripped = line.strip()

        if re.match(r'(async\s+)?def\s+\w+', stripped):
            if in_function:
                end_line = idx - 1
                method_length = end_line - start_line + 1
                if method_length > LENGTH_THRESHOLD:
                    long_methods.append({
                        "function": function_name,
                        "start_line": start_line + 1,
                        "end_line": end_line + 1,
                        "length": method_length,
                        "threshold": LENGTH_THRESHOLD
                    })
            in_function = True
            start_line = idx
            function_indent = len(line) - len(line.lstrip())
            match = re.match(r'(async\s+)?def\s+(\w+)', stripped)
            if match:
                function_name = match.group(2)
            continue

        if in_function:
            current_indent = len(line) - len(line.lstrip())

            if current_indent < function_indent and stripped:
                end_line = idx - 1
                method_length = end_line - start_line + 1
                if method_length > LENGTH_THRESHOLD:
                    long_methods.append({
                        "function": function_name,
                        "start_line": start_line + 1,
                        "end_line": end_line + 1,
                        "length": method_length,
                        "threshold": LENGTH_THRESHOLD
                    })
                in_function = False
                function_name = ""

    if in_function:
        end_line = len(lines) - 1
        method_length = end_line - start_line + 1
        if method_length > LENGTH_THRESHOLD:
            long_methods.append({
                "function": function_name,
                "start_line": start_line + 1,
                "end_line": end_line + 1,
                "length": method_length,
                "threshold": LENGTH_THRESHOLD
            })

    return long_methods

def _split_into_blocks(source_code: str) -> list:
    """_summary_

    Args:
        source_code (str): source code to be processed

    Returns:
        list: list of code blocks with their starting line numbers
    """
    lines = source_code.splitlines()
    blocks = []
    current_block = []
    current_indent = 0
    start_line = 1
    in_control_structure = False

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped:
            continue  
        indent_level = len(line) - len(line.lstrip())

        is_control_start = stripped.startswith(('if ', 'elif ', 'else:', 'for ', 'while ', 'try:', 'except ', 'finally:'))
        is_control_end = indent_level < current_indent and current_block and in_control_structure

        if (stripped.startswith(('def ', 'class ')) or
            is_control_start or
            (current_block and indent_level < current_indent and not in_control_structure)):
            if current_block:
                block_text = "\n".join(current_block).strip()
                if len(current_block) >= 3 and not block_text.startswith('return '):
                    blocks.append((block_text, start_line))
            current_block = [line]
            start_line = i
            current_indent = indent_level
            in_control_structure = is_control_start
        else:
            current_block.append(line)
            if is_control_start:
                in_control_structure = True
            elif indent_level <= current_indent and in_control_structure:
                in_control_structure = False

    if current_block:
        block_text = "\n".join(current_block).strip()
        if len(current_block) >= 3 and not block_text.startswith('return '):
            blocks.append((block_text, start_line))

    return blocks
    

def _remove_comments(source_code: str) -> str:
    """_summary_
    
    Args:
        source_code (str): source code to be processed
        
    Returns:
        str: source code without comments
    """
    code = re.sub(r'(""".*?"""|\'\'\'.*?\'\'\')', '', source_code, flags=re.DOTALL)
    lines = code.splitlines()
    cleaned_lines = []
    for line in lines:
        in_string = False
        for i, char in enumerate(line):
            if char in ('"', "'") and line[i-1:i] != "\\":
                in_string = not in_string
            elif char == '#' and not in_string:
                line = line[:i].rstrip()
                break
        if line.strip():
            cleaned_lines.append(line)
    return "\n".join(cleaned_lines)   


def _tokenize_block(block: str) -> set:
    """_summary_

    Args:
        block (str): code block to be tokenized

    Returns:
        set: set of tokens
    """
    block = re.sub(r'\b[A-Za-z_]\w*\b', 'VAR', block)
    tokens = re.findall(r'\w+|[+\-*/=<>!&|%^~]+|[()\[\]{},;.:]', block)
    return set(tokens)

def _jaccard_similarity(set1: set, set2: set) -> float:
    """_summary_

    Args:
        set1 (set): set A
        set2 (set): set B

    Returns:
        float: similarity score
    """
    intersection = set1 & set2
    union = set1 | set2
    if not union:
        return 0.0
    return len(intersection) / len(union)

# Catch error in main
def _find_duplicated_code(source_code: str) -> list:
    """_summary_

    Args:
        source_code (str): code returned form "_read_file_contents()"

    Returns:
        list: list of all instances where a method has more than <DUPS_THRESHOLD> parameters
    """
    cleaned_code = _remove_comments(source_code)
    if not cleaned_code.strip():
        raise CodeProcessingError("No valid code after removing comments", function="_remove_comments", source_code=source_code)

    blocks = _split_into_blocks(cleaned_code)
    if len(blocks) < 2:
        raise CodeProcessingError("Not enough code blocks to compare for duplication", function="_split_into_blocks", source_code=source_code)

    tokenized_blocks = [(_tokenize_block(block), block, line_num) for block, line_num in blocks]
    duplicates = []

    for i in range(len(tokenized_blocks)):
        for j in range(i + 1, len(tokenized_blocks)):
            tokens_i, block_i, line_i = tokenized_blocks[i]
            tokens_j, block_j, line_j = tokenized_blocks[j]
            sim = _jaccard_similarity(tokens_i, tokens_j)
            if sim >= DUPS_THRESHOLD:
                duplicates.append({
                    'block1': {'index': i,
                               'text': block_i,
                               'type': 'code', # formatting purposes TODO
                               'tokens': list(tokens_i),
                               'line_number': line_i},
                    
                    'block2': {'index': j,
                               'text': block_j,
                               'type': 'code', # formatting purposes TODO
                               'tokens': list(tokens_j),
                               'line_number': line_j},
                    'similarity': sim,
                    'threshold': DUPS_THRESHOLD
                })

    return duplicates


def _save_to_json(analysis_dict: dict, filename: str) -> str:
    """_summary_

    Args:
        analysis_dict (dict): the analysis of the file, obtained from @see 'find_code_smells()'

    Returns:
        _type_: path of the output file (<path>/json/info_<file_name>_<timestamp>.json)
    """
    
    json_dir = os.path.join(os.getcwd(), "analysis_report")
    os.makedirs(json_dir, exist_ok=True)

    base_name = os.path.basename(filename) 
    base_name = os.path.splitext(base_name)[0]
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    file_name = f"report_{base_name}_{timestamp}.json"
    file_path = os.path.join(json_dir, file_name)

    with open(file_path, "w") as json_file:
        json.dump(analysis_dict, json_file, indent=4)

    return file_path

def _generate_readable_report(file_name: str):
    """_summary_

    Args:
        file_name (str): Name of the JSON report file, @see save_to_json() in 'analyze.py'.
    """
    with open(file_name, 'r') as f:
        data = json.load(f)
    
    report_dir = os.path.join(os.getcwd(), "readable_report")
    base_name = os.path.basename(file_name)
    base_name = os.path.splitext(base_name)[0]
    output_file_name = f"report_{base_name}_readable.txt"
    file_path = os.path.join(report_dir, output_file_name)

    os.makedirs(report_dir, exist_ok=True)
    
    with open(file_path, 'w') as out:
        out.write("===== SOFTWARE ANALYSIS REPORT =====\n\n")
        
        out.write(">> Long Parameter List Detections:\n\n")
        for item in data.get('long_parameter_list', []):
            out.write(f"  - Function '{item['function']}' at line {item['position']}\n")
            out.write(f"    * Parameters: {item['params_count']} (Threshold: {item['threshold']})\n\n")
        
        out.write(">> Long Method Detections:\n\n")
        for item in data.get('long_method', []):
            out.write(f"  - Function '{item['function']}' from line {item['start_line']} to {item['end_line']}\n")
            out.write(f"    * Length: {item['length']} lines (Threshold: {item['threshold']})\n\n")
        
        out.write(">> Duplicated Code Detections:\n\n")
        for idx, item in enumerate(data.get('duplicated_code', []), 1):
            out.write(f"  - Duplicate {idx}: (Similarity: {item['similarity']:.2f})\n")
            
            block1_text = textwrap.dedent(item['block1']['text']).strip()
            block2_text = textwrap.dedent(item['block2']['text']).strip()
            
            block1_lines = block1_text.splitlines()
            block2_lines = block2_text.splitlines()
            
            out.write(f"    * Block 1 (Line {item['block1']['line_number']}):\n")
            for line in block1_lines:
                out.write(f"        {line}\n")
            
            out.write(f"    * Block 2 (Line {item['block2']['line_number']}):\n")
            for line in block2_lines:
                out.write(f"        {line}\n")
            
            out.write("\n")
        
        out.write("===== END OF REPORT =====\n")
    
    # TODO info messages in color

def find_code_smells(file_name: str) -> dict:
    """_summary_

    Raises:
        TypeError: _description_

    Returns:
        dict: _description_
    """
    source_code = _read_file_contents(file_name)
    code_smells = {
        "long_parameter_list": [],
        "long_method": [],
        "duplicated_code": [],
    }
    
    code_smells["long_parameter_list"] = _find_long_parameter_list(source_code)
    code_smells["long_method"] = _find_long_method(source_code)
    code_smells["duplicated_code"] = _find_duplicated_code(source_code)
            
    raw_json = _save_to_json(code_smells, file_name)
    _generate_readable_report(raw_json)
    
    return code_smells




# ================================ TO BE REMOVED ================================ 
FILE = "/Users/jbalkovec/Desktop/CPSC4260/Project/tests/test4.py"
find_code_smells(FILE)
# ================================ TO BE REMOVED ================================ 

