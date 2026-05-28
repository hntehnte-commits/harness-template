---
name: skill-creator
description: Empower the agent to convert chat histories, repetitive instructions, or specific procedures into highly structured, reusable skills under the multi-agent Harness system.
---

# Skill: Skill Creator

## Purpose
Empower the agent to convert chat histories, repetitive instructions, or specific procedures into highly structured, reusable skills under the multi-agent Harness system.

---

## 1. Skill Extraction and Analysis
When the user requests to save a procedure as a skill, or when a repetitive/complex activity is successfully completed in the chat:
1. **Analyze Conversation History**: Review the exact steps, tools used, and logical flow of the target activity.
2. **Identify Constants & Variables**: Separate project-specific details (e.g., specific file names, local variable values) from the generic protocol (e.g., step-by-step verification, self-correction, or tool patterns).
3. **Determine Scope**: Decide if the skill should be **Global** (placed directly under `.opencode/skills/`) or **Profile-Specific** (placed under `.opencode/profiles/<profile>/skills/`).
   * *Global*: Transversal skills useful for any stack (e.g., state management, git workflows).
   * *Profile-Specific*: Skills tied to a single language or framework (e.g., python testing, C memory auditing).

---

## 2. Skill Generation Protocol
1. **Load Template**: Read the skill structure template from `/.opencode/skills/skill-creator/assets/SKILL_TEMPLATE.md`.
2. **Format and Metadata**:
   * Create the file named in lower-snake-case (e.g. `my_new_skill.md`) if it's a simple skill, or a directory of the same name containing `SKILL.md` if the skill requires additional assets (like templates or scripts).
   * Ensure the **first line** is `# Skill: [Proper Capitalized Skill Name]`.
   * Ensure the **second paragraph** (under `## Purpose`) is a single, concise paragraph with no formatting tags, as the transpiler extracts this first block as the description metadata for the agent frontmatter.
3. **Draft the Content**: Populate sections `## 1.`, `## 2.`, and `## 3.` with the extracted step-by-step instructions, constraints, and dynamic self-correction loops.

---

## 3. Transpilation & Synchronization
Once the new skill file or directory is written:
1. **Verify Local Path**: Ensure the new file resides in `.opencode/skills/` (or `.opencode/profiles/<profile>/skills/`).
2. **Compile Harness**: Execute the harness transcompiler to propagate changes to `.opencode/` and update the master index:
   ```bash
   python3 adapt_harness.py opencode
   ```
3. **Verify Generation**:
   * Check that `.opencode/skills/<skill-name>/SKILL.md` was created and includes the correct OpenCode YAML frontmatter.
   * Verify that the new skill is correctly cataloged in `AGENTS.md` under `### Available Skills`.
4. **Notify the User**: Show the user where the new skill has been created and confirm it is ready to be used by any subagent.
