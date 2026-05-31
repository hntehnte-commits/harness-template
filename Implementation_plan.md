# Skill Directory Unification

## Background

Currently, skills in `.harness/skills/` use **two different formats**:

| Format | Example | Supports `assets/`? | Supports `scripts/`? |
|---|---|---|---|
| Flat `.md` file | `tdd_gatekeeper.md` | ❌ | ❌ |
| Directory | `skill-creator/SKILL.md` | ✅ | ✅ |

The goal is to migrate **every** skill to the directory format so all skills are consistent, extendable, and match how `.opencode/skills/` already works.

### Target structure (source of truth)
```
.harness/skills/
├── tdd-gatekeeper/
│   └── SKILL.md
├── state-management/
│   └── SKILL.md
├── python-clean-architecture/
│   └── SKILL.md
├── python-performance-optimization/
│   └── SKILL.md
├── python-testing-and-quality-profile-specific/
│   └── SKILL.md
├── git-management/
│   └── SKILL.md
├── javascript-quality/
│   └── SKILL.md
├── typescript-strict-safety/
│   └── SKILL.md
├── async-state-management/
│   └── SKILL.md
├── c-memory-analyzer/
│   └── SKILL.md
├── compilation-and-analysis/
│   └── SKILL.md
├── autosar-architecture/
│   └── SKILL.md
├── embedded-deep-reasoning/
│   └── SKILL.md
├── trace32-cmm-scripting/
│   └── SKILL.md
├── skill-creator/            ← already directory ✅
│   └── SKILL.md
├── file-translator/          ← already directory ✅
│   └── SKILL.md
└── scripts/                  ← global skill scripts (skill_creator_cli.py, etc.)
    ├── skill_creator_cli.py
    └── tdd_gatekeeper_runner.py
```

> [!IMPORTANT]
> The `scripts/` folder at `.harness/skills/scripts/` is a **global** scripts folder for harness-level automation (not per-skill). It stays as-is. Each individual skill can optionally have its own `assets/` folder for skill-specific scripts.

---

## Proposed Changes

### 1 — Skill file migration
#### [MODIFY] `.harness/skills/` (14 flat `.md` files → directories)

Each flat `<name>.md` becomes `<kebab-name>/SKILL.md`:

| Current file | New directory |
|---|---|
| `tdd_gatekeeper.md` | `tdd-gatekeeper/SKILL.md` |
| `state_management.md` | `state-management/SKILL.md` |
| `python_clean_architecture.md` | `python-clean-architecture/SKILL.md` |
| `python_performance_optimization.md` | `python-performance-optimization/SKILL.md` |
| `python_testing.md` | `python-testing-and-quality-profile-specific/SKILL.md` |
| `git_management.md` | `git-management/SKILL.md` |
| `javascript_quality.md` | `javascript-quality/SKILL.md` |
| `async_state_management.md` | `async-state-management/SKILL.md` |
| `typescript_strict_safety.md` | `typescript-strict-safety/SKILL.md` |
| `c_memory_analyzer.md` | `c-memory-analyzer/SKILL.md` |
| `compilation_and_analysis.md` | `compilation-and-analysis/SKILL.md` |
| `autosar_architecture.md` | `autosar-architecture/SKILL.md` |
| `embedded_deep_reasoning.md` | `embedded-deep-reasoning/SKILL.md` |
| `trace32_cmm_scripting.md` | `trace32-cmm-scripting/SKILL.md` |

The file **content is preserved exactly** — only the path changes.

---

### 2 — Transpiler refactor
#### [MODIFY] [transpiler_core.py](file:///Users/hazaeltrejo/Documents/harness_template/.harness/adaptation/scripts/transpiler_core.py)

**`compile_skills()` method changes:**

- **Remove** the "Caso 2: Archivo .md individual" branch (lines 207–221) — flat `.md` files will no longer exist.
- **Update `profile_skill_map`** to use directory names (kebab-case) instead of filenames with `.md` extension:

```python
profile_skill_map = {
    "python": [
        "python-testing-and-quality-profile-specific",
        "python-clean-architecture",
        "python-performance-optimization",
        "state-management",
    ],
    "embedded-c": [
        "c-memory-analyzer",
        "compilation-and-analysis",
        "autosar-architecture",
        "embedded-deep-reasoning",
        "trace32-cmm-scripting",
    ],
    "javascript": [
        "javascript-quality",
        "async-state-management",
        "typescript-strict-safety",
    ],
    "core": [
        "tdd-gatekeeper",
        "skill-creator",
        "file-translator",
        "git-management",
    ]
}
```

- **Simplify the `allowed_skills` filter** — since all entries are now directory names, the dual-check (`isdir and in allowed_skills`) simplifies to a single `filename not in allowed_skills`.
- **Skip `scripts/` explicitly** — add a guard to skip the `scripts/` subdirectory during skill iteration.

---

### 3 — skill_creator_cli.py
#### [MODIFY] [skill_creator_cli.py](file:///Users/hazaeltrejo/Documents/harness_template/.harness/skills/scripts/skill_creator_cli.py)

Small cosmetic fix: the CLI already creates directories correctly. Only change needed:
- Update the `assets/` folder creation to be **conditional** (only if user passes `--with-assets` flag). Currently it always creates an empty `assets/` folder.
- Update the template in `SKILL.md` generation to match the English template style used by `skill-creator` and `file-translator`.

---

### 4 — Documentation updates
#### [MODIFY] [AGENTS.md](file:///Users/hazaeltrejo/Documents/harness_template/AGENTS.md)

- Update the **Available Skills** list to use the new directory-based names.
- Update the CLI commands section — the `skill_creator_cli.py` invocation path stays the same.

#### [MODIFY] [ARCHITECTURE.md](file:///Users/hazaeltrejo/Documents/harness_template/ARCHITECTURE.md)

- Update the `.harness/skills/` directory tree diagram to show the directory-based structure.
- Add a note clarifying that `scripts/` inside a skill folder is the per-skill scripts location.

#### [MODIFY] [README.md](file:///Users/hazaeltrejo/Documents/harness_template/README.md) (root)

- Update the skills section if it mentions flat file structure.

#### [MODIFY] [.harness/README.md](file:///Users/hazaeltrejo/Documents/harness_template/.harness/README.md)

- Update the `skills/` section description and tree diagram to reflect the unified directory format.
- Document the optional `assets/` and `scripts/` subfolders per skill.

---

## Open Questions

> [!IMPORTANT]
> **`git-management` profile assignment**: Currently `git_management.md` is not in any profile's skill list (it exists on disk but is filtered out). Should it be added to `core` (available always) or left as a standalone skill that is always compiled regardless of profile?

> [!NOTE]
> **`scripts/` per skill**: Should individual skill directories support a `scripts/` subfolder (in addition to `assets/`) for per-skill scripts? This is what the user referenced in the request. If yes, the transpiler's `_copy_skill_assets` method needs to also copy `scripts/` subdirectories from within a skill folder.

---

## Verification Plan

### Automated
```bash
# After migration, recompile and verify all skills appear
python3 adapt_harness.py opencode

# Confirm 14+ skills compiled (0 "Skill transpilada" without "(dir)")
grep "Skill transpilada" <output>   # all lines should say "(dir)"
```

### Manual
- Confirm no flat `.md` files remain in `.harness/skills/` (only directories + `scripts/`).
- Confirm `.opencode/skills/` matches expected output.
- Confirm `AGENTS.md` skill list is complete and correct.
