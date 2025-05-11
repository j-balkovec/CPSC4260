# ===== SOFTWARE ANALYSIS REPORT =====

---
## Code Metrics:

| Metric | Description | Value |
|--------|-------------|-------|
| `LOC` | Lines of Code | `158` |
| `SLOC` | Source Lines of Code | `288` |
| `Comment Density` | Proportion of comment lines to total lines | `0.302` |
| `Blank Line Density` | Proportion of blank lines to total lines | `0.149` |

---
## Halstead Metrics:

| Metric | Description | Value |
|--------|-------------|-------|
| `n1` | Number of unique operators | `8` |
| `n2` | Number of unique operands | `162` |
| `N1` | Total occurrences of operators | `116` |
| `N2` | Total occurrences of operands | `503` |
| `N` | Total number of operators and operands (N1 + N2) | `619` |
| `n` | Total number of distinct operators and operands (n1 + n2) | `170` |
| `V` | Volume (size of the implementation) | `4586.413` |
| `D` | Difficulty (how difficult the program is to understand) | `12.42` |
| `HN` | Halstead's number (product of difficulty and volume) | `1213.056` |
| `E` | Effort (estimated mental effort) | `56962.117` |
| `T` | Time (estimated time to understand the program) | `3164.562` |
| `B` | Bugs (estimated number of bugs in the program) | `18.987` |
| `M` | Vocabulary (unique operators and operands used) | `-45.34` |


---
### Long Parameter List Detections:

  - Function `'visit_Module'` at line `220`
    * **Parameters**: `4`, Threshold: `3`

  - Function `'visit_FunctionDef'` at line `260`
    * **Parameters**: `4`, Threshold: `3`

  - Function `'_make_helper_node'` at line `371`
    * **Parameters**: `6`, Threshold: `3`

  - Function `'_refactor_with_ast'` at line `467`
    * **Parameters**: `4`, Threshold: `3`

  - Function `'_debug_dict'` at line `968`
    * **Parameters**: `6`, Threshold: `3`

---
### Long Method Detections:

  - Function `'__init__'` from line `39` to `55`
    * **Length**: `17 lines`, Threshold: `15`

  - Function `'visit_FunctionDef'` from line `70` to `98`
    * **Length**: `29 lines`, Threshold: `15`

  - Function `'_make_helper_node'` from line `99` to `128`
    * **Length**: `30 lines`, Threshold: `15`

  - Function `'_refactor_with_ast'` from line `129` to `149`
    * **Length**: `21 lines`, Threshold: `15`

  - Function `'_extract_functions'` from line `150` to `198`
    * **Length**: `49 lines`, Threshold: `15`

  - Function `'_find_duplicates'` from line `199` to `223`
    * **Length**: `25 lines`, Threshold: `15`

  - Function `'refactor_duplicates'` from line `224` to `251`
    * **Length**: `28 lines`, Threshold: `15`

  - Function `'_debug_dict'` from line `252` to `289`
    * **Length**: `38 lines`, Threshold: `15`

---
### Duplicated Code Detections:

  - *No duplicated code was found.*

---
# ===== END OF REPORT =====
