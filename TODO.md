# Overall Objectives

- [ ] implement **refactor methods** for duplicated code
- [ ] integrate **loading bars** for long operations (optional, is probably gonna slow everything down)
- [ ] **threading** or **multiprocessing** to improve GUI responsiveness
- [ ] **document** all core files and modules.

---

# Current Bugs

- GUI is **very slow and unresponsive** (probs due to synchronous blocking operations).
- Strip empty lines from the body of the function, or don't count them
- Fix duplicated code detection:
  - [x] **Jaccard similarity** is too brittle for small snippets.
  - [x] **Trigram-based** similarity is not robust enough.
  - [x] **Context-free logical blocks** need to be validated for refactoring.

---

# Today

- [x] Format `analysis` buttons!!!
- [x] Have the ability to refactor in place and crate a copy!!!
- [x] finish docs
- [x] fix `save_refactored_file` function:
  - make sure it works with **multiple duplicated functions**.
  - also make sure it doesn't corrupt the original file.

# Metrics, Coverge, and Code Smells Goals and Reports

- **Coverage: `coverage`**

**Results as of now (Sat May 24th):**

```plaintext
coverage report
Name                                                                       Stmts   Miss  Cover
----------------------------------------------------------------------------------------------
/Users/jbalkovec/Desktop/CPSC4260/project_root/core/code_metrics.py           65      0   100%
/Users/jbalkovec/Desktop/CPSC4260/project_root/core/code_smells.py            30      2    93%
/Users/jbalkovec/Desktop/CPSC4260/project_root/core/constants.py              17      0   100%
/Users/jbalkovec/Desktop/CPSC4260/project_root/core/duplicated_finder.py     134     16    88%
/Users/jbalkovec/Desktop/CPSC4260/project_root/core/file_saver.py             22      0   100%
/Users/jbalkovec/Desktop/CPSC4260/project_root/core/halstead.py               80     10    88%
/Users/jbalkovec/Desktop/CPSC4260/project_root/core/method_length.py          48     10    79%
/Users/jbalkovec/Desktop/CPSC4260/project_root/core/param_length.py           35      2    94%
/Users/jbalkovec/Desktop/CPSC4260/project_root/core/refactor.py              126     15    88%
/Users/jbalkovec/Desktop/CPSC4260/project_root/gui/new_ui.py                 185     82    56%
/Users/jbalkovec/Desktop/CPSC4260/project_root/utils/exceptions.py            45      3    93%
/Users/jbalkovec/Desktop/CPSC4260/project_root/utils/logger.py                29      5    83%
/Users/jbalkovec/Desktop/CPSC4260/project_root/utils/utility.py              164      6    96%
conftest.py                                                                   48     10    79%
sys_test.py                                                                  152      1    99%
unit_tests.py                                                                250      6    98%
----------------------------------------------------------------------------------------------
TOTAL                                                                       1430    168    88%
coverage html
Wrote HTML report to htmlcov/index.html
```

- **Code Smells: `pylint`**

**Results as of now (Sat May 24th):**

This is the result of running `pylint` on the codebase. The `pylintrc` file is used to configure the pylint settings, this includes ignoring certain errors and warnings due to the nature of some packages used in the codebase, and some of my "hotfixes" that I have made in order to fix certain bugs. Nonetheless, the result should still reflect the overall quality of the codebase.

```plaintext
Your code has been rated at 10.00/10 (previous run: 9.93/10, +0.07)
```

- **Metrics: `radon`**
  - [ ] have cyclomatic complexity < 10, the lower the better
  - currently at `11.0`
  - **Critical:**
    - `refactor.py` is at `20.0`
    - `file_saver.py` is at `12.0`
    - `utility.py` is at `12.0`
    - `new_ui` is at `12.0`

**Results as of now (Fri May 23rd):**

```plaintext
Too large to display
```

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
