# ===== SOFTWARE ANALYSIS REPORT =====

---
## Code Metrics:

| Metric | Description | Value |
|--------|-------------|-------|
| `LOC` | Lines of Code | `25` |
| `SLOC` | Source Lines of Code | `48` |
| `Comment Density` | Proportion of comment lines to total lines | `0.0` |
| `Blank Line Density` | Proportion of blank lines to total lines | `0.479` |

---
## Halstead Metrics:

| Metric | Description | Value |
|--------|-------------|-------|
| `n1` | Number of unique operators | `4` |
| `n2` | Number of unique operands | `28` |
| `N1` | Total occurrences of operators | `10` |
| `N2` | Total occurrences of operands | `99` |
| `N` | Total number of operators and operands (N1 + N2) | `109` |
| `n` | Total number of distinct operators and operands (n1 + n2) | `32` |
| `V` | Volume (size of the implementation) | `545.0` |
| `D` | Difficulty (how difficult the program is to understand) | `7.071` |
| `HN` | Halstead's number (product of difficulty and volume) | `142.606` |
| `E` | Effort (estimated mental effort) | `3853.929` |
| `T` | Time (estimated time to understand the program) | `214.107` |
| `B` | Bugs (estimated number of bugs in the program) | `1.285` |
| `M` | Vocabulary (unique operators and operands used) | `12.46` |


---
### Long Parameter List Detections:

  - *No functions with long parameter lists were found.*

---
### Long Method Detections:

  - Function `'func2'` from line `8` to `31`
    * **Length**: `18 lines`, Threshold: `15`

  - Function `'func3'` from line `32` to `48`
    * **Length**: `17 lines`, Threshold: `15`

---
### Duplicated Code Detections:

##### Duplicate 1, **Similarity**: `1.00`
 - **Block 1** `(Line 7)`:
```
        if not a:
            return "Error: Matrices cannot be multiplied. One of the matrices is empty."
```
 - **Block 2** `(Line 9)`:
```
        if not b:
            return "Error: Matrices cannot be multiplied. One of the matrices is empty."
```

---
# ===== END OF REPORT =====
