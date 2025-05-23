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
- [x] fix `save_refactored_file` function:
  - make sure it works with **multiple duplicated functions**.
  - also make sure it doesn't corrupt the original file.

# Metrics, Coverge, and Code Smells Goals and Reports

- **Coverage: `coverage`**

  - [ ] have coverage > 85%, the higher the better
  - currently at 73%
  - **Critical:**
    - `refactor.py` is at `41%`
    - `file_saver.py` is at `43%`
    - `utility.py` is at `53%`
    - `new_ui` is at `56%`

**Results as of now (Fri May 23rd):**

```plaintext
Name                                                                       Stmts   Miss  Cover
----------------------------------------------------------------------------------------------
/Users/jbalkovec/Desktop/CPSC4260/project_root/core/code_metrics.py           65     23    65%
/Users/jbalkovec/Desktop/CPSC4260/project_root/core/code_smells.py            31      2    94%
/Users/jbalkovec/Desktop/CPSC4260/project_root/core/constants.py              18      0   100%
/Users/jbalkovec/Desktop/CPSC4260/project_root/core/duplicated_finder.py     135     16    88%
/Users/jbalkovec/Desktop/CPSC4260/project_root/core/file_saver.py             23     13    43%
/Users/jbalkovec/Desktop/CPSC4260/project_root/core/halstead.py               85     12    86%
/Users/jbalkovec/Desktop/CPSC4260/project_root/core/method_length.py          48     10    79%
/Users/jbalkovec/Desktop/CPSC4260/project_root/core/param_length.py           33      2    94%
/Users/jbalkovec/Desktop/CPSC4260/project_root/core/refactor.py              128     75    41%
/Users/jbalkovec/Desktop/CPSC4260/project_root/gui/new_ui.py                 186     82    56%
/Users/jbalkovec/Desktop/CPSC4260/project_root/utils/exceptions.py            45      5    89%
/Users/jbalkovec/Desktop/CPSC4260/project_root/utils/logger.py                30      5    83%
/Users/jbalkovec/Desktop/CPSC4260/project_root/utils/utility.py              164     77    53%
conftest.py                                                                   48     10    79%
sys_test.py                                                                  152      1    99%
unit_tests.py                                                                 86      7    92%
----------------------------------------------------------------------------------------------
TOTAL                                                                       1277    340    73%
```

<!-- EDIT -->

- **Code Smells: `pylint`**
  - [ ] have pylint score > 8.0, the higher the better
  - currently at `7.5`
  - **Critical:**
    - `refactor.py` is at `6.0`
    - `file_saver.py` is at `6.0`
    - `utility.py` is at `7.0`
    - `new_ui` is at `7.0`

**Results as of now (Fri May 23rd):**

```plaintext
Your code has been rated at 5.09/10
```

<!-- EDIT -->

- **Metrics: `radon`**
  - [ ] have cyclomatic complexity < 10, the lower the better
  - currently at `11.0`
  - **Critical:**
    - `refactor.py` is at `20.0`
    - `file_saver.py` is at `12.0`
    - `utility.py` is at `12.0`
    - `new_ui` is at `12.0`

**Results as of now (Fri May 23rd):**

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
