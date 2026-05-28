# Skill: [Skill Name]

## Purpose
[Provide a concise, one-sentence description of the skill's purpose and target context. IMPORTANT: The transcompiler extracts this first paragraph as the official description for the OpenCode YAML frontmatter, so make sure it is a single, clear paragraph of text without titles or markers.]

---

## 1. [First Technical Protocol / Procedure]
[Define the core procedure or step-by-step actions that the agent must execute. Use bold text for key terms and numbered lists for strict sequential execution.]

1. **Prerequisites Verification**: Validate that all required configuration, files, or environment parameters are present before starting.
2. **Sequential Step Title**: Detailed explanation of the action to be performed, including typical input or files involved.
3. **Execution Verification**: How to verify that this step succeeded before moving to the next.

---

## 2. [Second Technical Protocol / Decision Tree]
[Define specific rules, constraints, or adaptive behavior. E.g., what to do when something fails, or how to choose between options.]

* **Constraint Title**: Describe the strict constraint or forbidden actions (e.g., "Do not use X library").
* **Self-Correction Protocol**: What specific steps should the agent take if this step fails (limit to N retry attempts).

---

## 3. [Quality & Safety Guidelines]
[Specify code style, architecture rules, security, or profile-specific checks that must be observed.]

1. **Guideline 1**: Direct instructions on standard formatting or patterns.
2. **Guideline 2**: Clear verification assertions or checks to run before declaring the skill task complete.
