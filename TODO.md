# Overall Objectives
- [ ] implement **refactor methods** for duplicated code
- [ ] integrate **loading bars** for long operations (optional, is probably gonna slow everything down)
- [ ] **threading** or **multiprocessing** to improve GUI responsiveness
- [ ] **document** all core files and modules.

---

# Current Bugs
- GUI is **very slow and unresponsive** (probs due to synchronous blocking operations).

---

# Today
- [x] finish docs
- [ ] fix `save_refactored_file` function:
  - make sure it works with **multiple duplicated functions**.
  - also make sure it doesn't corrupt the original file.

> Focus on **back-end functionality first**, design **frontend later**.

---

# Known Issues
- GUI performance needs improvement (hella slow rn)
- Sometimes, residual **function signatures and bodies** are not being fully removed after refactor.
- Jaccard similarity is actually **too brittle** for small snippets:
  - rn, it works as designed (trigram-based).
  - probs needs to be replaced or enhanced with a more robust heuristic.

---

# Fix Strategy
- Only validate **context-free logical blocks** for refactoring.
- On replacement:
  - Do **not call helper globally**.
  - **Preserve indentation** exactly.
  - **Replace blocks in-place** instead of appending helper only.

---

# Tech Gaps
- **Function argument matching** isn’t preserved.
- **Return values** are assumed identical -> may not be true.
- Requires **Python 3.8+** for `ast.end_lineno`.

---