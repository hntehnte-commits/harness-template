# Multi-Agent Harness Architecture: Prompt-Driven Compilation & Dynamic Translation

This document defines the architectural design, workflow, and execution details for the **Multi-Agent Harness**. The system is modularly built around **Markdown Prompts** and **Context Directives**, enforcing a predictable, structured software development life cycle governed by a finite state machine and automated verification tools.

---

## 1. Directory Structure & Separation of Concerns

The harness strictly separates the **Source of Truth (Templates)** from the **Transpiled Environment (Execution Target)**. This decoupling ensures that template source files are kept generic, stack-independent, and easily editable, while the target environment is dynamic, optimized, and optimized for AI tools.

```text
/ (Workspace Root)
├── AGENTS.md                       # Master Manifest: Catalogs active agents, skills, and CLI tools
├── ARCHITECTURE.md                 # System Blueprint: Describes architectural pillars and workflows
├── adapt_harness.py                # Redirection Shell: Light wrapper that executes the main compiler
├── .gitignore                      # Version control exclusions
│
├── .harness/                       # SOURCE TEMPLATES (Source of Truth)
│   ├── config.yaml                 # Base Config: Defines stack, default tests, and lint commands
│   ├── roles/                      # Agent Master Prompts (Orchestrator, Dev, QA, Spec, Docs)
│   │    └── scripts/               # Role-Specific Scripts: Python scripts executed purely by agents
│   │         └── state_transition.py
│   ├── skills/                     # Skill Master Prompts (each skill is a directory)
│   │    ├── tdd-gatekeeper/        #   SKILL.md per skill directory
│   │    ├── state-management/
│   │    ├── skill-creator/
│   │    ├── file-translator/
│   │    ├── python-clean-architecture/
│   │    ├── python-performance-optimization/
│   │    ├── python-testing-and-quality-profile-specific/
│   │    ├── javascript-quality/
│   │    ├── async-state-management/
│   │    ├── typescript-strict-safety/
│   │    ├── c-memory-analyzer/
│   │    ├── compilation-and-analysis/
│   │    ├── autosar-architecture/
│   │    ├── embedded-deep-reasoning/
│   │    ├── trace32-cmm-scripting/
│   │    ├── git-management/
│   │    └── scripts/               # Global skill scripts
│   │         ├── tdd_gatekeeper_runner.py
│   │         └── skill_creator_cli.py
│   ├── memory/                     # Shared Memory templates (ADR & Lessons Learned bases)
│   ├── artifacts/templates/        # Deliverable Schemas (Plans, tasks, walkthroughs)
│   ├── profiles/                   # Multi-Stack Profiles (embedded-c, python, javascript, etc.)
│   └── adaptation/                 # Compiler and Virtual Environment Isolation
│       ├── .venv/                  # Virtual environment created and managed dynamically
│       ├── requirements.txt        # Python dependency manifest (zero-dependency design)
│       └── scripts/                # Compiler Engine Core Python scripts
│           ├── state_manager.py    # Core State Manager (shared by roles and skills)
│           └── transpiler_core.py  # Main transpiler script (manages compilation process)
│
└── .opencode/                      # GENERATED ENVIRONMENT (Transpiled Target)
    ├── config.yaml                 # Active Stack Profile configuration
    ├── instructions.md             # Immediate pointer directing AI tools to AGENTS.md
    ├── agents/                     # Transpiled and formatted agents (roles)
    │    └── scripts/               # Compiled role scripts
    ├── skills/                     # Compiled skills (filtered dynamically based on active profile)
    │    └── scripts/               # Compiled skill scripts
    ├── memory/                     # Active dynamic memory files (persistence layer)
    └── artifacts/current_run/      # State Machine (Contains active task checklists and state YAML)
```

---

## 2. Five Pillars of the Technical Design

