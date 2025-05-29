# ===== SOFTWARE ANALYSIS REPORT =====

---
## Code Metrics:

| Metric | Description | Value |
|--------|-------------|-------|
| `LOC` | Lines of Code | `13` |
| `SLOC` | Source Lines of Code | `36` |
| `Comment Density` | Proportion of comment lines to total lines | `0.583` |
| `Blank Line Density` | Proportion of blank lines to total lines | `0.056` |

---
## Halstead Metrics:

| Metric | Description | Value |
|--------|-------------|-------|
| `n1` | Number of unique operators | `6` |
| `n2` | Number of unique operands | `20` |
| `N1` | Total occurrences of operators | `19` |
| `N2` | Total occurrences of operands | `39` |
| `N` | Total number of operators and operands (N1 + N2) | `58` |
| `n` | Total number of distinct operators and operands (n1 + n2) | `26` |
| `V` | Volume (size of the implementation) | `272.626` |
| `D` | Difficulty (how difficult the program is to understand) | `5.85` |
| `HN` | Halstead's number (product of difficulty and volume) | `101.948` |
| `E` | Effort (estimated mental effort) | `1594.859` |
| `T` | Time (estimated time to understand the program) | `88.603` |
| `B` | Bugs (estimated number of bugs in the program) | `0.532` |
| `M` | Vocabulary (unique operators and operands used) | `32.683` |


---
### Long Parameter List Detections:

  - Function `'calculate_compound_interest'` at line `19`
    * **Parameters**: `6`, Threshold: `3`

---
### Long Method Detections:

  - Function `'calculate_compound_interest'` from line `5` to `37`
    * **Length**: `33 lines`, Threshold: `15`

---
### Duplicated Code Detections:

  - *No duplicated code was found.*

---
# ===== END OF REPORT =====
