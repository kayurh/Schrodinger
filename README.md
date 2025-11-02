# Schrödinger 🐱📁

A command-line tool that clones and organizes file directory structures based on file extensions (like `.en`, `.hu`, etc.) — useful for translation projects, multi-version documentation, or any task requiring language or variant-specific directories.

## ✨ Features
- Duplicate directory structures without changing data
- Organize files by extension or variant (e.g., `.en`, `.hu`)
- Safely copy files to a new destination
- CLI interface for easy use

## 🧩 Example Usage
```bash
python -m schrodinger.cli --src ./docs --dst ./output --ext .en

