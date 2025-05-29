# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sun Apr 20th, 2025
#
# __file__: duplicated_code.py
#
# __brief__: This file contains the logic for finding duplicated code blocks in a given source code.

# =========
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# =========


import re
import keyword
import ast
import io
import tokenize
import textwrap
import json
from collections import defaultdict

from core.constants import DUPS_THRESHOLD
from utils.logger import setup_logger


# ==========
duplicated_code_logger = setup_logger(
    name="duplicated_code.py_logger", log_file="duplicated_code.log"
)
# ==========

duplicated_code_logger.info("duplicated_code_logger")

def _normalize_indentation(text: str) -> str:
    """
    Normalize indentation by replacing tabs with spaces and dedenting the text.

    Args:
        text (str): Input text to normalize

    Returns:
        str: Normalized text with consistent indentation
    """
    # Replace tabs with 4 spaces
    text = text.replace("\t", "    ")
    try:
        # Dedent to remove common leading whitespace
        text = textwrap.dedent(text)
    except textwrap.TextWrapError as e:
        duplicated_code_logger.warning(f"Failed to dedent text: {e}")
    return text

def _validate_indentation(text: str) -> bool:
    """
    Validate indentation in the text to detect issues like mixed tabs/spaces or invalid unindents.

    Args:
        text (str): Input text to validate

    Returns:
        bool: True if indentation is valid, False otherwise
    """
    lines = text.splitlines()
    indent_levels = []
    for i, line in enumerate(lines, 1):
        if not line.strip():  # Skip empty lines
            continue
        leading_ws = len(line) - len(line.lstrip())
        # Check for mixed tabs and spaces
        if "\t" in line[:leading_ws] and " " in line[:leading_ws]:
            duplicated_code_logger.warning(f"Mixed tabs and spaces in line {i}: {line}")
            return False
        # Track indentation levels for non-empty lines
        if indent_levels and leading_ws < indent_levels[-1]:
            if leading_ws not in indent_levels[:-1]:
                duplicated_code_logger.warning(f"Invalid unindent in line {i}: {line}")
                return False
        indent_levels.append(leading_ws)
    return True

def _normalize_block(text: str) -> str:
    """
    Normalize a block of text by stripping empty lines and normalizing indentation.

    Args:
        text (str): Block of text to normalize

    Returns:
        str: Normalized block
    """
    lines = text.splitlines()
    norm_lines = [line for line in lines if line.strip()]  # Keep only non-empty lines
    return "\n".join(norm_lines)

def _split_into_blocks(source_code: str) -> list:
    """
    Split source code into blocks based on control structures and indentation.

    Args:
        source_code (str): Source code to process

    Returns:
        list: List of (code_block_text, starting_line_number) tuples
    """
    # Normalize indentation before splitting
    source_code = _normalize_indentation(source_code)

    # Validate indentation
    if not _validate_indentation(source_code):
        duplicated_code_logger.warning("Invalid indentation in source code; attempting to process anyway")

    lines = source_code.splitlines()
    blocks = []
    func_map = defaultdict(list)
    current_block = []
    current_indent = None
    start_line = 0
    current_func_name = None

    def flush_block():
        nonlocal current_block, start_line, current_func_name
        if current_block:
            non_empty = [l for l in current_block if l.strip()]
            if len(non_empty) >= 2:  # Only include blocks with at least 2 non-empty lines
                block_text = "\n".join(current_block).rstrip()
                blocks.append((block_text, start_line))
                if current_func_name:
                    func_map[current_func_name].append((block_text, start_line))
            current_block = []
            current_func_name = None

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped:
            if current_block:
                current_block.append(line)
            continue

        indent = len(line) - len(line.lstrip())
        is_new_block = stripped.startswith(
            (
                "def ",
                "class ",
                "for ",
                "while ",
                "if ",
                "elif ",
                "else:",
                "try:",
                "except",
                "finally:",
                "with ",
            )
        )

        if is_new_block or (
            current_block and indent <= current_indent and not line.startswith(" ")
        ):
            flush_block()

        if not current_block:
            start_line = i
            current_indent = indent
            if stripped.startswith("def "):
                match = re.match(r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)", stripped)
                if match:
                    current_func_name = match.group(1)

        current_block.append(line)

    flush_block()

    # Check for duplicates within functions
    for name, entries in func_map.items():
        seen = set()
        for i in range(len(entries)):
            for j in range(i + 1, len(entries)):
                block_i = _normalize_block(entries[i][0])
                block_j = _normalize_block(entries[j][0])
                if block_i == block_j and block_i and block_j:
                    if (block_i, block_j) not in seen:
                        seen.add((block_i, block_j))
                        duplicated_code_logger.info(
                            f"[DUPLICATE FUNC] Function '{name}' duplicated at lines {entries[i][1]} and {entries[j][1]}"
                        )

    return blocks

