# menu.py
import os
import sys
from compiler import adapt_to_tool, compile_profile_overlay, remove_profile_overlay, apply_profile_to_harness
from sync import sync_manifest

# Códigos de color ANSI para una interfaz premium
C_CYAN = "\033[1;36m"
C_GREEN = "\033[1;32m"
C_YELLOW = "\033[1;33m"
C_RED = "\033[1;31m"
C_BOLD = "\033[1m"
C_RESET = "\033[0m"

def print_banner():
    """Imprime un banner premium en la consola"""
    print(f"{C_CYAN}{C_BOLD}")
    print("  _  _                                   ")
    print(" | || |__ _  _ _  _ _  ___ ___ ___       ")
    print(" | __ / _` || '_|| ' \\/ -_(_-<(_-<       ")
    print(" |_||_\\__,_||_|  |_||_\\___/__//__/       ")
    print(f"  🛡️  Adaptador y Administrador del Arnés{C_RESET}\n")

def get_available_profiles():
    """Escanea y obtiene dinámicamente los perfiles disponibles en .harness/profiles"""
    profiles_dir = ".harness/profiles"
    if not os.path.exists(profiles_dir):
        return []
    return sorted([d for d in os.listdir(profiles_dir) if os.path.isdir(os.path.join(profiles_dir, d))])

def select_profile(required=True):
    """Pide al usuario seleccionar un perfil de forma interactiva"""
    profiles = get_available_profiles()
    if not profiles:
        print(f"\n{C_YELLOW}⚠️  No se encontraron perfiles en .harness/profiles/.{C_RESET}")
        if required:
            print(f"{C_RED}❌ Operación cancelada: Esta acción requiere al menos un perfil.{C_RESET}")
            return None
        return None

    print(f"\n{C_BOLD}--- Perfiles de Stack Disponibles ---{C_RESET}")
    for i, profile in enumerate(profiles, start=1):
        print(f"  {C_CYAN}{i}.{C_RESET} {profile}")
    
    if not required:
        print(f"  {C_CYAN}{len(profiles) + 1}.{C_RESET} Ninguno / Solo Core (Arnés base)")

    max_val = len(profiles) if required else len(profiles) + 1
    while True:
        try:
            choice = input(f"\nSelecciona un perfil [1-{max_val}]: ").strip()
            if not choice:
                continue
            idx = int(choice) - 1
            if 0 <= idx < len(profiles):
                return profiles[idx]
            elif not required and idx == len(profiles):
                return None
            print(f"{C_RED}❌ Opción inválida. Intenta de nuevo.{C_RESET}")
        except ValueError:
            print(f"{C_RED}❌ Entrada no válida. Debe ser un número.{C_RESET}")
        except (KeyboardInterrupt, EOFError):
            print(f"\n{C_YELLOW}👋 Selección cancelada por el usuario.{C_RESET}")
            return None

