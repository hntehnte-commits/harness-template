# compiler.py
"""
compiler.py - Compilador principal del Harness
Adaptado para usar módulos descompuestos (transpiler_core, registry_builder)
Incluye soporte para compilación con perfiles dinámicos (Sprint 2)
"""
import os
import shutil
import sys

from constants import POINTER_TEXT, POINTER_TEXT_OPENCODE
from transpiler_core import TranspilerCore
from registry_builder import RegistryBuilder
from lazy_loader import ProfileAwareLoader


def load_profiles_config(config_file=".harness/profiles_enabled.yaml"):
    """Carga la configuración de perfiles activos"""
    if not os.path.exists(config_file):
        print("[!] Archivo de configuración de perfiles no encontrado")
        return ["core", "python"]  # Por defecto
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            # Parse YAML simple (sin dependencias)
            content = f.read()
            
            # Extraer perfiles habilitados
            enabled = []
            for line in content.split('\n'):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                # Búsqueda simple en la sección 'enabled'
                if '- ' in line and 'enabled' not in line:
                    profile = line.replace('- ', '', 1).strip()
                    # Eliminar comentarios inline
                    if '#' in profile:
                        profile = profile[:profile.index('#')].strip()
                    if profile:
                        enabled.append(profile)
            
            return enabled if enabled else ["core", "python"]
    except Exception as e:
        print(f"[!] Error cargando perfiles: {e}")
        return ["core", "python"]


def compile_for_opencode(profile_aware=True):
    """
    Compila todo el arnés a estructura nativa de OpenCode.
    
    Args:
        profile_aware: Si True, solo compila skills de perfiles activos (Sprint 2)
    """
    print("[*] Compilando Arnés a formato nativo de OpenCode...")
    
    if profile_aware:
        active_profiles = load_profiles_config()
        print(f"   [*] Perfiles activos: {', '.join(active_profiles)}\n")
    else:
        active_profiles = None
    
    transpiler = TranspilerCore(profile_aware=profile_aware, active_profiles=active_profiles)
    transpiler.compile_all(POINTER_TEXT_OPENCODE)
    
    # Sincronizar AGENTS.md automáticamente
    registry = RegistryBuilder()
    registry.sync_agents_md(use_opencode=True)
    
    # Imprimir análisis de perfiles si está habilitado
    if profile_aware and active_profiles:
        print_profile_footprint(active_profiles)


def print_profile_footprint(active_profiles):
    """Analiza e imprime el footprint de memoria de los perfiles activos"""
    loader = ProfileAwareLoader(active_profiles=active_profiles)
    analysis = loader.analyze_profile_footprint()

    print("\n[INFO] ANÁLISIS DE FOOTPRINT POR PERFIL")
    for profile, data in analysis.items():
        print(f"   {profile}: {data['skill_count']} skills, {data['total_size_kb']} KB")
    print(f"   Total perfiles activos: {len(active_profiles)}\n")


def sync_manifest(use_opencode=True):
    """Sincroniza AGENTS.md usando RegistryBuilder"""
    registry = RegistryBuilder()
    registry.sync_agents_md(use_opencode=use_opencode)


def adapt_to_tool(tool_name):
    """Adapta el arnés de entrada a un formato específico de herramienta (Claude/Cursor/OpenCode)"""
    print("[*] Limpiando adaptadores anteriores...")
    for f in [".clinerules", ".cursorrules"]:
        if os.path.exists(f): os.remove(f)
    if os.path.exists(".opencode"):
        shutil.rmtree(".opencode", ignore_errors=True)

    if tool_name in ["claude", "roo", "cline"]:
        sync_manifest(use_opencode=False)
        with open(".clinerules", "w", encoding="utf-8") as f:
            f.write(POINTER_TEXT)
        print("[OK] Arnés adaptado para Claude Code / Roo Code (Se generó .clinerules)")
        
    elif tool_name == "cursor":
        sync_manifest(use_opencode=False)
        with open(".cursorrules", "w", encoding="utf-8") as f:
            f.write(POINTER_TEXT)
        print("[OK] Arnés adaptado para Cursor (Se generó .cursorrules)")
        
    elif tool_name == "opencode":
        compile_for_opencode()
        sync_manifest(use_opencode=True)
        print("[OK] Arnés transpilado exitosamente a la estructura nativa de OpenCode.")
        
    else:
        print(f"[ERR] Herramienta desconocida: {tool_name}")
        sys.exit(1)
