# Skill: JavaScript Quality (Profile Specific)

## Purpose
Ensure JavaScript modern packages and source scripts maintain robust error boundaries, comply with ESLint formatting rules, and utilize modern asynchronous execution standards.

---

## 1. Asynchrony Audit (async/await)
- Verify that asynchronous tasks utilize the `async/await` syntax instead of deep nested callbacks or raw `.then()` chaining.
- Ensure all asynchronous calls are wrapped in robust `try/catch` error handlers to prevent unhandled promise rejections.

---

## 2. ES Module Verification
- Validate use of modern `import` / `export` syntax instead of standard CommonJS `require()` / `module.exports`.
- Ensure paths for imports contain correct file extensions if running in pure node/ES environments.

---

## 3. ESLint Compliance
- Execute lint commands as configured in `config.yaml` to detect undefined variables or syntax errors.
- Ensure that no debug methods (e.g. `console.log`) are left in production-ready files (use proper log interfaces if needed).
