# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sun Apr 20th, 2025
#
# __file__: analyze.py
#
# __brief__: This file contains the utility functions used throughout the project.

# =========
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# =========

import json
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
        with open(file_name, "r", encoding="utf-8") as file:
            content = file.read()
            utility_logger.info("File '%s' read successfully.", file_name)
            return content

    except ValueError as e:
        utility_logger.error(e)
        with open(file_name, "rb", encoding="utf-8") as file:
            content = file.read()
            content = content.replace(b"\0", b"")
            return content.decode("utf-8", errors="ignore")


def _save_to_json(analysis_dict: dict, filename: str) -> str:
    """_summary_

    Args:
        analysis_dict (dict): the analysis of the file, obtained from @see 'find_code_smells()'

    Returns:
        _type_: path of the output file (<path>/json/info_<file_name>_<timestamp>.json)
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    json_dir = os.path.join(project_root, "data", "report")
    os.makedirs(json_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(filename))[0]
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    file_name = f"report_{base_name}_{timestamp}.json"
    file_path = os.path.join(json_dir, file_name)

    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(analysis_dict, json_file, indent=4)

    utility_logger.info("Analysis report saved to: %s", file_name)
    return file_path


def get_code_metric_description(metric):
    """_summary_

    Args:
        metric (_type_): metric to get the description for

    Returns:
        _type_: description of the metric
    """
    descriptions = {
        "LOC": "Lines of Code",
        "SLOC": "Source Lines of Code",
        "Comment Density": "Proportion of comment lines to total lines",
        "Blank Line Density": "Proportion of blank lines to total lines",
    }
    return descriptions.get(metric, "No description available")


def get_halstead_metric_description(metric):
    """_summary_

    Args:
        metric (_type_): metric to get the description for

    Returns:
        _type_: description of the metric
    """
    descriptions = {
        "n1": "Number of unique operators",
        "n2": "Number of unique operands",
        "N1": "Total occurrences of operators",
        "N2": "Total occurrences of operands",
        "N": "Total number of operators and operands (N1 + N2)",
        "n": "Total number of distinct operators and operands (n1 + n2)",
        "V": "Volume (size of the implementation)",
        "D": "Difficulty (how difficult the program is to understand)",
        "HN": "Halstead's number (product of difficulty and volume)",
        "E": "Effort (estimated mental effort)",
        "T": "Time (estimated time to understand the program)",
        "B": "Bugs (estimated number of bugs in the program)",
        "M": "Vocabulary (unique operators and operands used)",
    }
    return descriptions.get(metric, "No description available")


def _generate_readable_report(code_analysis_dict_path: dict) -> str:
    """_summary_

    Args:
        code_smells_filename (str): filename containing the code smells
        code_metrics_filename (str): filename containing the code metrics
        halstead_metrics_filename (str): filename containing the halstead metrics
    """

    # Code smells
    with open(code_analysis_dict_path, "r", encoding="utf-8") as f:
        analysis_dict = json.load(f)

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    report_dir = os.path.join(project_root, "data", "readable")
    base_name = os.path.splitext(os.path.basename(code_analysis_dict_path))[0]
    output_filename = f"report_{base_name}_readable.md"
    file_path = os.path.join(report_dir, output_filename)

    os.makedirs(report_dir, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as out:
        out.write("# ===== SOFTWARE ANALYSIS REPORT =====\n\n")
        out.write("---\n")

        # ================ CODE METRICS =================
        out.write("## Code Metrics:\n\n")

        code_metrics = analysis_dict.get("code_metrics", {})
        if code_metrics:
            out.write("| Metric | Description | Value |\n")
            out.write("|--------|-------------|-------|\n")

            for metric, value in code_metrics.items():
                description = get_code_metric_description(metric)
                out.write(f"| `{metric}` | {description} | `{value}` |\n")

            out.write("\n")
        else:
            out.write("*No code metrics found.*\n\n")
        # ===============================================

        out.write("---\n")

        # ============== HALSTEAD METRICS ===============
        out.write("## Halstead Metrics:\n\n")
        halstead_metrics = analysis_dict.get("halstead_metrics", {})
        if halstead_metrics:
            out.write("| Metric | Description | Value |\n")
            out.write("|--------|-------------|-------|\n")

            for metric, value in halstead_metrics.items():
                description = get_halstead_metric_description(metric)
                out.write(f"| `{metric}` | {description} | `{value}` |\n")

            out.write("\n")
        else:
            out.write("*No Halstead metrics found.*\n\n")
        out.write("\n")
        # ===============================================

        out.write("---\n")

        # ============= LONG PARAM LIST =================
        out.write("### Long Parameter List Detections:\n\n")
        items = analysis_dict.get("long_parameter_list", [])
        if len(items) == 0:
            out.write("  - *No functions with long parameter lists were found.*\n\n")
        else:
            for item in items:
                out.write(
                    f"  - Function `'{item['function']}'` at line `{item['position']}`\n"
                )
                out.write(
                    f"    * **Parameters**: `{item['params_count']}`, Threshold: `{item['threshold']}`\n\n"
                )
        # ===============================================

        out.write("---\n")

        # ================ LONG METHOD ==================
        out.write("### Long Method Detections:\n\n")
        items = analysis_dict.get("long_method", [])
        if len(items) == 0:
            out.write("  - *No long methods were found.*\n\n")
        else:
            for item in items:
                out.write(
                    f"  - Function `'{item['function']}'` from line `{item['start_line']}` to `{item['end_line']}`\n"
                )
                out.write(
                    f"    * **Length**: `{item['length']} lines`, Threshold: `{item['threshold']}`\n\n"
                )
        # ===============================================

        out.write("---\n")

        # ============== DUPLICATED CODE ================
        out.write("### Duplicated Code Detections:\n\n")
        items = analysis_dict.get("duplicated_code", [])
        if len(items) == 0:
            out.write("  - *No duplicated code was found.*\n\n")
        else:
            for idx, item in enumerate(items, 1):
                out.write(
                    f"##### Duplicate {idx}, **Similarity**: `{item['similarity']:.2f}`\n"
                )

                block1_text = textwrap.dedent(item["block1"]["text"]).strip()
                block2_text = textwrap.dedent(item["block2"]["text"]).strip()

                block1_lines = block1_text.splitlines()
                block2_lines = block2_text.splitlines()

                out.write(f" - **Block 1** `(Line {item['block1']['line_number']})`:\n")
                out.write("```\n")
                for line in block1_lines:
                    out.write(f"        {line}\n")
                out.write("```\n")

                out.write(f" - **Block 2** `(Line {item['block2']['line_number']})`:\n")
                out.write("```\n")
                for line in block2_lines:
                    out.write(f"        {line}\n")
                out.write("```\n")
                out.write("\n")
        # =============================================

        out.write("---\n")
        out.write("# ===== END OF REPORT =====\n")

    utility_logger.info("Readable report saved to: %s ", file_path)
    return file_path


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
        print('    "code": """')
        print(data["text"])
        print('    """,')
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


def _pretty_print_raw_string_func(code: tuple) -> str:
    """
    YOINKED FROM SOME DUDE ON STACKOVERFLOW
        Link: https://stackoverflow.com/questions/1024435/how-to-fix-python-indentation
    """
    code_str = code[0]
    dedented_code = textwrap.dedent(code_str).strip()

    lines = dedented_code.split('\n')
    result = []
    indent_level = 0
    indent_size = 4

    print(lines)

    for i, line in enumerate(lines):
        line_stripped = line.strip()

        if not line_stripped:
            result.append(line)
            continue

        if line_stripped.startswith(('elif ', 'else:', 'except ', 'finally:', 'return ', 'raise ', 'break', 'continue')):

            if not (line_stripped == 'else:' and lines[i-1].strip().endswith(':')) :
                indent_level = max(0, indent_level - 1)

        current_indent = ' ' * (indent_level * indent_size)
        result.append(current_indent + line_stripped)

        if line_stripped.endswith(':'):
            indent_level += 1

    return '\n'.join(result)
