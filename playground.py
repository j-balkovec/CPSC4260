# =======================================================================
# ==== I'M GONNA DURK MY SCHMURK IF THIS SHIT DOES NOT START WORKING ====
# =======================================================================

# Testing different approaches to detecting duplicate code

import hashlib
import ast

# ================ APPROACH 1 ================
def hash_chunk(lines):
    return hashlib.md5("".join(lines).encode()).hexdigest()

def find_duplicate_code(filepath, chunk_size=5):
    with open(filepath) as f:
        lines = [line.strip() for line in f if line.strip()]  

    seen_hashes = {}
    duplicates = []

    for i in range(len(lines) - chunk_size + 1):
        chunk = lines[i:i+chunk_size]
        chunk_hash = hash_chunk(chunk)

        if chunk_hash in seen_hashes:
            duplicates.append((seen_hashes[chunk_hash], i))
        else:
            seen_hashes[chunk_hash] = i

    return duplicates

def extract_duplicate_code(filepath, duplicates, chunk_size=5):
    """Extract duplicated code blocks from the file based on duplicate line pairs."""
    with open(filepath) as f:
        lines = f.readlines()  

    code_blocks = []

    for original_start, duplicate_start in duplicates:
        original_block = lines[original_start : original_start + chunk_size]
        duplicate_block = lines[duplicate_start : duplicate_start + chunk_size]

        code_blocks.append({
            "original_start": original_start + 1,  
            "duplicate_start": duplicate_start + 1,
            "original_code": "".join(original_block),
            "duplicate_code": "".join(duplicate_block)
        })

    return code_blocks
# ================ APPROACH 1 ================


# ================ APPROACH 2 ================

def get_ast_subtrees(filepath):
    with open(filepath) as f:
        tree = ast.parse(f.read())

    subtrees = []
    nodes = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.For, ast.If, ast.While, ast.With)):
            subtrees.append(ast.dump(node))
            nodes.append(node)
    return subtrees, nodes

def find_duplicate_subtrees(filepath):
    subtrees, nodes = get_ast_subtrees(filepath)
    seen = {}
    duplicates = []

    for idx, subtree in enumerate(subtrees):
        if subtree in seen:
            duplicates.append((seen[subtree], idx))
        else:
            seen[subtree] = idx

    return duplicates, nodes

def extract_duplicate_subtrees(filepath, duplicates, nodes):
    with open(filepath) as f:
        lines = f.readlines()

    code_blocks = []

    for original_idx, duplicate_idx in duplicates:
        original_node = nodes[original_idx]
        duplicate_node = nodes[duplicate_idx]

        original_start = original_node.lineno - 1  
        original_end = original_node.end_lineno
        duplicate_start = duplicate_node.lineno - 1
        duplicate_end = duplicate_node.end_lineno

        original_block = lines[original_start:original_end]
        duplicate_block = lines[duplicate_start:duplicate_end]

        code_blocks.append({
            "original_start": original_start + 1,
            "duplicate_start": duplicate_start + 1,
            "original_code": "".join(original_block),
            "duplicate_code": "".join(duplicate_block)
        })

    return code_blocks
# ================ APPROACH 2 ================


FILE = "/Users/jbalkovec/Desktop/CPSC4260/Project/tests/test4.py"

print("# ================ APPROACH 1 ================\n")
duplicates = find_duplicate_code(FILE)
extracted = extract_duplicate_code(FILE, duplicates, chunk_size=5)

for block in extracted:
    print(f"\n=== Original block starting at line {block['original_start']} ===\n{block['original_code']}")
    print(f"=== Duplicate block starting at line {block['duplicate_start']} ===\n{block['duplicate_code']}")
print("\n# ================ APPROACH 1 ================\n")

for i in range(1, 5):
    print("*")

print("\n# ================ APPROACH 2 ================\n")
duplicates, nodes = find_duplicate_subtrees(FILE)
extracted = extract_duplicate_subtrees(FILE, duplicates, nodes)

for block in extracted:
    print(f"\n=== Original block starting at line {block['original_start']} ===\n{block['original_code']}")
    print(f"=== Duplicate block starting at line {block['duplicate_start']} ===\n{block['duplicate_code']}")
print("\n# ================ APPROACH 2 ================\n")