# ===== SOFTWARE ANALYSIS REPORT =====

---
## Code Metrics:

| Metric | Description | Value |
|--------|-------------|-------|
| `LOC` | Lines of Code | `8` |
| `SLOC` | Source Lines of Code | `46` |
| `Comment Density` | Proportion of comment lines to total lines | `0.087` |
| `Blank Line Density` | Proportion of blank lines to total lines | `0.739` |

---
## Halstead Metrics:

| Metric | Description | Value |
|--------|-------------|-------|
| `n1` | Number of unique operators | `1` |
| `n2` | Number of unique operands | `12` |
| `N1` | Total occurrences of operators | `2` |
| `N2` | Total occurrences of operands | `27` |
| `N` | Total number of operators and operands (N1 + N2) | `29` |
| `n` | Total number of distinct operators and operands (n1 + n2) | `13` |
| `V` | Volume (size of the implementation) | `107.313` |
| `D` | Difficulty (how difficult the program is to understand) | `1.125` |
| `HN` | Halstead's number (product of difficulty and volume) | `43.02` |
| `E` | Effort (estimated mental effort) | `120.727` |
| `T` | Time (estimated time to understand the program) | `6.707` |
| `B` | Bugs (estimated number of bugs in the program) | `0.04` |
| `M` | Vocabulary (unique operators and operands used) | `56.964` |


---
### Long Parameter List Detections:

  - Function `'func2'` at line `58`
    * **Parameters**: `8`, Threshold: `3`

---
### Long Method Detections:

  - *No long methods were found.*

---
### Duplicated Code Detections:

##### Duplicate 1, **Similarity**: `0.90`
 - **Block 1** `(Line 1)`:
```
        def func1(e,f,g):
            return e,f,g
```
 - **Block 2** `(Line 3)`:
```
        def func2(a, b, c, d, e, f, g, h):
            return a
```

##### Duplicate 2, **Similarity**: `1.00`
 - **Block 1** `(Line 5)`:
```
        def func3(a, b):
            return a * b
```
 - **Block 2** `(Line 7)`:
```
        def func4(c, d):
            return c * d
```

---
# ===== END OF REPORT =====
