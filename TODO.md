# Overall Objectives
- [ ] Implement **refactor methods** for duplicated code. 
- [ ] Integrate **loading bars** for long operations.
- [ ] Use **threading** to improve GUI responsiveness.
- [ ] **Document** all core files and modules.

---

# Current Bugs
- GUI is **very slow and unresponsive** (likely due to synchronous blocking operations).

---

# Today's Tasks
- [x] Finish writing documentation
- [ ] Fix `save_refactored_file` function:
  - Ensure it works with **multiple duplicated functions**.
  - Make sure it doesn't corrupt the original file.

> Focus on **back-end functionality first**, design **frontend later**.

---

# Known Issues
- GUI performance needs improvement or redesign.
- Residual **function signatures and bodies** are not being fully removed after refactor.
- Jaccard similarity is **too brittle** for small snippets:
  - Works as designed (trigram-based).
  - Needs to be replaced or enhanced with a more robust heuristic.

---

# Fix Strategy Summary
- Only validate **context-free logical blocks** for refactoring.
- On replacement:
  - Do **not call helper globally**.
  - **Preserve indentation** exactly.
  - **Replace blocks in-place** instead of appending helper only.

---

# Technical Gaps
- **Function argument matching** isn’t preserved.
- **Return values** are assumed identical — may not be true.
- Requires **Python 3.8+** for `ast.end_lineno`.

---