def run_interactive_menu():
    """Ejecuta el menú interactivo principal en la terminal"""
    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print_banner()
            print(f"{C_BOLD}¿Para qué herramienta de IA deseas adaptar tu arnés?{C_RESET}")
            print(f"  {C_CYAN}1.{C_RESET} ⚙️   {C_BOLD}OpenCode{C_RESET} (Compilar y transpilar a estructura nativa de .opencode/)")
            print(f"  {C_CYAN}2.{C_RESET} 🤖   {C_BOLD}Claude Code / Roo Code{C_RESET} (Generar directivas .clinerules)")
            print(f"  {C_CYAN}3.{C_RESET} 💻   {C_BOLD}Cursor{C_RESET} (Generar directivas .cursorrules)")
            print(f"\n{C_BOLD}Gestión de Perfiles y Manifiesto:{C_RESET}")
            print(f"  {C_CYAN}4.{C_RESET} 📥   Instalar / Aplicar perfil específico en tu arnés activo")
            print(f"  {C_CYAN}5.{C_RESET} 🧹   Remover / Desactivar perfil específico de tu arnés activo")
            print(f"  {C_CYAN}6.{C_RESET} 🔄   Sincronizar catálogo maestro AGENTS.md")
            print(f"  {C_CYAN}7.{C_RESET} ❌   {C_RED}Salir{C_RESET}")
            print(f"{C_CYAN}{'='*50}{C_RESET}")

            choice = input(f"\n{C_BOLD}Selecciona una opción [1-7]:{C_RESET} ").strip()
            if choice in ["1", "2", "3", "4", "5", "6", "7"]:
                break
            input(f"{C_RED}❌ Opción inválida. Presiona Enter para intentar de nuevo...{C_RESET}")

        if choice == "7":
            print(f"\n{C_GREEN}👋 ¡Hasta luego! ¡Buena suerte con tu desarrollo!{C_RESET}\n")
            sys.exit(0)

        if choice == "1":
            # OpenCode - compilar arnés con perfil opcional
            profile = select_profile(required=False)
            print(f"\n🚀 {C_CYAN}Iniciando transpilación nativa para OpenCode (Perfil: {profile or 'Solo Core'})...{C_RESET}\n")
            adapt_to_tool("opencode", profile)
            
        elif choice == "2":
            # Claude Code - perfil opcional
            profile = select_profile(required=False)
            print(f"\n🚀 {C_CYAN}Adaptando arnés para Claude/Roo Code (Perfil: {profile or 'Solo Core'})...{C_RESET}\n")
            adapt_to_tool("claude", profile)
            
        elif choice == "3":
            # Cursor - perfil opcional
            profile = select_profile(required=False)
            print(f"\n🚀 {C_CYAN}Adaptando arnés para Cursor (Perfil: {profile or 'Solo Core'})...{C_RESET}\n")
            adapt_to_tool("cursor", profile)
            
        elif choice == "4":
            # Instalar perfil overlay
            profile = select_profile(required=True)
            if profile:
                print(f"\n{C_BOLD}¿Para qué entorno/herramienta de IA deseas aplicar el perfil?{C_RESET}")
                print(f"  {C_CYAN}1.{C_RESET} OpenCode (Instalar en .opencode/)")
                print(f"  {C_CYAN}2.{C_RESET} Claude Code / Roo Code / Cursor (Aplicar en .harness/)")
                
                while True:
                    t_choice = input(f"\nSelecciona una opción [1-2]: ").strip()
                    if t_choice in ["1", "2"]:
                        break
                    print(f"{C_RED}❌ Opción inválida.{C_RESET}")
                
                if t_choice == "1":
                    print(f"\n🚀 {C_CYAN}Instalando perfil '{profile}' en .opencode/...{C_RESET}\n")
                    os.makedirs(".opencode/agents", exist_ok=True)
                    os.makedirs(".opencode/skills", exist_ok=True)
                    os.makedirs(".opencode/memory", exist_ok=True)
                    os.makedirs(".opencode/artifacts/templates", exist_ok=True)
                    os.makedirs(".opencode/profiles", exist_ok=True)
                    
                    compile_profile_overlay(profile, is_default=False)
                    sync_manifest(use_opencode=True)
                    print(f"\n{C_GREEN}✅ Perfil '{profile}' instalado exitosamente en .opencode/ y AGENTS.md sincronizado.{C_RESET}")
                else:
                    print(f"\n🚀 {C_CYAN}Aplicando perfil '{profile}' directamente en .harness/...{C_RESET}\n")
                    apply_profile_to_harness(profile)
                    sync_manifest(use_opencode=False)
                    print(f"\n{C_GREEN}✅ Perfil '{profile}' aplicado con éxito sobre la plantilla .harness/ y AGENTS.md sincronizado.{C_RESET}")
                
        elif choice == "5":
            # Remover perfil
            profile = select_profile(required=True)
            if profile:
                print(f"\n{C_BOLD}¿De qué entorno/herramienta de IA deseas remover o desactivar el perfil?{C_RESET}")
                print(f"  {C_CYAN}1.{C_RESET} OpenCode (Remover de .opencode/)")
                print(f"  {C_CYAN}2.{C_RESET} Claude Code / Roo Code / Cursor (Estructura de origen .harness/)")
                
                while True:
                    t_choice = input(f"\nSelecciona una opción [1-2]: ").strip()
                    if t_choice in ["1", "2"]:
                        break
                    print(f"{C_RED}❌ Opción inválida.{C_RESET}")
                
                if t_choice == "1":
                    print(f"\n🚀 {C_CYAN}Removiendo perfil '{profile}' de .opencode/...{C_RESET}\n")
                    remove_profile_overlay(profile)
                    sync_manifest(use_opencode=True)
                    print(f"\n{C_GREEN}✅ Perfil '{profile}' removido con éxito de .opencode/ y AGENTS.md sincronizado.{C_RESET}")
                else:
                    print(f"\n{C_YELLOW}ℹ️  Nota sobre el entorno .harness/:{C_RESET}")
                    print("Las modificaciones de perfil sobre .harness/ se aplican directamente sobre la plantilla de origen.")
                    print("Para revertir al estado core limpio, te recomendamos usar git:")
                    print(f"{C_CYAN}  git checkout .harness/{C_RESET}")
                    print("Esto restaurará todas las directivas base de forma segura.")
                
        elif choice == "6":
            # Sincronizar manifiesto
            print(f"\n🚀 {C_CYAN}Sincronizando manifiesto maestro AGENTS.md con el estado actual...{C_RESET}\n")
            sync_manifest()
            print(f"\n{C_GREEN}✅ Manifiesto AGENTS.md sincronizado correctamente.{C_RESET}")

        print(f"\n{C_CYAN}{'='*50}{C_RESET}")
        input(f"{C_BOLD}Presiona Enter para finalizar y volver a tu terminal...{C_RESET}")

    except KeyboardInterrupt:
        print(f"\n\n{C_YELLOW}👋 Ejecución cancelada por el usuario. ¡Hasta luego!{C_RESET}\n")
        sys.exit(0)
