# menu.py
import os
import sys
from compiler import adapt_to_tool
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
            print(f"\n{C_BOLD}Gestión y Sincronización:{C_RESET}")
            print(f"  {C_CYAN}4.{C_RESET} 🔄   Sincronizar catálogo maestro AGENTS.md")
            print(f"  {C_CYAN}5.{C_RESET} ❌   {C_RED}Salir{C_RESET}")
            print(f"{C_CYAN}{'='*50}{C_RESET}")

            choice = input(f"\n{C_BOLD}Selecciona una opción [1-5]:{C_RESET} ").strip()
            if choice in ["1", "2", "3", "4", "5"]:
                break
            input(f"{C_RED}❌ Opción inválida. Presiona Enter para intentar de nuevo...{C_RESET}")

        if choice == "5":
            print(f"\n{C_GREEN}👋 ¡Hasta luego! ¡Buena suerte con tu desarrollo!{C_RESET}\n")
            sys.exit(0)

        if choice == "1":
            print(f"\n🚀 {C_CYAN}Iniciando transpilación nativa para OpenCode...{C_RESET}\n")
            adapt_to_tool("opencode")
            
        elif choice == "2":
            print(f"\n🚀 {C_CYAN}Adaptando arnés para Claude/Roo Code...{C_RESET}\n")
            adapt_to_tool("claude")
            
        elif choice == "3":
            print(f"\n🚀 {C_CYAN}Adaptando arnés para Cursor...{C_RESET}\n")
            adapt_to_tool("cursor")
            
        elif choice == "4":
            print(f"\n🚀 {C_CYAN}Sincronizando manifiesto maestro AGENTS.md con el estado actual...{C_RESET}\n")
            sync_manifest()
            print(f"\n{C_GREEN}✅ Manifiesto AGENTS.md sincronizado correctamente.{C_RESET}")

        print(f"\n{C_CYAN}{'='*50}{C_RESET}")
        input(f"{C_BOLD}Presiona Enter para finalizar y volver a tu terminal...{C_RESET}")

    except KeyboardInterrupt:
        print(f"\n\n{C_YELLOW}👋 Ejecución cancelada por el usuario. ¡Hasta luego!{C_RESET}\n")
        sys.exit(0)
