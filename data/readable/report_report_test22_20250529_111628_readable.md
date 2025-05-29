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
| `n1` | Number of unique operators | `3` |
| `n2` | Number of unique operands | `18` |
| `N1` | Total occurrences of operators | `4` |
| `N2` | Total occurrences of operands | `25` |
| `N` | Total number of operators and operands (N1 + N2) | `29` |
| `n` | Total number of distinct operators and operands (n1 + n2) | `21` |
| `V` | Volume (size of the implementation) | `127.377` |
| `D` | Difficulty (how difficult the program is to understand) | `2.083` |
| `HN` | Halstead's number (product of difficulty and volume) | `79.814` |
| `E` | Effort (estimated mental effort) | `265.369` |
| `T` | Time (estimated time to understand the program) | `14.743` |
| `B` | Bugs (estimated number of bugs in the program) | `0.088` |
| `M` | Vocabulary (unique operators and operands used) | `55.458` |


---
### Long Parameter List Detections:

  - Function `'process_data_v1'` at line `19`
    * **Parameters**: `6`, Threshold: `3`

  - Function `'process_info_v1'` at line `74`
    * **Parameters**: `6`, Threshold: `3`

---
### Long Method Detections:

  - *No long methods were found.*

---
### Duplicated Code Detections:

##### Duplicate 1, **Similarity**: `1.00`
 - **Block 1** `(Line 2)`:
```
        if not isinstance(item_id, int) or not isinstance(value, (int, float)):
            raise ValueError("item_id must be an integer and value must be numeric.")
        return (value * multiplier) + offset
```
 - **Block 2** `(Line 6)`:
```
        if not isinstance(record_id, int) or not isinstance(amount, (int, float)):
            raise ValueError("record_id must be an integer and amount must be numeric.")
        return (amount * factor) + shift
```

---
# ===== END OF REPORT =====
