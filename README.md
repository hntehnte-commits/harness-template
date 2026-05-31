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
* **Sync Catalog (6)**: Dynamically re-indexes all available agents, roles, and skills and updates the master [`AGENTS.md`](AGENTS.md) file.

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

---

## 📂 Repository Structure

### Root Overview

- [**`.harness/`**](.harness/): **The Source of Truth**. Contains role templates, core skills, and profiles that you maintain in your repository. *(See detailed structure below).*
- [**`adapt_harness.py`**](adapt_harness.py): Self-managed Python virtual environment loader and bootstrap.
- [**`AGENTS.md`**](AGENTS.md): Dynamic central catalog and manifest that reads and indexes the actual agents and skills in your workspace to provide high-level context to the Orchestrator.
- **`.opencode/`** *(Generated)*: Transpiled harness folder ready for use by the local agent in OpenCode format.
- **`.clinerules` / `.cursorrules`** *(Generated)*: Directive/pointer files ready to feed Claude Code, Roo Code, or Cursor.

### The Harness Engine and Source of Truth (`.harness/`)

This directory is the **Single Source of Truth** for your entire multi-agent system. It is the exclusive place where you should make long-term modifications to directives, roles, skills, or development profiles.

```
.harness/
├── config.yaml                     # General configuration and default project stack
├── roles/                          # Master prompts for global subagents (Orchestrator, Dev, QA, etc.)
├── skills/                         # Cross-cutting base harness skills (each skill is a directory with SKILL.md)
├── memory/                         # Shared base memory files (architecture and lessons learned)
├── artifacts/
│   └── templates/                  # Templates for implementation plans, tasks, and walkthroughs
├── profiles/                       # Specific overlays for each development stack
│   ├── embedded-c-developer/       #   - Profile for Embedded C development
│   ├── python-developer/           #   - Profile for Python development
│   └── javascript-developer/       #   - Profile for JS / TS development
└── adaptation/                     # Transpiler engine and isolated runtime environment
    ├── requirements.txt            # Engine dependencies
    └── scripts/                    # Modular transpiler scripts
```

#### 1. `roles/` (Core Subagents)

Markdown prompts that define the personality, responsibilities, and strict constraints of each role:

* `orchestrator.md`: Launches subagents, manages priorities, and validates overall goal compliance.
* `spec_agent.md`: Validates requirements and drafts design plans and specifications.
* `dev_agent.md`: Writes source code strictly adhering to technical standards.
* `qa_agent.md`: Runs linters, test suites, and implements optional QA bypass.
* `docs_agent.md`: Generates clean final documentation and change walkthroughs.

#### 2. `skills/` (Core Skills)

Modular technical directives that inject special capabilities. Each skill is a directory containing a `SKILL.md` and optionally an `assets/` subfolder with the skill's own scripts.

* `state-management/`: State flow rules through artifacts (`implementation_plan.md`, `task.md`, `walkthrough.md`).
* `tdd-gatekeeper/`: Rigorous test-driven development logic before proceeding with production code.
* `git-management/`: Safe Git protocols in multi-repo environments.

#### 3. `profiles/` (Profiles and Specialization Layers)

Profiles allow multiple technology stacks to coexist concurrently. Each profile can extend the core harness by adding:

* `config.yaml`: Overrides active stack variables, test commands (`pytest`, `make test`, `npm test`), linters (`flake8`, `cppcheck`, `eslint`), and settings like `bypass_qa_execution`.
* `skills/`: Adds skills dedicated to that profile (e.g. `c-memory-analyzer/` for the C developer). These are automatically indexed uniquely under `.opencode/skills/` and listed in `AGENTS.md`.
* `memory/`: Injects language-specific design directives and tips.

---

## 🛠️ How to Add a New Profile

Adding support for a new technology stack (e.g., `rust-developer`) is very simple and clean:

1. **Create a profile directory**:
   ```bash
   mkdir -p .harness/profiles/rust-developer/skills
   mkdir -p .harness/profiles/rust-developer/memory
   ```
2. **Create its `config.yaml` file** specifying the particulars:
   ```yaml
   name: Rust Developer Profile
   stack: rust
   test_command: cargo test
   lint_command: cargo clippy
   bypass_qa_execution: false
   ```
3. **Add specific skills** (e.g. `rust_borrow_checker.md`) inside its `skills/` folder.
4. **Re-compile the harness**:
   ```bash
   python3 adapt_harness.py opencode
   ```
   *The modular compilation engine will automatically:*
   * Copy the profile non-destructively and concurrently to `.opencode/profiles/rust-developer/`.
   * Register and transpile its specific Rust skill under `.opencode/skills/rust-borrow-checker/SKILL.md`.
   * Re-sync `AGENTS.md`, cleanly cataloging and linking the newly integrated skills.
