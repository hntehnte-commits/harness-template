---
name: strict-tdd-gatekeeper
description: Enforce strict Red-Green-Refactor testing protocol during implementation, preventing application logic from being written without a verifying unit test.
---

# Skill: Strict TDD Gatekeeper

## Purpose
Enforce strict Red-Green-Refactor testing protocol during implementation, preventing application logic from being written without a verifying unit test.

---

## TDD Step-by-Step Checklist

### Phase 1: Contract Analysis
1. Read the design file `/.opencode/artifacts/current_run/03_design.yaml` to identify the required functions, parameters, and signatures.
2. Retrieve the `active_profile` from `/.opencode/artifacts/current_run/state.yaml`.
3. Load the `bypass_qa_execution` flag:
   - Check if `active_profile` configuration file exists at `/.opencode/profiles/<active_profile>/config.yaml`. If it does, read `project.bypass_qa_execution` from there.
   - Otherwise, fallback to the base configuration at `/.opencode/config.yaml`.
4. Do NOT write any application code at this stage.

### Phase 2: Red Phase (Failing Test)
1. Write a new unit test in the test suite that calls the unwritten feature according to the design signature.
2. If `bypass_qa_execution` is `true`, skip running the test runner command; statically verify that the test targets the correct unwritten function and proceed.
3. If `bypass_qa_execution` is `false`, run the test runner command from `config.yaml`. Verify that the test fails (RED). If the test passes or does not execute, rewrite it.

### Phase 3: Green Phase (Minimal Code)
1. Write the **minimal** application code required to make the test pass. Avoid any extra logic or over-engineering.
2. If `bypass_qa_execution` is `true`, skip running the test runner command; statically verify contract compliance and proceed.
3. If `bypass_qa_execution` is `false`, run the test runner command. If it fails, read output, correct code, and repeat until tests are GREEN.

### Phase 4: Refactor Phase (Clean Code)
1. Optimize the implemented code for readability, DRY principles, and structural cleanliness.
2. If `bypass_qa_execution` is `true`, skip running the test runner command; statically inspect the files and proceed.
3. If `bypass_qa_execution` is `false`, run the test runner again. If it fails, revert and restore green state.
4. Once refactored (and verified), mark the checklist item as completed in `state.yaml` and update `task.md`.
