# ===== SOFTWARE ANALYSIS REPORT =====

---
## Code Metrics:

| Metric | Description | Value |
|--------|-------------|-------|
| `LOC` | Lines of Code | `6` |
| `SLOC` | Source Lines of Code | `8` |
| `Comment Density` | Proportion of comment lines to total lines | `0.0` |
| `Blank Line Density` | Proportion of blank lines to total lines | `0.25` |

---
## Halstead Metrics:

| Metric | Description | Value |
|--------|-------------|-------|
| `n1` | Number of unique operators | `1` |
| `n2` | Number of unique operands | `7` |
| `N1` | Total occurrences of operators | `6` |
| `N2` | Total occurrences of operands | `21` |
| `N` | Total number of operators and operands (N1 + N2) | `27` |
| `n` | Total number of distinct operators and operands (n1 + n2) | `8` |
| `V` | Volume (size of the implementation) | `81.0` |
| `D` | Difficulty (how difficult the program is to understand) | `1.5` |
| `HN` | Halstead's number (product of difficulty and volume) | `19.651` |
| `E` | Effort (estimated mental effort) | `121.5` |
| `T` | Time (estimated time to understand the program) | `6.75` |
| `B` | Bugs (estimated number of bugs in the program) | `0.041` |
| `M` | Vocabulary (unique operators and operands used) | `60.659` |


---
### Long Parameter List Detections:

  - Function `'func3'` at line `27`
    * **Parameters**: `4`, Threshold: `3`

---
### Long Method Detections:

  - *No long methods were found.*

---
### Duplicated Code Detections:

##### Duplicate 1, **Similarity**: `0.79`
 - **Block 1** `(Line 1)`:
```
        def func1(a, b):
            return a + b
```
 - **Block 2** `(Line 3)`:
```
        def func2(a, b, c):
            return a + b + c
```

##### Duplicate 2, **Similarity**: `0.79`
 - **Block 1** `(Line 1)`:
```
        def func1(a, b):
            return a + b
```
 - **Block 2** `(Line 5)`:
```
        def func3(a, b, c, d):
            return a + b + c + d
```

##### Duplicate 3, **Similarity**: `1.00`
 - **Block 1** `(Line 3)`:
```
        def func2(a, b, c):
            return a + b + c
```
 - **Block 2** `(Line 5)`:
```
        def func3(a, b, c, d):
            return a + b + c + d
```

---
# ===== END OF REPORT =====