def _remove_comments(source_code: str) -> str:
    """
    Remove comments from source code.

    Args:
        source_code (str): Source code to process

    Returns:
        str: Source code without comments
    """
    # Remove multi-line strings/comments
    code = re.sub(r'(""".*?"""|\'\'\'.*?\'\'\')', "", source_code, flags=re.DOTALL)
    lines = code.splitlines()
    cleaned_lines = []
    for line in lines:
        in_string = False
        for i, char in enumerate(line):
            if char in ('"', "'") and line[i - 1 : i] != "\\":
                in_string = not in_string
            elif char == "#" and not in_string:
                line = line[:i].rstrip()
                break
        if line.strip():
            cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

# ==================================================================================================================================

def _tokenize_block(block: str) -> list:
    """
    Tokenize a block of Python code using both AST and tokenize.

    Args:
        block (str): Block of code to tokenize

    Returns:
        list: List of normalized tokens
    """
    tokens = []

    # === Helper: Normalize indentation ===
    def normalize_indentation(block: str) -> str:
        """_summary_

        Args:
            block (str): block of code to normalize

        Returns:
            str: normalized block of code
        """
        block = block.replace("\t", "    ")
        try:
            block = textwrap.dedent(block)
        except textwrap.TextWrapError as e:
            duplicated_code_logger.warning(f"Failed to dedent block: {e}")
            return block
        return block

    # === Helper: Validate indentation ===
    def validate_indentation(block: str) -> bool:
        """_summary_

        Args:
            block (str): block of code to validate

        Returns:
            bool: True if indentation is valid, False otherwise
        """
        lines = block.splitlines()
        indent_levels = []
        for i, line in enumerate(lines, 1):
            if not line.strip():
                continue
            leading_ws = len(line) - len(line.lstrip())
            if "\t" in line[:leading_ws] and " " in line[:leading_ws]:
                duplicated_code_logger.warning(f"Mixed tabs and spaces in line {i}: {line}")
                return False
            if indent_levels and leading_ws < indent_levels[-1]:
                if leading_ws not in indent_levels[:-1]:
                    duplicated_code_logger.warning(f"Invalid unindent in line {i}: {line}")
                    return False
            indent_levels.append(leading_ws)
        return True

    # === Helper: AST-based tokens ===
    def extract_ast_tokens(source: str) -> list:
        """_summary_

        Args:
            source (str): block of code to extract AST tokens from

        Returns:
            list: list of AST tokens
        """
        try:
            tree = ast.parse(source)
        except SyntaxError:
            duplicated_code_logger.warning(f"AST parsing failed for block: {source}")
            return ["SYNTAX_ERROR"]

        ast_tokens = []

        def binop_token(op):
            """_summary_

            Args:
                op (_type_): binary operation node

            Returns:
                _type_: string representation of the binary operation
            """
            return {
                ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.Div: "/",
                ast.Mod: "%", ast.Pow: "**", ast.FloorDiv: "//"
            }.get(type(op), "BINOP")

        def cmp_token(op):
            """_summary_

            Args:
                op (_type_): comparison operation node

            Returns:
                _type_: string representation of the comparison operation
            """
            return {
                ast.Eq: "==", ast.NotEq: "!=", ast.Lt: "<", ast.LtE: "<=",
                ast.Gt: ">", ast.GtE: ">=", ast.Is: "is", ast.IsNot: "is not",
                ast.In: "in", ast.NotIn: "not in"
            }.get(type(op), "CMP")

        def unary_token(op):
            """_summary_

            Args:
                op (_type_): unary operation node

            Returns:
                _type_: string representation of the unary operation
            """
            return {
                ast.UAdd: "+", ast.USub: "-", ast.Not: "not", ast.Invert: "~"
            }.get(type(op), "UNARYOP")

        for node in ast.walk(tree):
            match type(node):
                case ast.FunctionDef | ast.AsyncFunctionDef:
                    ast_tokens.append("def")
                    ast_tokens.append("VAR")
                    ast_tokens.extend(["VAR"] * len(node.args.args))
                case ast.Call:
                    ast_tokens.append("call")
                    ast_tokens.append("VAR")
                case ast.Assign | ast.AnnAssign:
                    ast_tokens.append("=")
                case ast.BinOp:
                    ast_tokens.append(binop_token(node.op))
                case ast.UnaryOp:
                    ast_tokens.append(unary_token(node.op))
                case ast.Compare:
                    for op in node.ops:
                        ast_tokens.append(cmp_token(op))
                case ast.Return:
                    ast_tokens.append("return")
                case ast.Constant:
                    if isinstance(node.value, str):
                        ast_tokens.append("STR")
                    elif isinstance(node.value, (int, float)):
                        ast_tokens.append("NUM")
                    elif node.value is None:
                        ast_tokens.append("None")
                    elif isinstance(node.value, bool):
                        ast_tokens.append(str(node.value))
                case ast.Name:
                    ast_tokens.append("VAR")
                case ast.If | ast.For | ast.While | ast.With | ast.Try:
                    ast_tokens.append(node.__class__.__name__.lower())
                case _:
                    pass

        return ast_tokens

    # === Helper: tokenize module tokens ===
    def extract_tokenize_tokens(source: str) -> list:
        """_summary_

        Args:
            source (str): block of code to tokenize

        Returns:
            list: list of tokens extracted using the tokenize module
        """
        tok_list = []
        try:
            token_stream = tokenize.generate_tokens(io.StringIO(source).readline)
            for tok_type, tok_str, *_ in token_stream:
                if tok_type == tokenize.NAME:
                    if tok_str in {"True", "False", "None"}:
                        tok_list.append(tok_str)
                    elif tok_str in {"def", "return", "if", "else", "for", "while", "with", "try", "except", "finally"}:
                        tok_list.append(tok_str)
                    else:
                        tok_list.append("VAR")
                elif tok_type == tokenize.STRING:
                    tok_list.append("STR")
                elif tok_type == tokenize.NUMBER:
                    tok_list.append("NUM")
                elif tok_type == tokenize.OP:
                    tok_list.append(tok_str)
                elif tok_type == tokenize.NEWLINE:
                    tok_list.append("NEWLINE")
        except tokenize.TokenError as e:
            duplicated_code_logger.warning(f"Tokenization failed for block: {e}\nBlock:\n{source}")
            return ["TOKEN_ERROR"]
        return tok_list

    block = normalize_indentation(block)
    if not validate_indentation(block):
        duplicated_code_logger.warning(f"Skipping tokenization due to indentation issues in block:\n{block}")
        return ["INDENTATION_ERROR"]

    tokens.extend(extract_ast_tokens(block))
    tokens.extend(extract_tokenize_tokens(block))

    return tokens

