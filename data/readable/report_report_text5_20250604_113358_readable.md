# ===== SOFTWARE ANALYSIS REPORT =====

---
## Code Metrics:

| Metric | Description | Value |
|--------|-------------|-------|
| `LOC` | Lines of Code | `17` |
| `SLOC` | Source Lines of Code | `25` |
| `Comment Density` | Proportion of comment lines to total lines | `0.0` |
| `Blank Line Density` | Proportion of blank lines to total lines | `0.32` |

---
## Halstead Metrics:

| Metric | Description | Value |
|--------|-------------|-------|
| `n1` | Number of unique operators | `5` |
| `n2` | Number of unique operands | `17` |
| `N1` | Total occurrences of operators | `22` |
| `N2` | Total occurrences of operands | `46` |
| `N` | Total number of operators and operands (N1 + N2) | `68` |
| `n` | Total number of distinct operators and operands (n1 + n2) | `22` |
| `V` | Volume (size of the implementation) | `303.241` |
| `D` | Difficulty (how difficult the program is to understand) | `6.765` |
| `HN` | Halstead's number (product of difficulty and volume) | `81.097` |
| `E` | Effort (estimated mental effort) | `2051.339` |
| `T` | Time (estimated time to understand the program) | `113.963` |
| `B` | Bugs (estimated number of bugs in the program) | `0.684` |
| `M` | Vocabulary (unique operators and operands used) | `27.957` |


---
### Long Parameter List Detections:

  - Function `'func1'` at line `11`
    * **Parameters**: `4`, Threshold: `3`

  - Function `'func2'` at line `25`
    * **Parameters**: `7`, Threshold: `3`

  - Function `'func3'` at line `42`
    * **Parameters**: `6`, Threshold: `3`

  - Function `'func4'` at line `75`
    * **Parameters**: `8`, Threshold: `3`

---
### Long Method Detections:

  - *No long methods were found.*

---
### Duplicated Code Detections:

##### Duplicate 1, **Similarity**: `0.79`
 - **Block 1** `(Line 14)`:
```
        def func5(a, b):
            return a + b
```
 - **Block 2** `(Line 16)`:
```
        def func5(a, b, c):
            return a + b + c
```

---
# ===== END OF REPORT =====
