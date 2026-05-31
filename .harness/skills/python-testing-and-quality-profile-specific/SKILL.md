# Skill: Python Testing and Quality (Profile Specific)

## Purpose
Ensure Python source code and test suites meet clean coding guidelines (PEP 8) and assert correct behaviors using pytest and mock structures.

---

## 1. Quality & Style Audit (PEP 8)
- Verify compliance with PEP 8 spacing, imports, and variables.
- Run `flake8` to identify unused imports, undefined variables, and spacing issues.
- Ensure all public functions and classes have descriptive docstrings and type hints.

---

## 2. pytest & Mocking Protocol
1. **Use pytest Fixtures**: Isolate heavy database setups, external integrations, or file writes using pytest fixtures.
2. **Mocking External APIs**: Use `unittest.mock` (or `pytest-mock` if available) to patch external calls:
   ```python
   from unittest.mock import patch
   with patch('module.external_call') as mock_call:
       mock_call.return_value = "mocked_data"
       # execute test assertions
   ```
3. **Exception Testing**: Ensure code handles errors gracefully and tests verify raised exceptions:
   ```python
   import pytest
   with pytest.raises(ValueError):
       invalid_function_call()
   ```
