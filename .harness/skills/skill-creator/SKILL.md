# Skill: Skill Creator

## Purpose
Empower the agent to convert chat histories, repetitive instructions, or specific procedures into highly structured, reusable skills under the multi-agent Harness system using the automated skill creator CLI and associated automation scripts.

---

## 1. Skill Extraction and Analysis
When the user requests to save a procedure as a skill, or when a repetitive/complex activity is successfully completed in the chat:
1. **Analyze Conversation History**: Review the exact steps, tools used, and logical flow of the target activity.
2. **Identify Constants & Variables**: Separate project-specific details from the generic protocol.
3. **Determine Scope**: Decide if the skill should be **Global** or **Profile-Specific** (e.g., Python-specific).

---

## 2. Skill Generation Protocol
Instead of manually creating files and directories, run the automated CLI tool:

1. **Create the Skill**: Run the following command in the workspace root:
   ```bash
   python3 .harness/skills/scripts/skill_creator_cli.py --name "[Proper Capitalized Skill Name]" --description "[Concise, clear purpose of the skill]" [--profile <profile_name>]
   ```
   *Example*: `python3 .harness/skills/scripts/skill_creator_cli.py --name "Git Management" --description "Establish secure git protocols."`

2. **Draft the Content**:
   - Open the newly created `SKILL.md` at `.harness/skills/<skill-folder-name>/SKILL.md`.
   - Populate the template sections with your extracted guidelines, tools, and constraints.

3. **Implement Automation Scripts (ONLY when explicitly requested)**:
   > **IMPORTANT**: Do NOT create Python scripts by default. Only implement an automation script if the user **explicitly asks** for it — e.g., with phrases like *"con scripts de python"*, *"with python automation"*, *"automate it with a script"*, or similar.

   If (and only if) the user explicitly requests Python automation:
   - Write a clean, zero-dependency Python script for the task.
   - Save it inside the skill's assets folder: `.harness/skills/<skill-folder-name>/assets/<script_name>.py`
   - Document the script's CLI interface in `SKILL.md` (flags, exit codes, usage examples).

4. **Compile and Catalog**:
   - Re-run the harness compilation to propagate the drafted content and compile assets:
     ```bash
     python3 adapt_harness.py opencode
     ```

5. **Notify the User**: Show the user where the new skill was created, list any automation scripts (if created), and confirm it is ready to use.
