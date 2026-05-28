# compiler.py
"""
compiler.py - Compilador principal del Harness
Adaptado para usar módulos descompuestos (transpiler_core, registry_builder)
"""
import os
import shutil
import sys

from constants import POINTER_TEXT, POINTER_TEXT_OPENCODE
from transpiler_core import TranspilerCore
from registry_builder import RegistryBuilder


def compile_for_opencode():
    """Compila todo el arnés a estructura nativa de OpenCode"""
    transpiler = TranspilerCore()
    transpiler.compile_all(POINTER_TEXT_OPENCODE)
    
    # Sincronizar AGENTS.md automáticamente
    registry = RegistryBuilder()
    registry.sync_agents_md(use_opencode=True)

def adapt_to_tool(tool_name):
    """Adapta el arnés de entrada a un formato específico de herramienta (Claude/Cursor/OpenCode)"""
    print(f"🧹 Limpiando adaptadores anteriores...")
    for f in [".clinerules", ".cursorrules"]:
        if os.path.exists(f): os.remove(f)
    if os.path.exists(".opencode"):
        shutil.rmtree(".opencode", ignore_errors=True)

    if tool_name in ["claude", "roo", "cline"]:
        sync_manifest(use_opencode=False)
        with open(".clinerules", "w", encoding="utf-8") as f:
            f.write(POINTER_TEXT)
        print("✅ Arnés adaptado para Claude Code / Roo Code (Se generó .clinerules)")
        
    elif tool_name == "cursor":
        sync_manifest(use_opencode=False)
        with open(".cursorrules", "w", encoding="utf-8") as f:
            f.write(POINTER_TEXT)
        print("✅ Arnés adaptado para Cursor (Se generó .cursorrules)")
        
    elif tool_name == "opencode":
        compile_for_opencode()
        sync_manifest(use_opencode=True)
        print("✅ Arnés transpilado exitosamente a la estructura nativa de OpenCode.")
        
    else:
        print(f"❌ Herramienta desconocida: {tool_name}")
        sys.exit(1)
