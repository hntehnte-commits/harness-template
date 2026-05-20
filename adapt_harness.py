#!/usr/bin/env python3
import os
import sys
import subprocess

# Ruta hacia el script real en la carpeta de adaptación
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REAL_SCRIPT = os.path.join(BASE_DIR, ".harness", "adaptation", "scripts", "adapt_harness.py")

def main():
    if not os.path.exists(REAL_SCRIPT):
        print(f"❌ Error: No se encontró el script real en {REAL_SCRIPT}")
        sys.exit(1)
        
    cmd = [sys.executable, REAL_SCRIPT] + sys.argv[1:]
    try:
        res = subprocess.run(cmd)
        sys.exit(res.returncode)
    except KeyboardInterrupt:
        print("\n👋 Ejecución cancelada por el usuario.")
        sys.exit(130)

if __name__ == "__main__":
    main()
