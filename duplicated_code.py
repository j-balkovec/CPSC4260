# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sun Apr 20th, 2025
#
# __file__: duplicated_code.py
#
# __brief__: TODO

import re
import keyword

from constants import (DUPS_THRESHOLD)
from exceptions import (CodeProcessingError)
from logger import setup_logger

# ==========
duplicated_code_logger = setup_logger(name="duplicated_code.py_logger", log_file="duplicated_code.log")
# ==========

duplicated_code_logger.info("duplicated_code_logger")

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

        # FIXME might need more??
        is_control_start = stripped.startswith(('if ', 
                                                'elif ', 
                                                'else:', 
                                                'for ', 
                                                'while ', 
                                                'try:', 
                                                'except ', 
                                                'finally:', 
                                                'with',
                                                ))
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
    block = re.sub(r'(["\']).*?\1', 'STR', block)  
    block = re.sub(r'\b\d+\.\d+\b', 'NUM', block)  
    block = re.sub(r'\b\d+\b', 'NUM', block)       
    
    block = re.sub(r'(?<!\w)(\d+\.\d+)(?!\w)', 'FLOAT', block)
    block = re.sub(r'(?<!\w)(\d+:\d+)(?!\w)', 'TIME', block)
    block = re.sub(r'(?<!\w)(\d+/\d+/\d+)(?!\w)', 'DATE', block)
    block = re.sub(r'(?<!\w)(\d+/\d+/\d+ \d+:\d+)(?!\w)', 'DATETIME', block)
    
    raw_tokens = re.findall(r'\w+|[+\-*/=<>!&|%^~]+|[()\[\]{},;.:]', block)
    
    tokens = []
    for tok in raw_tokens:
        if keyword.iskeyword(tok) or tok in {'True', 'False', 'None'}:
            tokens.append(tok)
        elif re.fullmatch(r'[a-zA-Z_]\w*', tok): 
            tokens.append('VAR')
        else:
            tokens.append(tok)

    return tokens # return as set maybe??? to remove dups and sort? 


def _generate_ngrams(tokens: list, n: int = 3) -> set:
    """_summary_

    Args:
        tokens (list): returned from @see _tokenize_block()
        n (int, optional): size of the ngram, defaults to 3 (trigram).

    Returns:
        set: set of ngrams to be used for comparison @ see _jaccard_similarity()
    """
    return set(tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1))


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
        raise CodeProcessingError(msg, function="_remove_comments", source_code=source_code)
    
    blocks = _split_into_blocks(cleaned_code)
    formatted_blocks = "\n\n".join(
        f"[Block starting at line {start}]\n{block}" for block, start in blocks
    )
    duplicated_code_logger.debug(f"[split] source code into {len(blocks)} blocks:\n{formatted_blocks}")
    
    if len(blocks) < 2:
        msg = "Not enough code blocks to compare for duplication"
        duplicated_code_logger.error(f"[error] " + msg)
        raise CodeProcessingError(msg, function="_split_into_blocks", source_code=source_code)

    tokenized_blocks = [(_tokenize_block(block), block, line_num) for block, line_num in blocks]
    duplicated_code_logger.debug(f"[info] tokenized all code blocks, {tokenized_blocks}")
    
    duplicates = []

    for i in range(len(tokenized_blocks)):
        for j in range(i + 1, len(tokenized_blocks)):
            tokens_i, block_i, line_i = tokenized_blocks[i]
            tokens_j, block_j, line_j = tokenized_blocks[j]
            sim = _jaccard_similarity(tokens_i, tokens_j)
            
            duplicated_code_logger.debug(f"[jaccard] comparing block {i} (line {line_i}) and block {j} (line {line_j}): similarity = {sim:.2f}")
            
            if sim >= DUPS_THRESHOLD:
                duplicated_code_logger.info(f"[found] duplicate between block {i} and block {j} with jacc_sim {sim:.2f}")
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
                
    duplicated_code_logger.info(f"[done], found {len(duplicates)} duplicated block pair/s.")
    duplicated_code_logger.info(f"[info]\n {json.dumps(duplicates, indent=4)}\n")
    
    return duplicates


# ========================================== WORKBENCH ===================================================

from utility import _read_file_contents
import json

PATH = r"/Users/jbalkovec/Desktop/CPSC4260/Project/tests/test4.py"

source = _read_file_contents(PATH)

duplicates = _find_duplicated_code(source)

json_dump = json.dumps(duplicates, indent=4)


print("\n\n=====================================================")
print("Duplicated Code:\n", json_dump)

# ========================================================================================================