# state_manager.py
"""
state_manager.py - Gestor de estado core para el Harness Multi-Agente
Proporciona API programática y comandos CLI para manipular state.yaml
utilizando únicamente la librería estándar de Python (cero dependencias).
"""
import os
import re
import sys
import argparse

class HarnessStateManager:
    """Clase principal para cargar, modificar, validar y serializar el estado del Harness"""
    
    ALLOWED_PHASES = ["Initialization", "Contract", "Implementation", "Audit", "Documentation", "Complete"]
    ALLOWED_AGENTS = ["orchestrator", "spec", "embedded-developer", "python-developer", "javascript-developer", "developer", "qa", "docs"]
    ALLOWED_TEST_STATUS = ["unknown", "passing", "failing"]
    ALLOWED_TASK_STATUS = ["pending", "in_progress", "completed"]

    def __init__(self, workspace_dir=".", use_opencode=True):
        self.workspace_dir = workspace_dir
        self.use_opencode = use_opencode
        self.harness_dir = os.path.join(workspace_dir, ".opencode" if use_opencode else ".harness")
        self.state_file = os.path.join(self.harness_dir, "artifacts", "current_run", "state.yaml")
        self.schema_file = os.path.join(self.harness_dir, "artifacts", "templates", "state_schema.yaml")

    def load_state(self):
        """Carga y parsea el archivo state.yaml si existe, de lo contrario retorna un estado vacío inicial"""
        if not os.path.exists(self.state_file):
            return self.get_initial_state()
        
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.parse_yaml(content)
        except Exception as e:
            print(f"[ERR] No se pudo leer el estado: {e}", file=sys.stderr)
            return self.get_initial_state()

    def get_initial_state(self):
        """Retorna un diccionario de estado inicial predeterminado"""
        return {
            "current_phase": "Initialization",
            "active_agent": "orchestrator",
            "plan_approved": False,
            "active_profile": "developer",
            "task_checklist": [],
            "test_status": "unknown",
            "last_error": ""
        }

    def save_state(self, state):
        """Valida y guarda de forma atómica el estado a state.yaml"""
        # Validar el esquema antes de guardar
        success, err_msg = self.validate_schema(state)
        if not success:
            raise ValueError(f"Error de validación del esquema de estado: {err_msg}")

        # Crear directorios si no existen
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        
        yaml_content = self.serialize_yaml(state)
        
        # Escritura atómica
        temp_file = self.state_file + ".tmp"
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(yaml_content)
            os.replace(temp_file, self.state_file)
            return True
        except Exception as e:
            if os.path.exists(temp_file):
                os.remove(temp_file)
            raise IOError(f"No se pudo guardar el archivo de estado: {e}")

    def validate_schema(self, state):
        """Valida que un diccionario de estado cumpla con las restricciones del esquema"""
        if not isinstance(state, dict):
            return False, "El estado debe ser un diccionario."

        required_keys = ["current_phase", "active_agent", "plan_approved", "active_profile", "test_status"]
        for key in required_keys:
            if key not in state:
                return False, f"Falta la clave requerida: {key}"

        if state["current_phase"] not in self.ALLOWED_PHASES:
            return False, f"Fase inválida: '{state['current_phase']}'. Permitidas: {self.ALLOWED_PHASES}"

        if state["active_agent"] not in self.ALLOWED_AGENTS:
            return False, f"Agente inválido: '{state['active_agent']}'. Permitidos: {self.ALLOWED_AGENTS}"

        if not isinstance(state["plan_approved"], bool):
            return False, "plan_approved debe ser un booleano (True/False)."

        if state["test_status"] not in self.ALLOWED_TEST_STATUS:
            return False, f"test_status inválido: '{state['test_status']}'. Permitidos: {self.ALLOWED_TEST_STATUS}"

        if "task_checklist" in state:
            if not isinstance(state["task_checklist"], list):
                return False, "task_checklist debe ser una lista."
            
            for idx, item in enumerate(state["task_checklist"]):
                if not isinstance(item, dict):
                    return False, f"El elemento {idx} de task_checklist debe ser un diccionario."
                if "task" not in item or "status" not in item:
                    return False, f"El elemento {idx} de task_checklist debe contener 'task' y 'status'."
                if item["status"] not in self.ALLOWED_TASK_STATUS:
                    return False, f"Estado de tarea inválido en elemento {idx}: '{item['status']}'. Permitidos: {self.ALLOWED_TASK_STATUS}"

        return True, ""

    def parse_yaml(self, content):
        """Parser simple y robusto de YAML sin dependencias para state.yaml"""
        state = self.get_initial_state()
        lines = content.splitlines()
        in_checklist = False
        current_task = None
        
        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
                
            # Detectar inicio del checklist
            if stripped.startswith('task_checklist:'):
                state['task_checklist'] = []
                in_checklist = True
                continue
                
            if in_checklist:
                # Comprobar indentación para saber si seguimos en checklist
                indent = len(line) - len(line.lstrip())
                if indent < 4 and not stripped.startswith('-'):
                    in_checklist = False
                else:
                    if stripped.startswith('-'):
                        # Nueva tarea
                        item_str = stripped[1:].strip()
                        current_task = {}
                        state['task_checklist'].append(current_task)
                        if ':' in item_str:
                            k, v = item_str.split(':', 1)
                            current_task[k.strip()] = self._parse_val(v)
                    elif ':' in stripped and current_task is not None:
                        k, v = stripped.split(':', 1)
                        current_task[k.strip()] = self._parse_val(v)
                    continue
                    
            if ':' in stripped:
                k, v = stripped.split(':', 1)
                k = k.strip()
                if k == 'state':
                    continue
                state[k] = self._parse_val(v)
                
        return state

    def serialize_yaml(self, state):
        """Serializa un diccionario de estado a YAML formateado con doble comillas"""
        lines = ["# Archivo de seguimiento de estado autogenerado", "state:"]
        
        keys = ["current_phase", "active_agent", "plan_approved", "active_profile"]
        for k in keys:
            if k in state:
                val = state[k]
                if isinstance(val, bool):
                    val_str = str(val).lower()
                else:
                    val_str = f'"{val}"'
                lines.append(f"  {k}: {val_str}")
                
        if "task_checklist" in state and isinstance(state["task_checklist"], list):
            lines.append("  task_checklist:")
            for item in state["task_checklist"]:
                if isinstance(item, dict):
                    task_val = item.get("task", "").replace('"', '\\"')
                    status_val = item.get("status", "pending")
                    lines.append(f'    - task: "{task_val}"')
                    lines.append(f'      status: "{status_val}"')
                    
        keys_end = ["test_status", "last_error"]
        for k in keys_end:
            if k in state:
                val = state[k]
                if val is None:
                    val_str = '""'
                elif isinstance(val, bool):
                    val_str = str(val).lower()
                else:
                    val_escaped = str(val).replace('"', '\\"').replace('\n', '\\n')
                    val_str = f'"{val_escaped}"'
                lines.append(f"  {k}: {val_str}")
                
        return "\n".join(lines) + "\n"

    def _parse_val(self, v):
        v = v.strip()
        # Eliminar comentarios inline
        if '#' in v:
            v = v.split('#', 1)[0].strip()
        if v.lower() == 'true':
            return True
        if v.lower() == 'false':
            return False
        if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
            return v[1:-1]
        return v


