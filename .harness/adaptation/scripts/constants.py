# constants.py
"""
constants.py - Constantes globales del Harness
Incluye textos de instrucciones y tabla de reemplazos
"""

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

# NOTA: REPLACEMENTS ahora está en path_translator.py para centralización
# Esta línea se mantiene para compatibilidad hacia atrás
from path_translator import REPLACEMENTS

__all__ = ['POINTER_TEXT', 'POINTER_TEXT_OPENCODE', 'REPLACEMENTS']

