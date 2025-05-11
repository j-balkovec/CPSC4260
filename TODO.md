# Overall Objectives
- Implement **refactor methods** for duplicated code.
- Add **logging** where useful.
- Integrate **loading bars** for long operations.
- Use **threading** to improve GUI responsiveness.
- Print key messages in **color** (see `generate_readable_report` in `analyze.py`).
- Generate **HTML reports** from TXT output (future task).
- **Document** all core files and modules.

---

# Current Bugs
- GUI is **very slow and unresponsive** (likely due to synchronous blocking operations).

---

# Today's Tasks
- [x] Split up `analyze.py` into smaller modules.
- [ ] Fix duplicated code detection (false positives or missing cases).
- [ ] Implement `refactor` functionality.
- [ ] (Optional) Resolve GUI issues or pivot to terminal-first approach.

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

# GUI: Code Editor Functionality
- Show `"No code to show"` message on empty state.
- Press "Analyze":
  - Display code with highlights.
- Press "Refactor":
  - Show refactored code.
- Allow **saving** to original or new file:
  - Accept path via **RichLog** or input prompt.

---

# Tomorrow’s Priority
- Revisit **file saving** logic:
  - Must support files with **more than 2 duplicated functions**.
  - Ensure the entire file is updated cleanly without corrupting unaffected code.