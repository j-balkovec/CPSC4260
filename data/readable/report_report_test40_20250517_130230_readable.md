# ===== SOFTWARE ANALYSIS REPORT =====

---
## Code Metrics:

| Metric | Description | Value |
|--------|-------------|-------|
| `LOC` | Lines of Code | `8` |
| `SLOC` | Source Lines of Code | `15` |
| `Comment Density` | Proportion of comment lines to total lines | `0.4` |
| `Blank Line Density` | Proportion of blank lines to total lines | `0.067` |

---
## Halstead Metrics:

| Metric | Description | Value |
|--------|-------------|-------|
| `n1` | Number of unique operators | `2` |
| `n2` | Number of unique operands | `18` |
| `N1` | Total occurrences of operators | `3` |
| `N2` | Total occurrences of operands | `24` |
| `N` | Total number of operators and operands (N1 + N2) | `27` |
| `n` | Total number of distinct operators and operands (n1 + n2) | `20` |
| `V` | Volume (size of the implementation) | `116.692` |
| `D` | Difficulty (how difficult the program is to understand) | `1.333` |
| `HN` | Halstead's number (product of difficulty and volume) | `77.059` |
| `E` | Effort (estimated mental effort) | `155.589` |
| `T` | Time (estimated time to understand the program) | `8.644` |
| `B` | Bugs (estimated number of bugs in the program) | `0.052` |
| `M` | Vocabulary (unique operators and operands used) | `57.958` |


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
        if not isinstance(data_list, list) or not isinstance(expected_length, int):
                raise TypeError("First argument must be a list, second must be an integer.")
            return len(data_list) == expected_length
```
 - **Block 2** `(Line 6)`:
```
        if not isinstance(array_data, list) or not isinstance(target_size, int):
                raise TypeError("First argument must be a list, second must be an integer.")
            return len(array_data) == target_size
```

---
# ===== END OF REPORT =====
