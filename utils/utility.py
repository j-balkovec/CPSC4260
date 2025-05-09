# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sun Apr 20th, 2025
#
# __file__: analyze.py
#
# __brief__: TODO

# =========
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# =========

import json
import os
import time
import textwrap

from utils.logger import setup_logger

# ==========
utility_logger = setup_logger(name="utility.py_logger", log_file="utility.log")
# ==========

utility_logger.info("utility_logger")


def _read_file_contents(file_name: str) -> str:
    """_summary_

    Args:
        filename (str): The name of the file to read.

    Returns:
        str: The contents of the file.
    """
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()
            utility_logger.info(f"File '{file_name}' read successfully.")
            return content
        
    except ValueError as e:
        with open(file_name, 'rb') as file:
            content = file.read()
            content = content.replace(b'\0', b'')
            return content.decode('utf-8', errors='ignore')


def _save_to_json(analysis_dict: dict, filename: str) -> str:
    """_summary_

    Args:
        analysis_dict (dict): the analysis of the file, obtained from @see 'find_code_smells()'

    Returns:
        _type_: path of the output file (<path>/json/info_<file_name>_<timestamp>.json)
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    json_dir = os.path.join(project_root, "data", "report")
    os.makedirs(json_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(filename))[0]
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    file_name = f"report_{base_name}_{timestamp}.json"
    file_path = os.path.join(json_dir, file_name)

    with open(file_path, "w") as json_file:
        json.dump(analysis_dict, json_file, indent=4)

    utility_logger.info(f"Analysis report saved to '{file_path}'")
    return file_path


def _generate_readable_report(filename: str):
    """_summary_

    Args:
        file_name (str): Name of the JSON report file, @see save_to_json() in 'analyze.py'.
    """
    with open(filename, 'r') as f:
        data = json.load(f)
    
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    report_dir = os.path.join(project_root, "data", "readable")
    base_name = os.path.splitext(os.path.basename(filename))[0]
    output_filename = f"report_{base_name}_readable.txt"
    file_path = os.path.join(report_dir, output_filename)

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
    
    utility_logger.info(f"Readable report saved to '{file_path}'")
    # TODO info messages in color


# Used only during development
def _pretty_print(funcs_dict: dict) -> None:
    """_summary_
    
    Args:
        funcs_dict (dict): Dictionary containing function names and their details.
        
    Returns:
        None
    """
    print("[")
    for i, (name, data) in enumerate(funcs_dict.items()):
        print(f'\n\n  "{name}": {{')
        print(f'    "code": """')
        print(data["text"])
        print(f'    """,')
        print(f'    "start": {data["start"]},')
        print(f'    "end": {data["end"]}')
        print("  }" + ("," if i < len(funcs_dict) - 1 else ""))
    print("\n\n]")


def _pretty_print_debug_dict(debug: dict) -> None:
    """_summary_

    Args:
        debug (dict): Dictionary containing debug details.
    """
    def format_function_text(text: str) -> str:
        lines = text.strip().splitlines()
        return "\n" + "\n".join("                " + line for line in lines)

    result = "{\n"

    result += '    "functions": {\n'
    for name, info in debug.get("functions", {}).items():
        result += f'        "{name}": {{\n'
        result += f'            "start": {info["start"]},\n'
        result += f'            "end": {info["end"]},\n'
        escaped_text = format_function_text(info["text"]).replace('"', '\\"')
        result += f'            "text": "{escaped_text}"\n'
        result += "        },\n"
    if debug.get("functions"):
        result = result.rstrip(",\n") + "\n"
    result += "    },\n"

    result += '    "tokens": {\n'
    for name, tokens in debug.get("tokens", {}).items():
        token_list = json.dumps(tokens, indent=12)
        result += f'        "{name}": {token_list},\n'
    if debug.get("tokens"):
        result = result.rstrip(",\n") + "\n"
    result += "    },\n"

    result += '    "similarities": [\n'
    for sim in debug.get("similarities", []):
        pair_str = json.dumps(sim, indent=8)
        result += f"        {pair_str},\n"
    if debug.get("similarities"):
        result = result.rstrip(",\n") + "\n"
    result += "    ],\n"

    result += '    "duplicates": [\n'
    for dup in debug.get("duplicates", []):
        result += f"        {json.dumps(dup)},\n"
    if debug.get("duplicates"):
        result = result.rstrip(",\n") + "\n"
    result += "    ]\n"

    result += "}\n"
    print(result)