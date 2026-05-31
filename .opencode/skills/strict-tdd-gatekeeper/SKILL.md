---
name: strict-tdd-gatekeeper
description: Enforce strict Red-Green-Refactor testing protocol during implementation, preventing application logic from being written without a verifying unit test, utilizing the automated TDD validation script.
---

# Skill: Strict TDD Gatekeeper

## Purpose
Enforce strict Red-Green-Refactor testing protocol during implementation, preventing application logic from being written without a verifying unit test, utilizing the automated TDD validation script.

---

## TDD Step-by-Step Checklist

### Phase 1: Contract Analysis
1. Read the design file `/.opencode/artifacts/current_run/03_design.yaml` to identify the required functions, parameters, and signatures.
2. Retrieve the `active_profile` from `/.opencode/artifacts/current_run/state.yaml` (using `state get`).
3. Do NOT write any application code at this stage.

### Phase 2: Red Phase (Failing Test)
1. Write a new unit test in the test suite that calls the unwritten feature according to the design signature.
2. Execute the automated TDD gatekeeper validation for the RED phase:
   ```bash
   python3 -m skills.scripts.tdd_gatekeeper_runner --phase red
   ```
3. If the script succeeds (returns 0), the test failed as expected (RED). If it fails (returns 1), the tests either passed or there was an configuration issue. Correct your tests and repeat until the script confirms RED phase.

### Phase 3: Green Phase (Minimal Code)
1. Write the **minimal** application code required to make the test pass. Avoid any extra logic or over-engineering.
2. Execute the automated TDD gatekeeper validation for the GREEN phase:
   ```bash
   python3 -m skills.scripts.tdd_gatekeeper_runner --phase green
   ```
3. If it succeeds, the tests are GREEN and you can proceed. If it fails, read the printed test failure details, fix the code, and re-run until it returns success.

### Phase 4: Refactor Phase (Clean Code)
1. Optimize the implemented code for readability, DRY principles, and structural cleanliness.
2. Execute the automated TDD gatekeeper validation for the REFACTOR phase:
   ```bash
   python3 -m skills.scripts.tdd_gatekeeper_runner --phase refactor
   ```
3. If it fails (either due to linter or tests), fix the refactored code and repeat.
4. Once verified GREEN, update the checklist item status in the state machine and `task.md`.
