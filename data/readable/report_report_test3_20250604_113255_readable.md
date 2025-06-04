# ===== SOFTWARE ANALYSIS REPORT =====

---
## Code Metrics:

| Metric | Description | Value |
|--------|-------------|-------|
| `LOC` | Lines of Code | `16` |
| `SLOC` | Source Lines of Code | `21` |
| `Comment Density` | Proportion of comment lines to total lines | `0.0` |
| `Blank Line Density` | Proportion of blank lines to total lines | `0.238` |

---
## Halstead Metrics:

| Metric | Description | Value |
|--------|-------------|-------|
| `n1` | Number of unique operators | `1` |
| `n2` | Number of unique operands | `23` |
| `N1` | Total occurrences of operators | `4` |
| `N2` | Total occurrences of operands | `54` |
| `N` | Total number of operators and operands (N1 + N2) | `58` |
| `n` | Total number of distinct operators and operands (n1 + n2) | `24` |
| `V` | Volume (size of the implementation) | `265.928` |
| `D` | Difficulty (how difficult the program is to understand) | `1.174` |
| `HN` | Halstead's number (product of difficulty and volume) | `104.042` |
| `E` | Effort (estimated mental effort) | `312.176` |
| `T` | Time (estimated time to understand the program) | `17.343` |
| `B` | Bugs (estimated number of bugs in the program) | `0.104` |
| `M` | Vocabulary (unique operators and operands used) | `33.945` |


---
### Long Parameter List Detections:

  - Function `'func3'` at line `25`
    * **Parameters**: `4`, Threshold: `3`

  - Function `'func4'` at line `36`
    * **Parameters**: `4`, Threshold: `3`

---
### Long Method Detections:

  - *No long methods were found.*

---
### Duplicated Code Detections:

##### Duplicate 1, **Similarity**: `1.00`
 - **Block 1** `(Line 1)`:
```
        def func1(a, b):
            return a + b
```
 - **Block 2** `(Line 3)`:
```
        def func2(a, b):
            return a + b
```

##### Duplicate 2, **Similarity**: `0.95`
 - **Block 1** `(Line 1)`:
```
        def func1(a, b):
            return a + b
```
 - **Block 2** `(Line 5)`:
```
        def func3(a, b, c, d):
            return a + b
```

##### Duplicate 3, **Similarity**: `0.95`
 - **Block 1** `(Line 1)`:
```
        def func1(a, b):
            return a + b
```
 - **Block 2** `(Line 7)`:
```
        def func4(e, f, g, h):
            return e + f
```

##### Duplicate 4, **Similarity**: `0.95`
 - **Block 1** `(Line 3)`:
```
        def func2(a, b):
            return a + b
```
 - **Block 2** `(Line 5)`:
```
        def func3(a, b, c, d):
            return a + b
```

##### Duplicate 5, **Similarity**: `0.95`
 - **Block 1** `(Line 3)`:
```
        def func2(a, b):
            return a + b
```
 - **Block 2** `(Line 7)`:
```
        def func4(e, f, g, h):
            return e + f
```

##### Duplicate 6, **Similarity**: `1.00`
 - **Block 1** `(Line 5)`:
```
        def func3(a, b, c, d):
            return a + b
```
 - **Block 2** `(Line 7)`:
```
        def func4(e, f, g, h):
            return e + f
```

---
# ===== END OF REPORT =====