def main():
    parser = argparse.ArgumentParser(description="Gestor de Estado del Harness Multi-Agente (Standard Library Only)")
    subparsers = parser.add_subparsers(dest="command", help="Comando a ejecutar")
    
    # Comando get
    subparsers.add_parser("get", help="Obtiene y muestra el estado actual en formato legible")
    
    # Comando update
    update_parser = subparsers.add_parser("update", help="Actualiza un valor simple en el estado")
    update_parser.add_argument("--key", required=True, help="Clave a actualizar (ej: plan_approved, test_status, active_profile)")
    update_parser.add_argument("--value", required=True, help="Valor a asignar")
    
    args = parser.parse_args()
    
    # Detectar directorio base del workspace
    # adapt_harness.py corre en el root, por lo que el Cwd es el root
    manager = HarnessStateManager(use_opencode=False) # Trabajamos sobre .harness por defecto y el transpiler lo compila
    
    if args.command == "get":
        state = manager.load_state()
        print("\n=== ESTADO ACTUAL DEL HARNESS ===")
        for k, v in state.items():
            if k != "task_checklist":
                print(f"  {k}: {v}")
        if state.get("task_checklist"):
            print("  task_checklist:")
            for idx, task in enumerate(state["task_checklist"]):
                print(f"    [{'x' if task['status'] == 'completed' else '/' if task['status'] == 'in_progress' else ' '}] {task['task']}")
        print("=================================\n")
        
    elif args.command == "update":
        state = manager.load_state()
        key = args.key
        val = args.value
        
        # Conversión de tipos
        if val.lower() == "true":
            val = True
        elif val.lower() == "false":
            val = False
            
        state[key] = val
        try:
            manager.save_state(state)
            print(f"[OK] Estado actualizado: '{key}' a '{val}'")
        except Exception as e:
            print(f"[ERR] Error al actualizar estado: {e}", file=sys.stderr)
            sys.exit(1)
            
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
