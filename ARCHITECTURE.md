# Agent Harness Architecture: Prompt-Based Design

This document defines the architecture and workflow for a generic **Agent Harness**, designed entirely around **Markdown Prompts**. It transforms raw AI autonomy into controlled, predictable, and verifiable engineering work.

## 1. Directory Architecture (Agnostic)

The structure is designed to separate responsibilities and isolate state. It relies on the AI reading these files to assume roles or learn rules.

```text
/ (Project Root)
├── AGENTS.md                   # Global Context: Defines source code locations and project map.
├── .harness/                   # The Core Harness Environment
│   ├── roles/                  # System Prompts for Sub-agents (Workers)
│   │   ├── orchestrator.md     # Central coordinator. Delegates, does not execute code.
│   │   ├── spec_agent.md       # Defines contracts and specifications.
│   │   ├── dev_agent.md        # Writes code purely focused on passing tests.
│   │   └── qa_agent.md         # Verifies deliverables and updates memory.
│   │
│   ├── artifacts/              # Source of Truth and State Machine
│   │   ├── templates/          # YAML schemas for the agents to fill out.
│   │   └── current_run/        # State of the current task (e.g., 03_design.yaml).
│   │
│   ├── memory/                 # Persistence System
│   │   ├── architecture_decisions.md # Immutable technical constraints.
│   │   └── lessons_learned.md  # Dynamic memory of bugs and gotchas to avoid.
│   │
│   ├── skills/                 # Protocols and Operating Procedures
│   │   ├── tdd_gatekeeper.md   # Step-by-step instructions for Red-Green-Refactor.
│   │   └── state_management.md # Instructions on how to manage YAML artifacts safely.
│   │
│   └── config.yaml             # Tech stack configuration for the current project.
```

---

## 2. The 5 Design Pillars

### 2.1. Orchestration (Orchestrator)
The **Orchestrator** acts as an *Engineering Manager*. It maintains high-level context by reading `AGENTS.md` and the artifacts.
- **Golden Rule:** It never writes or executes source code.
- **Mechanism:** It delegates tasks by instructing the AI (e.g., Claude Code) to load the prompt of another role (e.g., `/.harness/roles/dev_agent.md`).

### 2.2. Artifacts & Grammar (State Machine)
The development process is a **finite state machine** driven by YAML files.
*   `02_specification.yaml`: Exact requirements, edge cases, and acceptance criteria.
*   `03_design.yaml`: Architecture, interfaces, and function signatures.
If the agent loses context or the session closes, the Orchestrator simply reads `current_run/` to know exactly where it left off.

### 2.3. Runtime Discipline (Strict TDD Gatekeeper)
The *Discipline* component is injected via the `tdd_gatekeeper.md` skill. The *Dev Agent* is forced to read this skill.
1.  **Red Phase:** The agent must write a failing test and run it in the terminal. If it passes (green), the agent is instructed to reject it for being a fake test.
2.  **Green Phase:** The agent writes the code. If the test fails, it corrects it.
3.  **Refactor Phase:** Clean up.

### 2.4. Persistence (Memory System)
Memory is divided into explicit Markdown files to prevent hallucination:
*   **Long-Term Memory (ADR):** `architecture_decisions.md` (e.g., "We mock the database using X, not Y").
*   **Dynamic Memory:** `lessons_learned.md`. The QA Agent appends notes here after every task so future sessions don't repeat the same mistakes.

### 2.5. Skills Registry
Instead of giving the agent open access to guess how to do things, we provide explicit protocols in `/.harness/skills/`. The orchestrator restricts these skills according to the phase.

---

## 3. Workflow Example

1.  **Bootstrapping & Context Loading:**
    *   User provides the task. The AI reads `AGENTS.md` and `/.harness/roles/orchestrator.md`.
    *   The Orchestrator reads `config.yaml` and hydrates the long-term memory.

2.  **Contractual Phase (Spec & Design):**
    *   Orchestrator delegates to the *Spec Agent*.
    *   The *Spec Agent* fills out `02_specification.yaml` and `03_design.yaml`.

3.  **Discipline Phase (The TDD Loop):**
    *   Orchestrator delegates to the *Dev Agent*.
    *   *Dev Agent* reads the `tdd_gatekeeper.md` skill, writes the failing test, verifies failure, writes code, and verifies success.

4.  **Audit and Closure:**
    *   Orchestrator delegates to the *QA Agent*.
    *   The QA Agent audits the code, updates `lessons_learned.md`, and closes the task.
