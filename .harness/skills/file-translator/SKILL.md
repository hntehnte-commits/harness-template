# Skill: File Translator

## Purpose
Translate any file provided by the user to the language they specify, while **strictly preserving** the original file's structure, formatting, and content — only the human-readable text is translated.

---

## 1. Inputs Required

Before starting, confirm with the user:

| Input | Description | Example |
|---|---|---|
| `input_file` | Path to the file to translate | `docs/README.md` |
| `target_language` | The language to translate to | `Spanish`, `French`, `German` |
| `output_file` *(optional)* | Where to save the result. If omitted, save next to the original with the language appended to the filename | `docs/README.es.md` |

---

## 2. Execution Procedure

### Step 1 – Read and analyze the file
- Open the file and identify its format (Markdown, plain text, YAML, JSON, code, etc.).
- Identify which parts are **translatable** (human-readable prose) and which are **protected** (must not be changed).

### Step 2 – Identify protected content (DO NOT translate these)
The following must be left **bit-identical** to the original:
- Code blocks (fenced ` ``` ` or `~~~`, and inline backtick code)
- Shell commands and CLI flags
- Variable names, function names, class names
- URLs and file paths inside markdown links — only the link text may be translated
- YAML / TOML / JSON **keys** (only values that are human-readable prose may be translated)
- Front-matter blocks (`---` delimiters and their keys)
- Indentation, blank lines, bullet symbols, heading markers (`#`, `##`, etc.)
- Any content inside `<tags>` that is a technical identifier

### Step 3 – Translate
- Translate **only** the prose portions identified in Step 2.
- Maintain the exact same sentence structure and paragraph breaks where possible.
- Do not add, remove, or reorder sections.
- Do not add translator notes or commentary.

### Step 4 – Reconstruct the file
- Reassemble the file keeping every protected span identical to the original.
- The output file must have the exact same number of sections, headings, and code blocks as the input.

### Step 5 – Save and report
- Write the translated content to `output_file` (or the auto-generated name).
- Tell the user:
  1. The path of the output file.
  2. Which sections (if any) were intentionally left untranslated and why.

---

## 3. Validation Rules

Before delivering the output, verify:
- ✅ All headings, bullet points, and code fences are present and in the same order.
- ✅ Code blocks are identical to the originals (character-by-character).
- ✅ URLs inside markdown links are unchanged.
- ✅ No new sections, footnotes, or comments were added.
- ✅ The file encoding is UTF-8.

If any of these checks fail, correct the output before delivering it to the user.

---

## 4. Auto-Correction
- If you notice you accidentally translated a code block or a URL, revert that specific span to the original and re-deliver the file.
- If the target language is ambiguous (e.g., "Chinese" → Simplified or Traditional?), ask the user before proceeding.
