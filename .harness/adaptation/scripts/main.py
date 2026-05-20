# main.py
import sys
import os
import argparse

from compiler import adapt_to_tool, compile_profile_overlay, remove_profile_overlay
from sync import sync_manifest
from menu import run_interactive_menu

def main():
    # Si se ejecuta sin argumentos, activar modo menú interactivo
    if len(sys.argv) == 1:
        run_interactive_menu()
        sys.exit(0)

    parser = argparse.ArgumentParser(description="Adapta el Harness a una herramienta de IA específica o gestiona perfiles.")
    parser.add_argument("command", choices=["claude", "cursor", "opencode", "compile", "sync", "install", "remove"], help="El comando a ejecutar")
    parser.add_argument("profile", nargs="?", default=None, help="El perfil a aplicar, instalar o remover")
    args = parser.parse_args()
    
    # Validar perfil si se requiere
    if args.command in ["install", "remove"] and not args.profile:
        print(f"❌ Error: El comando '{args.command}' requiere especificar un perfil.")
        print("Uso: python3 adapt_harness.py install <profile_name>")
        sys.exit(1)
        
    if args.profile:
        # Validar si el perfil existe en .harness/profiles/
        profile_path = os.path.join(".harness/profiles", args.profile)
        if not os.path.exists(profile_path) and args.command != "remove":
            print(f"❌ Error: El perfil '{args.profile}' no existe en .harness/profiles/")
            sys.exit(1)

    if args.command == "sync":
        sync_manifest()
    elif args.command == "install":
        # Asegurar que la estructura básica de .opencode exista
        os.makedirs(".opencode/agents", exist_ok=True)
        os.makedirs(".opencode/skills", exist_ok=True)
        os.makedirs(".opencode/memory", exist_ok=True)
        os.makedirs(".opencode/artifacts/templates", exist_ok=True)
        os.makedirs(".opencode/profiles", exist_ok=True)
        
        compile_profile_overlay(args.profile, is_default=False)
        sync_manifest(use_opencode=True)
        print(f"✅ Perfil '{args.profile}' instalado y AGENTS.md sincronizado.")
    elif args.command == "remove":
        remove_profile_overlay(args.profile)
        sync_manifest(use_opencode=True)
        print(f"✅ Perfil '{args.profile}' removido y AGENTS.md sincronizado.")
    elif args.command in ["opencode", "compile"]:
        adapt_to_tool("opencode", args.profile)
    else:
        adapt_to_tool(args.command, args.profile)

if __name__ == "__main__":
    main()
