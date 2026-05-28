# main.py
"""
main.py - Punto de entrada del Harness Adapter
Orquesta la compilación, adaptación y sincronización
"""
import sys
import os
import argparse

from compiler import compile_for_opencode, adapt_to_tool
from sync import sync_manifest
from menu import run_interactive_menu


def main():
    """Punto de entrada principal"""
    # Si se ejecuta sin argumentos, activar modo menú interactivo
    if len(sys.argv) == 1:
        run_interactive_menu()
        sys.exit(0)

    parser = argparse.ArgumentParser(
        description="Adaptador del Multi-Agent Harness a herramientas de IA.",
        epilog="Ejemplos: python main.py sync | python main.py opencode | python main.py claude"
    )
    parser.add_argument(
        "command",
        choices=["claude", "cursor", "opencode", "compile", "sync"],
        help="Comando a ejecutar"
    )
    args = parser.parse_args()

    try:
        if args.command == "sync":
            sync_manifest()
        elif args.command in ["opencode", "compile"]:
            compile_for_opencode()
        elif args.command in ["claude", "cursor"]:
            adapt_to_tool(args.command)
        else:
            print(f"[ERR] Comando desconocido: {args.command}")
            sys.exit(1)
        
        print("\n[OK] Operación completada exitosamente.")
        
    except KeyboardInterrupt:
        print("\n\n👋 Ejecución cancelada por el usuario.")
        sys.exit(130)
    except Exception as e:
        print(f"\n[ERR] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

