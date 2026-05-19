---
name: state-management
description: To safely interact with the State Machine artifacts without corrupting them.
---
# Skill: State Management

## Purpose
To safely interact with the State Machine artifacts without corrupting them.

## Execution Steps
1. When generating a YAML artifact, always use the exact schema defined in `/.harness/artifacts/templates/`.
2. Do not include markdown codeblocks (```yaml) in the saved file; save pure, valid YAML.
3. Save the artifact in `/.harness/artifacts/current_run/` with the exact naming convention:
   - `01_proposal.yaml`
   - `02_specification.yaml`
   - `03_design.yaml`
   - `04_implementation.yaml`
   - `05_verification.yaml`
