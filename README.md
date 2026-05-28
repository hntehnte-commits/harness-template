# 🛡️ Multi-Agent Prompt Harness

This repository contains an advanced, professional **Multi-Agent Prompt Harness** designed to structure the behavior, workflow, and capabilities of Artificial Intelligence agents (such as **OpenCode**, **Claude Code**, **Roo Code**, or **Cursor**).

The harness implements a rigorous architecture focused on role separation, strict TDD validation, and concurrent management of multiple development profiles (embedded C, Python, and JavaScript) that can be dynamically installed, removed, or adapted.

---

## 🚀 Quick Start (First Run)

To start the harness and configure your favorite development tool:

1. **Clone the repository** into your workspace.
2. **Run the bootstrap script** from the root:
   ```bash
   python3 adapt_harness.py
   ```
   *Note: The first time you run it, the script will detect the absence of local dependencies, automatically create a secure virtual environment under `.harness/adaptation/.venv/`, and install the requirements in the background in a 100% transparent manner.*

---

## 🎨 Interactive Terminal Menu

If you run `python3 adapt_harness.py` without arguments, a premium interactive visual interface will be displayed:

```
==========================================================
🛡️  Harness Adaptation & Profile Manager - Interactive Menu
==========================================================
  1. ⚙️  Compile/Transpile Harness to OpenCode format (opencode)
  2. 📥  Install / Update a Profile in .opencode/ (install)
  3. 🧹  Remove a Profile from .opencode/ (remove)
  4. 🤖  Adapt Harness for Claude Code / Roo Code (claude)
  5. 💻  Adapt Harness for Cursor (cursor)
  6. 🔄  Sync AGENTS.md catalog (sync)
  7. ❌  Exit
==========================================================
```

### Available Options:
* **Compile for OpenCode (1)**: Transpiles the source templates under `.harness/` to the native OpenCode format and structure (`.opencode/`).
* **Install Profile (2)**: Dynamically choose which development profile (`python-developer`, `embedded-c-developer`, `javascript-developer`) to install as an overlay in your development environment.
* **Remove Profile (3)**: Cleanly and selectively remove a profile and all its specific skills/directives to prevent context leaks in the AI agent.
* **Adapt for Claude Code / Roo Code / Cursor (4 and 5)**: Generates the corresponding pointer files (`.clinerules` or `.cursorrules`) and syncs the manifest.
* **Sync Catalog (6)**: Dynamically re-indexes all available agents, roles, and skills and updates the master [`AGENTS.md`](file:///Users/hazaeltrejo/Documents/harness_template/AGENTS.md) file.

---

## 💻 Direct Command Line Usage (CLI)

If you prefer the terminal or are automating flows in a CI/CD pipeline, you can use command-line arguments directly:

* **Compile the entire harness for OpenCode**:
  ```bash
  python3 adapt_harness.py opencode
  ```
* **Install a specific profile**:
  ```bash
  python3 adapt_harness.py install python-developer
  ```
* **Remove a specific profile**:
  ```bash
  python3 adapt_harness.py remove python-developer
  ```
* **Adapt harness for Claude Code / Cursor**:
  ```bash
  python3 adapt_harness.py claude
  python3 adapt_harness.py cursor
  ```
* **Sync agent catalog**:
  ```bash
  python3 adapt_harness.py sync
  ```

## 📂 Repository Structure

- [**`.harness/`**](file:///Users/hazaeltrejo/Documents/harness_template/.harness/): **The Source of Truth**. Contains role templates, core skills, and profiles that you maintain in your repository. *(See the [`.harness/` README](file:///Users/hazaeltrejo/Documents/harness_template/.harness/README.md) for details).*
- [**`adapt_harness.py`**](file:///Users/hazaeltrejo/Documents/harness_template/adapt_harness.py): Self-managed Python virtual environment loader and bootstrap.
- [**`AGENTS.md`**](file:///Users/hazaeltrejo/Documents/harness_template/AGENTS.md): Dynamic central catalog and manifest that reads and indexes the actual agents and skills in your workspace to provide high-level context to the Orchestrator.
- **`.opencode/`** *(Generated)*: Transpiled harness folder ready for use by the local agent in OpenCode format.
- **`.clinerules` / `.cursorrules`** *(Generated)*: Directive/pointer files ready to feed Claude Code, Roo Code, or Cursor.
