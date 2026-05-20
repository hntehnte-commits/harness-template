# menu.py
import os
import sys
from compiler import adapt_to_tool, compile_profile_overlay, remove_profile_overlay
from sync import sync_manifest

def get_available_profiles():
    """Escanea y obtiene dinámicamente los perfiles disponibles en .harness/profiles"""
    profiles_dir = ".harness/profiles"
    if not os.path.exists(profiles_dir):
        return []
    return [d for d in os.listdir(profiles_dir) if os.path.isdir(os.path.join(profiles_dir, d))]

def select_profile(required=True):
    """Pide al usuario seleccionar un perfil de forma interactiva"""
    profiles = get_available_profiles()
    if not profiles:
        print("⚠️ No se encontraron perfiles disponibles en .harness/profiles/.")
        if required:
            print("❌ Operación cancelada: Esta acción requiere de al menos un perfil.")
            return None
        return None

    print("\n--- Perfiles Disponibles ---")
    for i, profile in enumerate(profiles, start=1):
        print(f"  {i}. {profile}")
    
    if not required:
        print(f"  {len(profiles) + 1}. Ninguno / Solo Core")

    while True:
        try:
            choice = input(f"\nSelecciona un perfil [1-{len(profiles) if required else len(profiles) + 1}]: ").strip()
            if not choice:
                continue
            idx = int(choice) - 1
            if 0 <= idx < len(profiles):
                return profiles[idx]
            elif not required and idx == len(profiles):
                return None
            print("❌ Opción inválida. Intenta de nuevo.")
        except ValueError:
            print("❌ Entrada no válida. Debe ser un número.")

def run_interactive_menu():
    """Ejecuta el menú interactivo principal en la terminal"""
    print("\n" + "="*58)
    print("🛡️  Harness Adaptation & Profile Manager - Interactive Menu")
    print("="*58)
    print("  1. ⚙️  Compilar/Transpilar Arnés a formato OpenCode (opencode)")
    print("  2. 📥  Instalar / Actualizar un Perfil en .opencode/ (install)")
    print("  3. 🧹  Remover un Perfil de .opencode/ (remove)")
    print("  4. 🤖  Adaptar Arnés para Claude Code / Roo Code (claude)")
    print("  5. 💻  Adaptar Arnés para Cursor (cursor)")
    print("  6. 🔄  Sincronizar catálogo AGENTS.md (sync)")
    print("  7. ❌  Salir")
    print("="*58)

    while True:
        choice = input("\nSelecciona una opción [1-7]: ").strip()
        if choice in ["1", "2", "3", "4", "5", "6", "7"]:
            break
        print("❌ Opción inválida. Elige un número del 1 al 7.")

    if choice == "7":
        print("👋 ¡Hasta luego!")
        sys.exit(0)

    if choice == "1":
        # Opencode (compile) - perfil opcional
        profile = select_profile(required=False)
        print(f"\n🚀 Iniciando transpilación para OpenCode (Perfil: {profile or 'Ninguno'})...\n")
        adapt_to_tool("opencode", profile)
        
    elif choice == "2":
        # Install profile - perfil requerido
        profile = select_profile(required=True)
        if profile:
            print(f"\n🚀 Instalando perfil '{profile}' under .opencode/...\n")
            # Asegurar que los directorios base existen
            os.makedirs(".opencode/agents", exist_ok=True)
            os.makedirs(".opencode/skills", exist_ok=True)
            os.makedirs(".opencode/memory", exist_ok=True)
            os.makedirs(".opencode/artifacts/templates", exist_ok=True)
            os.makedirs(".opencode/profiles", exist_ok=True)
            
            compile_profile_overlay(profile, is_default=False)
            sync_manifest(use_opencode=True)
            print(f"✅ Perfil '{profile}' instalado exitosamente y AGENTS.md sincronizado.")
            
    elif choice == "3":
        # Remove profile - perfil requerido
        profile = select_profile(required=True)
        if profile:
            print(f"\n🚀 Removiendo perfil '{profile}' de .opencode/...\n")
            remove_profile_overlay(profile)
            sync_manifest(use_opencode=True)
            print(f"✅ Perfil '{profile}' removido y AGENTS.md sincronizado.")
            
    elif choice == "4":
        # Claude - perfil opcional
        profile = select_profile(required=False)
        print(f"\n🚀 Adaptando arnés para Claude Code (Perfil: {profile or 'Ninguno'})...\n")
        adapt_to_tool("claude", profile)
        
    elif choice == "5":
        # Cursor - perfil opcional
        profile = select_profile(required=False)
        print(f"\n🚀 Adaptando arnés para Cursor (Perfil: {profile or 'Ninguno'})...\n")
        adapt_to_tool("cursor", profile)
        
    elif choice == "6":
        # Sync
        print("\n🚀 Sincronizando catálogo AGENTS.md...\n")
        sync_manifest()
