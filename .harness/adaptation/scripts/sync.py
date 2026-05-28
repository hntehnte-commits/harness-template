# sync.py
"""
sync.py - Sincronización de AGENTS.md
Adaptado para usar registry_builder
"""
import os
from registry_builder import RegistryBuilder


def sync_manifest(use_opencode=None):
    """Sincroniza el manifiesto central AGENTS.md con los agentes y habilidades reales"""
    if use_opencode is None:
        use_opencode = os.path.exists(".opencode")
    
    mode = "OpenCode (.opencode/)" if use_opencode else "Harness (.harness/)"
    print(f"🔄 Sincronizando AGENTS.md con roles y skills disponibles en {mode}...\n")
    
    registry = RegistryBuilder()
    success = registry.sync_agents_md(use_opencode=use_opencode)
    
    if success:
        print(f"\n✅ AGENTS.md sincronizado correctamente.")
    else:
        print(f"\n❌ Error al sincronizar AGENTS.md")

