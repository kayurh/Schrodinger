# Schrödinger 🐱📁

A command-line tool that clones and organizes file directory structures based on file extensions (like `.en`, `.hu`, etc.) — useful for translation projects, multi-version documentation, or any task requiring language or variant-specific directories.

---

## ✨ Features
- Duplicate directory structures without changing data
- Organize files by extension or variant (e.g., `.en`, `.hu`)
- Safely copy files to a new destination
- CLI interface for easy use

---

## ⚙️ Installation (Setting up locally)
1. Clone the repository:   
   git clone https://github.com/YOUR_USERNAME/schrodinger.git
   cd schrodinger

2. Install Dependencies: 
   pip install -r requirements.txt

---

## 🧰 Project Structure

```bash
schrodinger/
├── schrodinger/
│   ├── cli.py
│   ├── core.py
│   └── utils.py
├── tests/
│   ├── test_core.py
│   └── test_cli.py
├── examples/
│   └── sample_project/
├── README.md
├── requirements.txt
└── setup.py

```
---

### 📁 **Description of Files**

| File / Folder              | Purpose                                        |
| -------------------------- | ---------------------------------------------- |
| `cli.py`                   | Command-line interface and user input handling |
| `core.py`                  | Core file-cloning logic                        |
| `utils.py`                 | Helper and utility functions                   |
| `test_core.py`             | Unit tests for core logic                      |
| `test_cli.py`              | Tests for command-line behavior                |
| `sample_project/`          | Example input files for testing                |
| `requirements.txt`         | Dependency list                                |
| `setup.py`                 | Installation and packaging script              |

---

## 🗓️ 1-Month Development Schedule for “Schrödinger”

This schedule outlines the one-month plan for building and polishing the **Schrödinger CLI** tool — from setup to final release.

| **Week** | **Goal** | **Key Tasks** | **Deliverables / Checkpoints** |
|-----------|-----------|---------------|--------------------------------|
| **Week 1 – Setup & Familiarization** | Establish the project foundation | • Set up Python 3.10+ and PyCharm environment<br>• Create GitHub repo and add README + LICENSE<br>• Review starter code structure<br>• Run initial file-cloning tests | ✅ Project runs locally<br>✅ Repo live with README and LICENSE |
| **Week 2 – Core Functionality** | Implement and test the core logic | • Learn `os`, `shutil`, and `argparse` modules<br>• Implement `core.py` to clone directory structures<br>• Add filtering by extension (e.g., `.en`, `.hu`)<br>• Write initial unit tests in `tests/test_core.py` | ✅ CLI works with `.en` and `.hu` filters<br>✅ Tests pass for core logic |
| **Week 3 – CLI & Enhancements** | Improve interactivity and usability | • Finalize `cli.py` argument parser<br>• Add `--verbose`, `--dry-run`, and logging<br>• Add optional progress bar using `tqdm`<br>• Improve console messages and error handling | ✅ Full CLI interface operational<br>✅ Progress bar and logging integrated |
| **Week 4 – Testing & Release** | Polish, document, and publish | • Refactor code to follow PEP 8<br>• Expand unit tests and validate edge cases<br>• Update `README.md` with usage examples & diagrams<br>• Tag version `v1.0.0` and create final GitHub release | ✅ All tests passing<br>✅ Documentation complete<br>✅ Version 1.0 released |

---

### 🧠 Weekly Learning Focus

| **Week** | **Topics to Study** | **Focus Area** |
|-----------|--------------------|----------------|
| 1 | Git & GitHub basics | Repository setup, commits, pushing changes |
| 2 | File I/O, directory traversal | Using `os.walk()` and `shutil.copy2()` |
| 3 | CLI building & logging | Using `argparse`, `logging`, and `tqdm` |
| 4 | Testing & documentation | Writing tests with `pytest`, improving README |

---

## 📜 License
Distributed under the MIT License.  
See `LICENSE` for more information.

