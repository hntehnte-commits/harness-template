# Skill: Compilation and Analysis

## Purpose
Standardize execution of compilers, test runners, and static analyzers, providing local models with a deterministic self-correction loop when errors occur.

---

## 1. Tool Execution Protocol
1. Read `active_profile` from `/.harness/artifacts/current_run/state.yaml`.
2. Load configuration (`test_command`, `lint_command`, and `bypass_qa_execution`):
   - Check if `active_profile` configuration file exists at `/.harness/profiles/<active_profile>/config.yaml`. If it does, read properties from there.
   - Otherwise, fallback to the base configuration at `/.harness/config.yaml`.
3. If `bypass_qa_execution` is `true`, **OMIT** command execution. Instead, perform a manual or static verification of contract compliance and syntax correctness.
4. If `bypass_qa_execution` is `false`, propose/Run the command exactly as defined in the loaded configuration and capture the full terminal output (both `stdout` and `stderr`).

---

## 2. Dynamic Self-Correction Protocol
When a command fails (returns non-zero exit code or logs error patterns):
1. **Identify Error Source**: Look for keywords like `Error`, `SyntaxError`, `Warning`, `LNK`, `FAILED`, `Exception`.
2. **Retrieve Line Reference**: Match the error to the exact file path and line number.
3. **Analyze Code Context**: Open the file at the referenced line and examine the surrounding 5 lines.
4. **Formulate Correction**:
   - For syntax/linter errors: correct spacing, type hints, or missing imports.
   - For test failures: verify assertions, mock implementations, or variable values.
5. **Re-Execute**: Run the compiler or linter again. If it fails again, repeat this analysis for a maximum of 3 times before raising the flag in `state.yaml` under `last_error`.