# ==================================================================================================================================


def _generate_ngrams(tokens: list, n: int = 3) -> set:
    """
    Generate n-grams from a list of tokens.

    Args:
        tokens (list): List of tokens
        n (int, optional): Size of n-grams. Defaults to 3.

    Returns:
        set: Set of n-gram tuples
    """
    return set(tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1))

def _jaccard_similarity(tokens1: list, tokens2: list, ngram_size: int = 3) -> float:
    """
    Calculate Jaccard similarity between two sets of tokens.

    Args:
        tokens1 (list): First list of tokens
        tokens2 (list): Second list of tokens
        ngram_size (int, optional): Size of n-grams. Defaults to 3.

    Returns:
        float: Jaccard similarity score
    """
    ngrams1 = _generate_ngrams(tokens1, ngram_size)
    ngrams2 = _generate_ngrams(tokens2, ngram_size)
    intersection = ngrams1 & ngrams2
    union = ngrams1 | ngrams2
    return len(intersection) / len(union) if union else 0.0

def _find_duplicated_code(source_code: str) -> list:
    """
    Find duplicated code blocks in the source code.

    Args:
        source_code (str): Source code to analyze

    Returns:
        list: List of dictionaries containing duplicate block pairs
    """
    duplicated_code_logger.info("[starting] _find_duplicated_code()")

    cleaned_code = _remove_comments(source_code)
    duplicated_code_logger.debug("[removed comments] from source code")

    if not cleaned_code.strip():
        msg = "No valid code after removing comments"
        duplicated_code_logger.error("[error] " + msg)
        return []

    blocks = _split_into_blocks(cleaned_code)
    formatted_blocks = "\n\n".join(
        f"[Block starting at line {start}]\n{block}" for block, start in blocks
    )
    duplicated_code_logger.debug(
        f"[split] source code into {len(blocks)} blocks:\n{formatted_blocks}"
    )

    if len(blocks) < 2:
        msg = "Not enough code blocks to compare for duplication"
        duplicated_code_logger.error("[error] " + msg)
        return []

    tokenized_blocks = []
    for block, line_num in blocks:
        tokens = _tokenize_block(block)
        if tokens and tokens != ["INDENTATION_ERROR"] and tokens != ["TOKEN_ERROR"]:
            tokenized_blocks.append((tokens, block, line_num))
        else:
            duplicated_code_logger.warning(f"Skipping block at line {line_num} due to tokenization failure")

    duplicated_code_logger.debug(
        f"[info] tokenized {len(tokenized_blocks)} of {len(blocks)} blocks"
    )

    duplicates = []
    for i in range(len(tokenized_blocks)):
        for j in range(i + 1, len(tokenized_blocks)):
            tokens_i, block_i, line_i = tokenized_blocks[i]
            tokens_j, block_j, line_j = tokenized_blocks[j]
            sim = _jaccard_similarity(tokens_i, tokens_j)

            duplicated_code_logger.debug(
                f"[jaccard] comparing block {i} (line {line_i}) and block {j} (line {line_j}): similarity = {sim:.2f}"
            )

            if sim >= DUPS_THRESHOLD:
                duplicated_code_logger.info(
                    f"[found] duplicate between block {i} and block {j} with jacc_sim {sim:.2f}"
                )
                duplicates.append(
                    {
                        "block1": {
                            "index": i,
                            "text": block_i,
                            "type": "code",
                            "tokens": list(tokens_i),
                            "line_number": line_i,
                        },
                        "block2": {
                            "index": j,
                            "text": block_j,
                            "type": "code",
                            "tokens": list(tokens_j),
                            "line_number": line_j,
                        },
                        "similarity": sim,
                        "threshold": DUPS_THRESHOLD,
                    }
                )

    duplicated_code_logger.info(
        f"[done], found {len(duplicates)} duplicated block pair/s."
    )
    duplicated_code_logger.info(f"[info]\n {json.dumps(duplicates, indent=4)}\n")

    return duplicates
