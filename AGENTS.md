# Agent Context Manifest (AGENTS.md)

This file provides the AI Agent (Orchestrator) with the global context of the project, including where to find source code and how the harness is structured.

## 1. Project Information
- **Project Name**: [Nombre del Proyecto]
- **Description**: [Descripción de lo que hace tu software]
- **Source Code Location**: `/src/` (Asegúrate de cambiar esto a tu carpeta real de código)
- **Tests Location**: `/tests/` (Asegúrate de cambiar esto a tu carpeta real de tests)

## 2. Harness Architecture Overview
This project is governed by a strict **Multi-Agent Prompt Harness** located in `/.harness/`.
The AI agent must never act freely; it must adopt a specific "Role" to perform a task.

### Available Sub-Agents (Roles)
- **Orchestrator** (`/.harness/roles/orchestrator.md`): Coordinates the workflow. Delegates tasks. Never writes code.
- **Spec Agent** (`/.harness/roles/spec_agent.md`): Generates strict YAML specifications and architectural designs.
- **Dev Agent** (`/.harness/roles/dev_agent.md`): Writes code strictly following Red-Green-Refactor TDD.
- **QA Agent** (`/.harness/roles/qa_agent.md`): Audits the code against the design and updates the system's memory.

## 3. Memory & Artifacts
The Orchestrator and sub-agents must read from and write to these locations to maintain state:
- **State Machine (Artifacts)**: `/.harness/artifacts/current_run/` (Contains the YAMLs defining the current task).
- **Long-Term Memory**: `/.harness/memory/architecture_decisions.md` (Constraints and rules).
- **Dynamic Memory**: `/.harness/memory/lessons_learned.md` (Gotchas and past mistakes to avoid).

## 4. Initialization
When the AI is first loaded into this project, it must read this `AGENTS.md` file, understand the project layout, and then immediately read `/.harness/roles/orchestrator.md` to assume the Orchestrator role.
