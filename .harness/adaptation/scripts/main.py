# main.py
import sys
import os
import argparse

from compiler import adapt_to_tool
from sync import sync_manifest
from menu import run_interactive_menu

def main():
    # Si se ejecuta sin argumentos, activar modo menú interactivo
    if len(sys.argv) == 1:
        run_interactive_menu()
        sys.exit(0)

    parser = argparse.ArgumentParser(description="Adapta el Harness a una herramienta de IA específica.")
    parser.add_argument("command", choices=["claude", "cursor", "opencode", "compile", "sync"], help="El comando a ejecutar")
    args = parser.parse_args()

    if args.command == "sync":
        sync_manifest()
    elif args.command in ["opencode", "compile"]:
        adapt_to_tool("opencode")
    else:
        adapt_to_tool(args.command)

if __name__ == "__main__":
    main()
