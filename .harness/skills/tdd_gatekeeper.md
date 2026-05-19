# Skill: Strict TDD Gatekeeper

## Purpose
To ensure code is written only to satisfy a failing test.

## Execution Steps
1. **Understand Contract**: Read the `03_design.yaml` to know what to test.
2. **Write Test (Red Phase)**: Write a unit test that verifies the contract.
3. **Execute Test**: Run the test command in the terminal (check config.yaml for the command).
   - If the test passes, YOU FAILED. A valid test for unwritten code must fail. Delete the test and write a proper one.
   - If the test fails, YOU PASSED the Red Phase. Proceed to step 4.
4. **Write Code (Green Phase)**: Write the minimal application code to make the test pass.
5. **Execute Test**: Run the test command in the terminal.
   - If the test fails, fix the code until it passes. Do not proceed to the next feature.
   - If the test passes, YOU PASSED the Green Phase.
6. **Refactor**: Clean up the code, run tests again to ensure they stay green.
