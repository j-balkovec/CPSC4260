# ===== SOFTWARE ANALYSIS REPORT =====

---
## Code Metrics:

| Metric | Description | Value |
|--------|-------------|-------|
| `LOC` | Lines of Code | `19` |
| `SLOC` | Source Lines of Code | `27` |
| `Comment Density` | Proportion of comment lines to total lines | `0.222` |
| `Blank Line Density` | Proportion of blank lines to total lines | `0.074` |

---
## Halstead Metrics:

| Metric | Description | Value |
|--------|-------------|-------|
| `n1` | Number of unique operators | `2` |
| `n2` | Number of unique operands | `16` |
| `N1` | Total occurrences of operators | `9` |
| `N2` | Total occurrences of operands | `21` |
| `N` | Total number of operators and operands (N1 + N2) | `30` |
| `n` | Total number of distinct operators and operands (n1 + n2) | `18` |
| `V` | Volume (size of the implementation) | `125.098` |
| `D` | Difficulty (how difficult the program is to understand) | `1.312` |
| `HN` | Halstead's number (product of difficulty and volume) | `66.0` |
| `E` | Effort (estimated mental effort) | `164.191` |
| `T` | Time (estimated time to understand the program) | `9.122` |
| `B` | Bugs (estimated number of bugs in the program) | `0.055` |
| `M` | Vocabulary (unique operators and operands used) | `54.979` |


---
### Long Parameter List Detections:

  - Function `'show_order_details_with_shipping'` at line `48`
    * **Parameters**: `7`, Threshold: `3`

---
### Long Method Detections:

  - Function `'show_order_details_with_shipping'` from line `12` to `28`
    * **Length**: `17 lines`, Threshold: `15`

---
### Duplicated Code Detections:

##### Duplicate 1, **Similarity**: `1.00`
 - **Block 1** `(Line 11)`:
```
        if shipping_address:
                details += f", Ship To: {shipping_address}"
```
 - **Block 2** `(Line 13)`:
```
        if tracking_number:
                    details += f", Tracking: {tracking_number}"
```

---
# ===== END OF REPORT =====
