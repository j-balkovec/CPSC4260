# ===== SOFTWARE ANALYSIS REPORT =====

---
## Code Metrics:

| Metric | Description | Value |
|--------|-------------|-------|
| `LOC` | Lines of Code | `8` |
| `SLOC` | Source Lines of Code | `16` |
| `Comment Density` | Proportion of comment lines to total lines | `0.375` |
| `Blank Line Density` | Proportion of blank lines to total lines | `0.125` |

---
## Halstead Metrics:

| Metric | Description | Value |
|--------|-------------|-------|
| `n1` | Number of unique operators | `0` |
| `n2` | Number of unique operands | `12` |
| `N1` | Total occurrences of operators | `0` |
| `N2` | Total occurrences of operands | `13` |
| `N` | Total number of operators and operands (N1 + N2) | `13` |
| `n` | Total number of distinct operators and operands (n1 + n2) | `12` |
| `V` | Volume (size of the implementation) | `46.605` |
| `D` | Difficulty (how difficult the program is to understand) | `0.0` |
| `HN` | Halstead's number (product of difficulty and volume) | `0` |
| `E` | Effort (estimated mental effort) | `0.0` |
| `T` | Time (estimated time to understand the program) | `0.0` |
| `B` | Bugs (estimated number of bugs in the program) | `0.0` |
| `M` | Vocabulary (unique operators and operands used) | `82.232` |


---
### Long Parameter List Detections:

  - *No functions with long parameter lists were found.*

---
### Long Method Detections:

  - *No long methods were found.*

---
### Duplicated Code Detections:

##### Duplicate 1, **Similarity**: `1.00`
 - **Block 1** `(Line 2)`:
```
        if not isinstance(text, str):
            raise TypeError("Input must be a string.")
        return text.upper()
```
 - **Block 2** `(Line 6)`:
```
        if not isinstance(input_string, str):
            raise TypeError("Input must be a string.")
        return input_string.upper()
```

---
# ===== END OF REPORT =====
