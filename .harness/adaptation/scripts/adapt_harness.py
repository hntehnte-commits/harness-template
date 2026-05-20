#!/usr/bin/env python3
import os
import sys
import subprocess

# Rutas del entorno virtual y script principal
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # .harness/adaptation/scripts
ADAPTATION_DIR = os.path.dirname(BASE_DIR)            # .harness/adaptation
VENV_DIR = os.path.join(ADAPTATION_DIR, ".venv")

if os.name == "nt":
    VENV_PYTHON = os.path.join(VENV_DIR, "Scripts", "python.exe")
else:
    VENV_PYTHON = os.path.join(VENV_DIR, "bin", "python")

MAIN_SCRIPT = os.path.join(BASE_DIR, "main.py")
REQUIREMENTS_FILE = os.path.join(ADAPTATION_DIR, "requirements.txt")

def setup_venv():
    """Crea el entorno virtual e instala los requerimientos si no existen"""
    if not os.path.exists(VENV_DIR):
        print("🌱 Creando entorno virtual bajo .harness/adaptation/.venv/...")
        try:
            import venv
            venv.create(VENV_DIR, with_pip=True)
            print("✅ Entorno virtual creado exitosamente.")
            
            # Instalar dependencias si requirements.txt tiene contenido válido
            if os.path.exists(REQUIREMENTS_FILE):
                with open(REQUIREMENTS_FILE, "r", encoding="utf-8") as f:
                    req_content = f.read().strip()
                # Filtrar comentarios y líneas vacías
                has_deps = any(line.strip() and not line.strip().startswith("#") for line in req_content.split("\n"))
                
                if has_deps:
                    print("📦 Instalando dependencias de requirements.txt...")
                    subprocess.check_call([VENV_PYTHON, "-m", "pip", "install", "-q", "-r", REQUIREMENTS_FILE])
                    print("✅ Dependencias instaladas exitosamente.")
        except Exception as e:
            print(f"❌ Error al inicializar el entorno virtual: {e}")
            sys.exit(1)

def is_running_in_venv():
    """Detecta si el proceso actual se está ejecutando dentro de un entorno virtual"""
    return (sys.prefix != sys.base_prefix) or ("VIRTUAL_ENV" in os.environ)

def main():
    # Asegurar la existencia y configuración del venv
    setup_venv()
    
    # Si ya estamos corriendo dentro de un venv o no pudimos hallar el script principal,
    # ejecutamos directamente importando o salimos con error
    if is_running_in_venv():
        # Ejecutar importando el script main si estamos en el venv correcto
        sys.path.insert(0, ADAPTATION_DIR)
        sys.path.insert(0, BASE_DIR)
        from scripts.main import main as run_main
        run_main()
    else:
        # Re-ejecutar el script usando el Python del venv de forma transparente
        if not os.path.exists(MAIN_SCRIPT):
            print(f"❌ Error: No se encontró el script principal en {MAIN_SCRIPT}")
            sys.exit(1)
            
        cmd = [VENV_PYTHON, MAIN_SCRIPT] + sys.argv[1:]
        try:
            res = subprocess.run(cmd)
            sys.exit(res.returncode)
        except KeyboardInterrupt:
            # Capturar Ctrl+C elegantemente sin lanzar traza de error
            print("\n👋 Ejecución cancelada por el usuario.")
            sys.exit(130)

if __name__ == "__main__":
    main()
