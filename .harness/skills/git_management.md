# Skill: Git Management

## Purpose
Establish a secure execution protocol for Git operations in complex environments (multi-repo and symlink-heavy). The agent must prioritize **context verification** and **auditability** over direct execution.

---

## 1. Context Identification Protocol (Mandatory)
Before executing any command, the agent must validate the environment:
1. **Identification:** Run `git -C <path> rev-parse --show-toplevel`.
2. **Validation:** Compare the result with the expected path. If they do not match, **abort and report the error** to the user.
3. **Symlink Resolution:** If the path contains a symbolic link, run `readlink -f <path>` to obtain the real path before declaring the context.

## 2. Explicit Context Execution
* **Golden Rule:** Every Git command must include the `-C <path_to_repo>` flag.
* **Prohibition:** Never change the current working directory (avoid `cd`). Always maintain an absolute reference to the repository path.

## 3. Pre-Flight Check (State Validation)
Before any write operation (`commit`, `push`, `merge`, `reset`), the agent must generate a brief report:
1. **Status:** `git -C <path> status --short --branch`
2. **Diffs:** `git -C <path> diff --cached` (staged changes) and `git -C <path> diff` (unstaged changes).
3. **Confirmation:** The agent must list affected files and await approval if more than 3 files are modified or if changes are detected in configuration files (`.env`, `.gitignore`, `config/`).

## 4. Audit and Change Extraction (Diffing Commits)
For auditing history or specific changes between commits:
1. **Show specific commit:** Use `git -C <path> show <commit_hash>` to retrieve the changes and metadata for a specific commit.
2. **Diff between two commits:** Use `git -C <path> diff <commit_hash_1> <commit_hash_2>` to compare two points in history.
3. **Diff with parent:** Use `git -C <path> diff <commit_hash>^!` to see the exact changes introduced by a specific commit.
4. **Summary First:** If the diff is extensive, the agent must first run `git -C <path> diff --stat <commit_hash_1> <commit_hash_2>` to provide a summary of modified files before displaying detailed content.

## 5. Nested Repository Handling
* **Scanning:** When operating in a new directory, recursively scan for `.git` subdirectories.
* **Isolation:** If a nested repository is detected, treat it as an independent entity and **never** include its files in a `git add` command intended for the parent repository.

## 6. Security Policy (Destructive Actions)
* **Blocked Actions:** `git reset --hard`, `git push --force`, `git clean -xfd`, `git branch -D`.
* **Exception Protocol:**
    1. If strictly necessary, the agent must:
        a) Explain why it is necessary.
        b) Perform a "Safety Backup" (e.g., `git stash save "Backup pre-destructive-action"`).
        c) Request explicit user confirmation: *"Do you confirm you want to execute [command] on [repo]? This action is destructive."*

## 7. Error Handling
If a Git command returns a non-zero exit code:
1. **Do not retry automatically.**
2. Capture the `stderr`.
3. Analyze: Is it a permission issue, a merge conflict, or a missing repository?
4. Report back to the user with an actionable recommendation.

---

## 8. Quick Decision Tree

| Action | Pre-flight Required | Approval Required |
| :--- | :--- | :--- |
| **Read/Diff** | No | No |
| **Commit** | Yes (Diff) | If critical files are changed |
| **Push** | Yes (Branch/Remote check) | Always |
| **Destructive** | Yes (Backup + Analysis) | **ALWAYS** |