### 2.1. Rigorous Orchestration (Orchestrator Role)
The **Orchestrator** acts as the *Project Manager* or *Engineering Director*. It supervises the high-level execution context by scanning [`AGENTS.md`](file:///Users/hazaeltrejo/Documents/harness_template/AGENTS.md) and active run state deliverables.
* **Golden Rule**: The Orchestrator NEVER writes production code or implements parches directly.
* **Mechanism**: It delegates work units by instructing the underlying model to assume specialized agent roles (e.g., `/.opencode/agents/developer.md`).

### 2.2. Artifact-Driven State Machine
The development lifecycle is governed by an explicit finite state machine based on structured deliverables and schemas:
* `state.yaml`: Catalogs current phase, active agent, profile, checklist tasks, and test results, strictly validating against `state_schema.yaml`.
* `implementation_plan.md`: Defines requirements, acceptance criteria, design schemas, and technical specifications.
* `task.md`: Serves as a live TODO checklist, tracking completed and in-progress tasks.
* `walkthrough.md`: Summarizes final implemented changes, lint outcomes, and test results.

### 2.3. Executable Execution Discipline (Strict TDD Gatekeeper)
The *Developer Agent* operates under the strict constraints of the `strict-tdd-gatekeeper` skill:
1. **Red Phase**: Force-writes a failing test signature before implementing any code. If the test passes early, it is flagged as a false test and rejected.
2. **Green Phase**: Implements the minimum production code required to make the test pass.
3. **Refactor Phase**: Cleans and optimizes the codebase while verifying linter rules and keeping the test suite green.

### 2.4. Segmented Long-Term & Dynamic Memory
Memory is compartmentalized to avoid hallucinations and maintain context sizes:
* **Architecture Decisions (ADR)**: `architecture_decisions.md` (Static architecture limits).
* **Lessons Learned**: `lessons_learned.md` (Dynamic memory. The QA Agent registers issues, bugs, and fixes during audits so future sessions avoid repeating past mistakes).

### 2.5. Profile-Aware Modular Skills Registry
Capabilities are packaged as modular plugins under `/.opencode/skills/`. The compiler registers these based on enabled profiles (e.g., Python profile disables JS and Embedded C skills), saving up to 80% of context window space.

---

## 3. Coexistence & Self-Managed Transpilation

The prompt transpiler enables multi-stack coexistence (`embedded-c-developer`, `python-developer`, `javascript-developer`):
1. **Concurrent Stacks**: The engine compiles global templates and mounts stack-specific properties cleanly.
2. **Dynamic Hot-Loading**: Agents inspect active workspace files at initialization, dynamically selecting the profile and configuring linters, tests, and bypass constraints (e.g., `bypass_qa_execution` for complex embedded system cross-compilations).
3. **Atomic Scaffolding**: Folder scaffolding and script compilations isolate stacks cleanly, keeping the workspace extremely light.

---

## 4. Automation Python Scripts & CLI Tools

To guarantee 100% execution safety, zero formatting syntax errors, and prevent YAML corruption, the harness incorporates four automated CLI scripts.

### 4.1. Harness State Manager (`state_manager.py`)
- **Location**: `.harness/adaptation/scripts/state_manager.py` (Compiled to `.opencode/core/state_manager.py`).
- **Description**: Zero-dependency module that parses, updates, and validates the state machine against `state_schema.yaml`. It exposes commands `state get` and `state update` under `adapt_harness.py`.

### 4.2. Agent State Transition (`state_transition.py`)
- **Location**: `.harness/roles/scripts/state_transition.py` (Compiled to `.opencode/agents/scripts/state_transition.py`).
- **Description**: Used by agents (roles) to transition between phases and agents. It automatically validates changes, saves them cleanly, and prints the standard transition directive tag (e.g., `--> NEXT ROLE: QA Agent`).

### 4.3. TDD Gatekeeper Runner (`tdd_gatekeeper_runner.py`)
- **Location**: `.harness/skills/scripts/tdd_gatekeeper_runner.py` (Compiled to `.opencode/skills/scripts/tdd_gatekeeper_runner.py`).
- **Description**: Executed by the developer agent during TDD verification. It resolves bypass parameters, executes linters and test suites, interprets outputs, and logs failures into `state.yaml`'s `last_error` field automatically.

### 4.4. Skill Creator CLI (`skill_creator_cli.py`)
- **Location**: `.harness/skills/scripts/skill_creator_cli.py` (Compiled to `.opencode/skills/scripts/skill_creator_cli.py`).
- **Description**: Executed by the skill-creator agent to scaffold new skills, write standard SKILL.md templates, and run the compiler to dynamically catalog them inside `AGENTS.md`.
