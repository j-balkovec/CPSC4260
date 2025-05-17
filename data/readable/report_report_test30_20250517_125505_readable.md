# ===== SOFTWARE ANALYSIS REPORT =====

---
## Code Metrics:

| Metric | Description | Value |
|--------|-------------|-------|
| `LOC` | Lines of Code | `13` |
| `SLOC` | Source Lines of Code | `24` |
| `Comment Density` | Proportion of comment lines to total lines | `0.333` |
| `Blank Line Density` | Proportion of blank lines to total lines | `0.125` |

---
## Halstead Metrics:

| Metric | Description | Value |
|--------|-------------|-------|
| `n1` | Number of unique operators | `1` |
| `n2` | Number of unique operands | `21` |
| `N1` | Total occurrences of operators | `6` |
| `N2` | Total occurrences of operands | `26` |
| `N` | Total number of operators and operands (N1 + N2) | `32` |
| `n` | Total number of distinct operators and operands (n1 + n2) | `22` |
| `V` | Volume (size of the implementation) | `142.702` |
| `D` | Difficulty (how difficult the program is to understand) | `0.619` |
| `HN` | Halstead's number (product of difficulty and volume) | `92.239` |
| `E` | Effort (estimated mental effort) | `88.339` |
| `T` | Time (estimated time to understand the program) | `4.908` |
| `B` | Bugs (estimated number of bugs in the program) | `0.029` |
| `M` | Vocabulary (unique operators and operands used) | `52.642` |


---
### Long Parameter List Detections:

  - Function `'log_event_detailed_v2'` at line `60`
    * **Parameters**: `8`, Threshold: `3`

  - Function `'audit_operation_complex_v2'` at line `110`
    * **Parameters**: `10`, Threshold: `3`

---
### Long Method Detections:

  - *No long methods were found.*

---
### Duplicated Code Detections:

  - *No duplicated code was found.*

---
# ===== END OF REPORT =====
