# state_transition.py
"""
state_transition.py - Script de transición de estados exclusivo para Roles
Permite al Orchestrator y otros sub-agentes realizar transiciones seguras.
"""
import os
import sys
import argparse

# Localizar la raíz del workspace de forma dinámica
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", "..", ".."))

# Agregar rutas de importación para state_manager
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


# Mapeo de IDs de agentes a sus nombres formales de directiva
AGENT_NAME_MAPPING = {
    "orchestrator": "Orchestrator",
    "spec": "Spec Agent",
    "developer": "Developer Agent",
    "embedded-developer": "Embedded Developer Agent",
    "python-developer": "Python Developer Agent",
    "javascript-developer": "Javascript Developer Agent",
    "qa": "QA Agent",
    "docs": "Docs Agent"
}


def transition(next_agent, next_phase, use_opencode=True):
    """Realiza la transición de agente y fase y escribe el estado de forma segura"""
    manager = HarnessStateManager(workspace_dir=WORKSPACE_ROOT, use_opencode=use_opencode)
    state = manager.load_state()
    
    old_agent = state.get("active_agent")
    old_phase = state.get("current_phase")
    
    # Asignar nuevos valores
    state["active_agent"] = next_agent
    state["current_phase"] = next_phase
    
    # Encontrar nombre formal de directiva
    formal_name = AGENT_NAME_MAPPING.get(next_agent)
    if not formal_name:
        # Fallback simple
        formal_name = next_agent.replace("-", " ").title() + " Agent"

    try:
        manager.save_state(state)
        
        # Loguear detalles del cambio
        print(f"\n[OK] Transición exitosa en state.yaml:")
        print(f"   - Agente: {old_agent} -> {next_agent}")
        print(f"   - Fase: {old_phase} -> {next_phase}\n")
        
        # Imprimir la directiva mágica de transición (debe ser la última línea o bloque visible)
        print(f"--> NEXT ROLE: {formal_name}")
        return True
    except Exception as e:
        print(f"[ERR] No se pudo completar la transición: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Script de Transición Atómica de Agentes y Fases (Exclusivo de Roles)")
    parser.add_argument("--agent", required=True, choices=list(AGENT_NAME_MAPPING.keys()), help="ID del siguiente agente")
    parser.add_argument("--phase", required=True, help="Nombre de la siguiente fase")
    
    args = parser.parse_args()
    
    # Detectar en qué entorno nos estamos ejecutando leyendo el path
    use_opencode = ".opencode" in BASE_DIR
    
    success = transition(args.agent, args.phase, use_opencode=use_opencode)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
