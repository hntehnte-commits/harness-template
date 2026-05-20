# constants.py

POINTER_TEXT = """# SYSTEM HARNESS DIRECTIVE
You are operating within a strict multi-agent Harness system.
BEFORE doing anything else, you MUST read the file `AGENTS.md` to understand the project structure,
and then read `/.harness/roles/orchestrator.md` to begin the initialization process. 
Do not proceed with the user's task until you have assumed the Orchestrator role.
"""

POINTER_TEXT_OPENCODE = """# SYSTEM HARNESS DIRECTIVE
You are operating within a strict multi-agent Harness system.
BEFORE doing anything else, you MUST read the file `AGENTS.md` to understand the project structure,
and then read `/.opencode/agents/orchestrator.md` to begin the initialization process. 
Do not proceed with the user's task until you have assumed the Orchestrator role.
"""

REPLACEMENTS = {
    "/.harness/roles/orchestrator.md": "/.opencode/agents/orchestrator.md",
    "/.harness/roles/spec_agent.md": "/.opencode/agents/spec.md",
    "/.harness/roles/dev_agent.md": "/.opencode/agents/dev.md",
    "/.harness/roles/qa_agent.md": "/.opencode/agents/qa.md",
    "/.harness/skills/state_management.md": "/.opencode/skills/state-management/SKILL.md",
    "/.harness/skills/tdd_gatekeeper.md": "/.opencode/skills/strict-tdd-gatekeeper/SKILL.md",
    "/.harness/": "/.opencode/",
    ".harness/": ".opencode/"
}
