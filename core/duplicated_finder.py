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


def _normalize_block(text: str) -> str:
    """_summary_

    Args:
        text (str): block of text to be normalized

    Returns:
        str: returns the normalized text
    """
    lines = text.splitlines()
    norm_lines = [line.strip() for line in lines if line.strip()]
    return "\n".join(norm_lines)


def _split_into_blocks(source_code: str) -> list:
    """_summary_

    Args:
        source_code (str): Source code to process

    Returns:
        list: List of (code_block_text, starting_line_number) tuples
    """
    lines = source_code.splitlines()
    blocks = []
    func_map = defaultdict(list)
    current_block = []
    current_indent = None
    start_line = 0
    current_func_name = None

    def flush_block():
        nonlocal current_block, start_line, current_func_name
        non_empty = [l for l in current_block if l.strip()]
        if len(non_empty) >= 2:
            block_text = "\n".join(current_block).strip()
            blocks.append((block_text, start_line))

            if current_func_name:
                func_map[current_func_name].append((block_text, start_line))
        current_block = []
        current_func_name = None

    for i, line in enumerate(lines):
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
            start_line = i + 1
            current_indent = indent

            if stripped.startswith("def "):
                match = re.match(r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)", stripped)
                if match:
                    current_func_name = match.group(1)

        current_block.append(line)

    flush_block()

    for name, entries in func_map.items():
        seen = set()
        for i in range(len(entries)):
            for j in range(i + 1, len(entries)):
                block_i = _normalize_block(entries[i][0])
                block_j = _normalize_block(entries[j][0])
                if block_i == block_j:
                    if (block_i, block_j) not in seen:
                        seen.add((block_i, block_j))
                        print(
                            f"[DUPLICATE FUNC] Function '{name}' duplicated at lines {entries[i][1]} and {entries[j][1]}"
                        )

    return blocks


def _remove_comments(source_code: str) -> str:
    """_summary_

    Args:
        source_code (str): source code to be processed

    Returns:
        str: source code without comments
    """
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


def _tokenize_block(block: str) -> list:
    """_summary_

    Args:
        block (str): code block to be tokenized

    Returns:
        list: list of tokens
    """
    block = re.sub(r'(["\']).*?\1', "STR", block)
    block = re.sub(r"\b\d+\.\d+\b", "NUM", block)
    block = re.sub(r"\b\d+\b", "NUM", block)

    block = re.sub(r"(?<!\w)(\d+\.\d+)(?!\w)", "FLOAT", block)
    block = re.sub(r"(?<!\w)(\d+:\d+)(?!\w)", "TIME", block)
    block = re.sub(r"(?<!\w)(\d+/\d+/\d+)(?!\w)", "DATE", block)
    block = re.sub(r"(?<!\w)(\d+/\d+/\d+ \d+:\d+)(?!\w)", "DATETIME", block)

    raw_tokens = re.findall(r"\w+|[+\-*/=<>!&|%^~]+|[()\[\]{},;.:]", block)

    tokens = []
    for tok in raw_tokens:
        if keyword.iskeyword(tok) or tok in {"True", "False", "None"}:
            tokens.append(tok)
        elif re.fullmatch(r"[a-zA-Z_]\w*", tok):
            tokens.append("VAR")
        else:
            tokens.append(tok)

    return tokens  # return as set maybe??? to remove dups and sort?


def _generate_ngrams(tokens: list, n: int = 3) -> set:
    """_summary_

    Args:
        tokens (list): returned from @see _tokenize_block()
        n (int, optional): size of the ngram, defaults to 3 (trigram).

    Returns:
        set: set of ngrams to be used for comparison @ see _jaccard_similarity()
    """
    return set(tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1))


def _jaccard_similarity(tokens1: list, tokens2: list, ngram_size: int = 3) -> float:
    """_summary_

    Args:
        set1 (set): set A
        set2 (set): set B

    Returns:
        float: similarity score
    """
    ngrams1 = _generate_ngrams(tokens1, ngram_size)
    ngrams2 = _generate_ngrams(tokens2, ngram_size)

    intersection = ngrams1 & ngrams2
    union = ngrams1 | ngrams2

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
    duplicated_code_logger.info("[starting] _find_duplicated_code()")

    cleaned_code = _remove_comments(source_code)
    duplicated_code_logger.debug("[removed comments] from source code")

    if not cleaned_code.strip():
        msg = "No valid code after removing comments"
        duplicated_code_logger.error("[error] " + msg)
        # raise CodeProcessingError(msg, function="_remove_comments", source_code=source_code)
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
        # raise CodeProcessingError(msg, function="_split_into_blocks", source_code=source_code)
        return []

    tokenized_blocks = [
        (_tokenize_block(block), block, line_num) for block, line_num in blocks
    ]
    duplicated_code_logger.debug(
        f"[info] tokenized all code blocks, {tokenized_blocks}"
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
                            "type": "code",  # formatting purposes TODO
                            "tokens": list(tokens_i),
                            "line_number": line_i,
                        },
                        "block2": {
                            "index": j,
                            "text": block_j,
                            "type": "code",  # formatting purposes TODO
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
