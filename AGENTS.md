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
- **Developer Agent** (`/.opencode/agents/dev.md`)
- **Documentation Agent** (`/.opencode/agents/docs.md`)
- **Orchestrator** (`/.opencode/agents/orchestrator.md`)
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
- **Async State Management** (`/.opencode/skills/async-state-management/SKILL.md`)
- **AUTOSAR Software Architecture** (`/.opencode/skills/autosar-software-architecture/SKILL.md`)
- **C Memory Analyzer (Profile Specific)** (`/.opencode/skills/c-memory-analyzer-profile-specific/SKILL.md`)
- **Compilation and Analysis** (`/.opencode/skills/compilation-and-analysis/SKILL.md`)
- **Embedded Deep Reasoning** (`/.opencode/skills/embedded-deep-reasoning/SKILL.md`)
- **JavaScript Quality (Profile Specific)** (`/.opencode/skills/javascript-quality-profile-specific/SKILL.md`)
- **Python Clean Architecture** (`/.opencode/skills/python-clean-architecture/SKILL.md`)
- **Python Performance Optimization** (`/.opencode/skills/python-performance-optimization/SKILL.md`)
- **Python Testing and Quality (Profile Specific)** (`/.opencode/skills/python-testing-and-quality-profile-specific/SKILL.md`)
- **Skill Creator** (`/.opencode/skills/skill-creator/SKILL.md`)
- **State Management** (`/.opencode/skills/state-management/SKILL.md`)
- **Strict TDD Gatekeeper** (`/.opencode/skills/strict-tdd-gatekeeper/SKILL.md`)
- **TRACE32 CMM Scripting** (`/.opencode/skills/trace32-cmm-scripting/SKILL.md`)
- **TypeScript Strict Safety** (`/.opencode/skills/typescript-strict-safety/SKILL.md`)
