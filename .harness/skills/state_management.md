# Skill: State Management

## Purpose
To interact with the State Machine artifacts safely and cleanly, maintaining correct schemas and ensuring smooth transitions between agents using the automated CLI tool.

---

## 1. Safety Rules
- Use only the automated CLI commands (`python3 adapt_harness.py state ...`) to read and update state.
- Do NOT edit the `state.yaml` file manually to prevent schema corruption or formatting errors.
- Any manual transition or update is strictly prohibited unless the CLI tool fails.

---

## 2. Reading State Protocol
1. To inspect the current run state, run:
   ```bash
   python3 adapt_harness.py state get
   ```
2. Review the printed active agent, phase, and checklist. If `state.yaml` is empty or missing, it will automatically initialize.
3. Check `active_agent` to make sure it matches your own role.

---

## 3. Writing State Protocol
1. Parse your current task from the checklist.
2. When starting a task, update its status to `in_progress` if necessary, or simply mark it completed when finished.
3. To update a state key-value pair safely (such as `plan_approved` or `test_status`), run:
   ```bash
   python3 adapt_harness.py state update --key <key_name> --value <value>
   ```
   *Example*: `python3 adapt_harness.py state update --key plan_approved --value true`
4. If you need to transition to another agent, use the agent transition tool (described in the agent scripts) or let the Orchestrator handle the transition.
