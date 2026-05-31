# Agent Context Manifest (AGENTS.md)

This file provides the AI Agent (Orchestrator) with the global context of the project, including where to find source code and how the harness is structured.

## 1. Project Information
- **Project Name**: My AI Harnessed Project
- **Active Profile / Stack**: python
- **Test Command**: `pytest`
- **Lint Command**: `flake8`
- **Source Code Location**: `/src/` (Asegúrate de cambiar esto a tu carpeta real de código)
- **Tests Location**: `/tests/` (Asegúrate de cambiar esto a tu carpeta real de tests)

## 2. Harness Architecture Overview
This project is governed by a strict **Multi-Agent Prompt Harness** located in `/.opencode/`.
The AI agent must never act freely; it must adopt a specific "Role" to perform a task.

### Available Sub-Agents (Roles)
- **Developer Agent** (`/.opencode/agents/developer.md`)
- **Documentation Agent** (`/.opencode/agents/docs.md`)
- **Embedded Developer Agent** (`/.opencode/agents/embedded-developer.md`)
- **Javascript Developer Agent** (`/.opencode/agents/javascript-developer.md`)
- **Orchestrator** (`/.opencode/agents/orchestrator.md`)
- **Python Developer Agent** (`/.opencode/agents/python-developer.md`)
- **QA Agent** (`/.opencode/agents/qa.md`)
- **Specification Agent** (`/.opencode/agents/spec.md`)

## 3. Memory & Artifacts
The Orchestrator and sub-agents must read from and write to these locations to maintain state:
- **State Machine (Artifacts)**: `/.opencode/artifacts/current_run/` (Contains the YAMLs defining the current task).
- **Long-Term Memory**: `/.opencode/memory/architecture_decisions.md` (Constraints and rules).
- **Dynamic Memory**: `/.opencode/memory/lessons_learned.md` (Gotchas and past mistakes to avoid).

## 4. Initialization
When the AI is first loaded into this project, it must read this `AGENTS.md` file, understand the project layout, and then immediately read `/.opencode/agents/orchestrator.md` to assume the Orchestrator role.

### Available Skills
- **File Translator** (`/.opencode/skills/file-translator/SKILL.md`)
- **Python Clean Architecture** (`/.opencode/skills/python-clean-architecture/SKILL.md`)
- **Python Performance Optimization** (`/.opencode/skills/python-performance-optimization/SKILL.md`)
- **Python Testing and Quality (Profile Specific)** (`/.opencode/skills/python-testing-and-quality-profile-specific/SKILL.md`)
- **Skill Creator** (`/.opencode/skills/skill-creator/SKILL.md`)
- **State Management** (`/.opencode/skills/state-management/SKILL.md`)
- **Strict TDD Gatekeeper** (`/.opencode/skills/strict-tdd-gatekeeper/SKILL.md`)

## 5. Automated Harness CLI Commands
To guarantee execution safety, schema consistency, and zero formatting syntax errors, agents and skills MUST interact with the harness through the following automated CLI scripts (never modify `state.yaml` manually!):

### 5.1 State Management (Read & Update)
Used by skills and agents to inspect and update keys in `state.yaml` without corrupting the YAML structure.
- **Inspect State**:
  ```bash
  python3 adapt_harness.py state get
  ```
- **Update Key**:
  ```bash
  python3 adapt_harness.py state update --key <key_name> --value <value>
  ```
  *Example*: `python3 adapt_harness.py state update --key plan_approved --value true`

### 5.2 Agent Transitions (Transition Agent & Phase)
Used by agents/roles to transfer execution control cleanly, validate schema, and output the required transition directive string.
- **Execute Transition**:
  ```bash
  python3 -m agents.scripts.state_transition --agent <agent_id> --phase <phase_name>
  ```
  *Example*: `python3 -m agents.scripts.state_transition --agent spec --phase Contract`
  *Standard Output Directive*: `--> NEXT ROLE: Spec Agent` (Automatically printed at the end)

### 5.3 TDD Gatekeeper Validation (RED, GREEN, REFACTOR)
Used by developer agents to execute automated TDD checking (linters/tests based on config, including `bypass_qa_execution` handling and automatic failure logging).
- **Verify TDD Phase**:
  ```bash
  python3 -m skills.scripts.tdd_gatekeeper_runner --phase <red|green|refactor>
  ```

### 5.4 Skill Scaffolding and Auto-Compilation
Used by agents/skills to auto-generate a new skill skeleton, auto-compile it, and auto-register it in `AGENTS.md`.
- **Create and Register Skill**:
  ```bash
  python3 -m skills.scripts.skill_creator_cli --name "[Proper Capitalized Skill Name]" --description "[Short Purpose]"
  ```
