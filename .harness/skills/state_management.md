# Skill: State Management

## Purpose
To interact with the State Machine artifacts (`.harness/artifacts/current_run/`) safely, maintaining correct schemas and ensuring smooth transitions between agents.

---

## 1. Safety Rules
- Always output pure, valid YAML inside files.
- Do NOT include markdown codeblocks (```yaml) or conversational text within the saved file.
- Verify that every transition matches the `state_schema.yaml` template.

---

## 2. Reading State Protocol
1. Navigate to `/.harness/artifacts/current_run/state.yaml` (or the compiled path `/.opencode/artifacts/current_run/state.yaml`).
2. Read the file completely. If it is empty or missing, invoke the Orchestrator's initialization step to generate it.
3. Check `active_agent` to make sure it matches your own role.

---

## 3. Writing State Protocol
1. Parse your current task from the checklist array.
2. Mark completed items with `status: "completed"`.
3. Set the new active agent if you are transferring control (e.g. `active_agent: "dev"`).
4. Save the file exactly back to `/.harness/artifacts/current_run/state.yaml` (or compiled `.opencode` equivalent).
5. Output the explicit transition tag `--> NEXT ROLE: [Agent Name]` as the very last line of your execution.
