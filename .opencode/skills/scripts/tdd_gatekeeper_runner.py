# tdd_gatekeeper_runner.py
"""
tdd_gatekeeper_runner.py - Script de automatización para el Strict TDD Gatekeeper
Para uso exclusivo del skill tdd_gatekeeper.md.
"""
import os
import sys
import subprocess
import argparse

# Localizar la raíz del workspace de forma dinámica
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", "..", ".."))

# Agregar ruta para state_manager
OPENCODE_CORE = os.path.join(WORKSPACE_ROOT, ".opencode", "core")
HARNESS_CORE = os.path.join(WORKSPACE_ROOT, ".harness", "adaptation", "scripts")

if os.path.exists(OPENCODE_CORE):
    sys.path.insert(0, OPENCODE_CORE)
elif os.path.exists(HARNESS_CORE):
    sys.path.insert(0, HARNESS_CORE)

try:
    from state_manager import HarnessStateManager
except ImportError:
    print("[ERR] No se pudo importar state_manager.py. Asegúrate de compilar el arnés.", file=sys.stderr)
    sys.exit(1)


def parse_config_yaml(file_path):
    """Parsea claves simples de archivos config.yaml sin dependencias externas"""
    if not os.path.exists(file_path):
        return {}
        
    config = {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if ":" in line:
                    k, v = line.split(":", 1)
                    k = k.strip()
                    v = v.strip()
                    if k == "project":
                        continue
                    if "#" in v:
                        v = v.split("#", 1)[0].strip()
                    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
                        v = v[1:-1]
                    elif v.lower() == "true":
                        v = True
                    elif v.lower() == "false":
                        v = False
                    config[k] = v
    except Exception as e:
        print(f"[!] Error parseando config {file_path}: {e}")
    return config


def run_command(command_str):
    """Ejecuta un comando en la terminal y retorna (exit_code, stdout, stderr)"""
    try:
        # Ejecutar en el workspace root
        res = subprocess.run(
            command_str,
            shell=True,
            cwd=WORKSPACE_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return res.returncode, res.stdout, res.stderr
    except Exception as e:
        return -1, "", str(e)


def main():
    parser = argparse.ArgumentParser(description="Ejecutor y Validador Inteligente de TDD (Exclusivo de Skills)")
    parser.add_argument("--phase", required=True, choices=["red", "green", "refactor"], help="Fase actual de TDD a verificar")
    
    args = parser.parse_args()
    
    # Determinar si estamos en OpenCode o en Harness
    use_opencode = ".opencode" in BASE_DIR
    manager = HarnessStateManager(workspace_dir=WORKSPACE_ROOT, use_opencode=use_opencode)
    state = manager.load_state()
    
    active_profile = state.get("active_profile", "developer")
    
    # Resolver bypass_qa_execution y comandos
    profile_dir = ".opencode" if use_opencode else ".harness"
    profile_config_path = os.path.join(WORKSPACE_ROOT, profile_dir, "profiles", active_profile, "config.yaml")
    base_config_path = os.path.join(WORKSPACE_ROOT, profile_dir, "config.yaml")
    
    config = {}
    # Cargar base
    config.update(parse_config_yaml(base_config_path))
    # Sobrescribir con perfil si existe
    if os.path.exists(profile_config_path):
        config.update(parse_config_yaml(profile_config_path))
        
    bypass_qa = config.get("bypass_qa_execution", False)
    test_command = config.get("test_command", "pytest")
    lint_command = config.get("lint_command", "flake8")
    
    print(f"[*] Perfil activo: {active_profile}")
    print(f"[*] bypass_qa_execution: {bypass_qa}")
    print(f"[*] Comando de tests: '{test_command}'")
    print(f"[*] Comando de linter: '{lint_command}'")
    print(f"[*] Fase a verificar: {args.phase.upper()}")
    print("--------------------------------------------------")
    
    if bypass_qa:
        print(f"[OK] bypass_qa_execution está habilitado. Se asume verificación estática exitosa.")
        if args.phase == "red":
            state["test_status"] = "failing"
        else:
            state["test_status"] = "passing"
        state["last_error"] = ""
        manager.save_state(state)
        sys.exit(0)
        
    # Ejecutar comandos reales si bypass_qa es False
    if args.phase == "red":
        # RED: Esperamos que las pruebas FALLEN
        print(f"[*] Corriendo tests esperando que fallen (RED)...")
        code, out, err = run_command(test_command)
        
        if code != 0:
            print(f"[OK] ¡Prueba falló exitosamente en fase RED! (Salida esperada)")
            state["test_status"] = "failing"
            state["last_error"] = ""
            manager.save_state(state)
            sys.exit(0)
        else:
            print(f"[ERR] Fallo de TDD: Los tests pasaron, pero en fase RED se esperaba que fallaran.", file=sys.stderr)
            state["test_status"] = "passing"
            state["last_error"] = "TDD Red Phase failure: Tests passed when they should have failed."
            manager.save_state(state)
            sys.exit(1)
            
    elif args.phase == "green":
        # GREEN: Esperamos que las pruebas PASEN
        print(f"[*] Corriendo tests esperando que pasen (GREEN)...")
        code, out, err = run_command(test_command)
        
        if code == 0:
            print(f"[OK] ¡Prueba pasó exitosamente! Estado GREEN alcanzado.")
            state["test_status"] = "passing"
            state["last_error"] = ""
            manager.save_state(state)
            sys.exit(0)
        else:
            print(f"[ERR] Tests fallando en fase GREEN.", file=sys.stderr)
            print(f"Detalle de salida:\n{out}\n{err}", file=sys.stderr)
            state["test_status"] = "failing"
            state["last_error"] = f"Green phase failure:\n{out}\n{err}"
            manager.save_state(state)
            sys.exit(1)
            
    elif args.phase == "refactor":
        # REFACTOR: Esperamos linter y tests exitosos
        print(f"[*] Corriendo linter...")
        l_code, l_out, l_err = run_command(lint_command)
        if l_code != 0:
            print(f"[ERR] Fallo de linter en fase REFACTOR.", file=sys.stderr)
            print(f"Detalle de linter:\n{l_out}\n{l_err}", file=sys.stderr)
            state["test_status"] = "failing"
            state["last_error"] = f"Refactor phase linter failure:\n{l_out}\n{l_err}"
            manager.save_state(state)
            sys.exit(1)
            
        print(f"[*] Corriendo tests...")
        code, out, err = run_command(test_command)
        
        if code == 0:
            print(f"[OK] ¡Linter y tests exitosos en fase REFACTOR!")
            state["test_status"] = "passing"
            state["last_error"] = ""
            manager.save_state(state)
            sys.exit(0)
        else:
            print(f"[ERR] Tests fallando después de refactorización.", file=sys.stderr)
            state["test_status"] = "failing"
            state["last_error"] = f"Refactor phase test failure:\n{out}\n{err}"
            manager.save_state(state)
            sys.exit(1)


if __name__ == "__main__":
    main()
