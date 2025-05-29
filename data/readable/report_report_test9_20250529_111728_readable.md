# ===== SOFTWARE ANALYSIS REPORT =====

---
## Code Metrics:

| Metric | Description | Value |
|--------|-------------|-------|
| `LOC` | Lines of Code | `17` |
| `SLOC` | Source Lines of Code | `30` |
| `Comment Density` | Proportion of comment lines to total lines | `0.267` |
| `Blank Line Density` | Proportion of blank lines to total lines | `0.167` |

---
## Halstead Metrics:

| Metric | Description | Value |
|--------|-------------|-------|
| `n1` | Number of unique operators | `6` |
| `n2` | Number of unique operands | `31` |
| `N1` | Total occurrences of operators | `27` |
| `N2` | Total occurrences of operands | `65` |
| `N` | Total number of operators and operands (N1 + N2) | `92` |
| `n` | Total number of distinct operators and operands (n1 + n2) | `37` |
| `V` | Volume (size of the implementation) | `479.27` |
| `D` | Difficulty (how difficult the program is to understand) | `6.29` |
| `HN` | Halstead's number (product of difficulty and volume) | `169.09` |
| `E` | Effort (estimated mental effort) | `3014.761` |
| `T` | Time (estimated time to understand the program) | `167.487` |
| `B` | Bugs (estimated number of bugs in the program) | `1.005` |
| `M` | Vocabulary (unique operators and operands used) | `17.567` |


---
### Long Parameter List Detections:

  - Function `'format_data_table'` at line `18`
    * **Parameters**: `5`, Threshold: `3`

---
### Long Method Detections:

  - Function `'format_data_table'` from line `5` to `31`
    * **Length**: `27 lines`, Threshold: `15`

---
### Duplicated Code Detections:

  - *No duplicated code was found.*

---
# ===== END OF REPORT =====
