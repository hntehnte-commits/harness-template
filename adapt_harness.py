import sys
import os
import argparse

# Este es el "Apuntador". Le dice a la herramienta que vaya a leer el Harness.
POINTER_TEXT = """# SYSTEM HARNESS DIRECTIVE
You are operating within a strict multi-agent Harness system.
BEFORE doing anything else, you MUST read the file: `AGENTS.md` to understand the project structure,
and then read `.harness/harness_entry.md` to begin the initialization process. 
Do not proceed with the user's task until you have assumed the Orchestrator role.
"""

def adapt_to_tool(tool_name):
    print(f"🧹 Limpiando adaptadores anteriores...")
    # Limpiar adaptadores anteriores para evitar conflictos si cambias de herramienta
    for f in [".clinerules", ".cursorrules"]:
        if os.path.exists(f):
            os.remove(f)
            
    if os.path.exists(".opencode/instructions.md"):
        os.remove(".opencode/instructions.md")

    # Inyectar el nuevo adaptador
    if tool_name in ["claude", "roo", "cline"]:
        with open(".clinerules", "w", encoding="utf-8") as f:
            f.write(POINTER_TEXT)
        print("✅ Arnés adaptado para Claude Code / Roo Code (Se generó .clinerules)")
        
    elif tool_name == "cursor":
        with open(".cursorrules", "w", encoding="utf-8") as f:
            f.write(POINTER_TEXT)
        print("✅ Arnés adaptado para Cursor (Se generó .cursorrules)")
        
    elif tool_name == "opencode":
        os.makedirs(".opencode", exist_ok=True)
        with open(".opencode/instructions.md", "w", encoding="utf-8") as f:
            f.write(POINTER_TEXT)
        print("✅ Arnés adaptado para OpenCode (Se generó .opencode/instructions.md)")
        
    else:
        print(f"❌ Herramienta desconocida: {tool_name}")
        sys.exit(1)

def sync_manifest():
    print("🔄 Sincronizando AGENTS.md con los roles y skills disponibles...")
    
    roles_text = ""
    for filepath in os.listdir(".harness/roles"):
        if filepath.endswith(".md"):
            with open(os.path.join(".harness/roles", filepath), "r", encoding="utf-8") as f:
                first_line = f.readline().strip().replace("# Role: ", "")
                roles_text += f"- **{first_line}** (`/.harness/roles/{filepath}`)\n"

    skills_text = ""
    for filepath in os.listdir(".harness/skills"):
        if filepath.endswith(".md"):
            with open(os.path.join(".harness/skills", filepath), "r", encoding="utf-8") as f:
                first_line = f.readline().strip().replace("# Skill: ", "")
                skills_text += f"- **{first_line}** (`/.harness/skills/{filepath}`)\n"

    # Actualizar AGENTS.md (reemplazo simple de secciones para el ejemplo)
    if os.path.exists("AGENTS.md"):
        with open("AGENTS.md", "r", encoding="utf-8") as f:
            content = f.read()
            
        import re
        # Reemplazar Sub-Agents
        content = re.sub(r'(### Available Sub-Agents \(Roles\)\n).*?(?=\n##|\Z)', r'\1' + roles_text, content, flags=re.DOTALL)
        # Asegurar que los skills estén listados
        if "### Available Skills" not in content:
            content += "\n### Available Skills\n" + skills_text
        else:
            content = re.sub(r'(### Available Skills\n).*?(?=\n##|\Z)', r'\1' + skills_text, content, flags=re.DOTALL)

        with open("AGENTS.md", "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ AGENTS.md actualizado dinámicamente con los nuevos Agentes y Skills.")
    else:
        print("❌ No se encontró AGENTS.md para sincronizar.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Adapta el Harness a una herramienta de IA específica.")
    parser.add_argument("tool", choices=["claude", "cursor", "opencode", "sync"], help="La herramienta a usar (o 'sync' para actualizar AGENTS.md)")
    args = parser.parse_args()
    
    if args.tool == "sync":
        sync_manifest()
    else:
        adapt_to_tool(args.tool)
