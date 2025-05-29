# ===== SOFTWARE ANALYSIS REPORT =====

---
## Code Metrics:

| Metric | Description | Value |
|--------|-------------|-------|
| `LOC` | Lines of Code | `10` |
| `SLOC` | Source Lines of Code | `15` |
| `Comment Density` | Proportion of comment lines to total lines | `0.133` |
| `Blank Line Density` | Proportion of blank lines to total lines | `0.2` |

---
## Halstead Metrics:

| Metric | Description | Value |
|--------|-------------|-------|
| `n1` | Number of unique operators | `1` |
| `n2` | Number of unique operands | `12` |
| `N1` | Total occurrences of operators | `2` |
| `N2` | Total occurrences of operands | `15` |
| `N` | Total number of operators and operands (N1 + N2) | `17` |
| `n` | Total number of distinct operators and operands (n1 + n2) | `13` |
| `V` | Volume (size of the implementation) | `62.907` |
| `D` | Difficulty (how difficult the program is to understand) | `0.625` |
| `HN` | Halstead's number (product of difficulty and volume) | `43.02` |
| `E` | Effort (estimated mental effort) | `39.317` |
| `T` | Time (estimated time to understand the program) | `2.184` |
| `B` | Bugs (estimated number of bugs in the program) | `0.013` |
| `M` | Vocabulary (unique operators and operands used) | `73.569` |


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
        if not isinstance(number, (int, float)):
            raise TypeError("Input must be a number.")
        return number**2
```
 - **Block 2** `(Line 6)`:
```
        if not isinstance(value, (int, float)):
            raise TypeError("Input must be a number.")
        return value**2
```

---
# ===== END OF REPORT =====
