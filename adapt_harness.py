import sys
import os
import argparse
import re
import shutil

# Este es el "Apuntador". Le dice a la herramienta que vaya a leer el Harness dinámicamente.
POINTER_TEXT = """# SYSTEM HARNESS DIRECTIVE
You are operating within a strict multi-agent Harness system.
BEFORE doing anything else, you MUST read the file `AGENTS.md` to understand the project structure,
and then read `/.harness/roles/orchestrator.md` to begin the initialization process. 
Do not proceed with the user's task until you have assumed the Orchestrator role.
"""

def get_frontmatter(title, desc, is_skill=False, is_primary=False):
    """Genera el Frontmatter YAML nativo de OpenCode"""
    if is_skill:
        safe_name = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        return f"---\nname: {safe_name}\ndescription: {desc}\n---\n"
    else:
        mode = "primary" if is_primary else "subagent"
        return f"---\ndescription: {desc}\nmode: {mode}\n---\n"

def extract_metadata(filepath):
    """Extrae el titulo y una descripción corta del Markdown del Arnés"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    lines = content.split('\n')
    title = lines[0].replace("# Role: ", "").replace("# Skill: ", "").strip()
    desc = "Harness component"
    for line in lines[1:]:
        # Busca la primera línea con texto real que no sea un título para la descripción
        if line.strip() and not line.startswith("#"):
            desc = line.strip()
            break
            
    return title, desc, content

def compile_for_opencode():
    print("⚙️ Compilando Arnés a formato nativo de OpenCode...")
    os.makedirs(".opencode/agents", exist_ok=True)
    os.makedirs(".opencode/skills", exist_ok=True)
    
    # 1. Transpilar Agentes (Roles)
    if os.path.exists(".harness/roles"):
        for filename in os.listdir(".harness/roles"):
            if filename.endswith(".md"):
                filepath = os.path.join(".harness/roles", filename)
                title, desc, content = extract_metadata(filepath)
                
                is_primary = (filename == "orchestrator.md")
                frontmatter = get_frontmatter(title, desc, is_skill=False, is_primary=is_primary)
                
                # Para opencode, cambiamos el nombre (ej. dev_agent.md -> dev.md)
                agent_name = filename.replace("_agent", "").replace("_", "-")
                dest_path = os.path.join(".opencode/agents", agent_name)
                
                with open(dest_path, "w", encoding="utf-8") as f:
                    f.write(frontmatter + "\n" + content)
                print(f"  + Agente nativo generado: .opencode/agents/{agent_name}")

    # 2. Transpilar Skills
    if os.path.exists(".harness/skills"):
        for filename in os.listdir(".harness/skills"):
            if filename.endswith(".md"):
                filepath = os.path.join(".harness/skills", filename)
                title, desc, content = extract_metadata(filepath)
                
                skill_name = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
                skill_dir = os.path.join(".opencode/skills", skill_name)
                os.makedirs(skill_dir, exist_ok=True)
                
                frontmatter = get_frontmatter(title, desc, is_skill=True)
                with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
                    f.write(frontmatter + "\n" + content)
                print(f"  + Skill nativa generada: .opencode/skills/{skill_name}/SKILL.md")
                
    # 3. Base instructions (Pointer)
    with open(".opencode/instructions.md", "w", encoding="utf-8") as f:
        f.write(POINTER_TEXT)

def adapt_to_tool(tool_name):
    print(f"🧹 Limpiando adaptadores anteriores...")
    for f in [".clinerules", ".cursorrules"]:
        if os.path.exists(f): os.remove(f)
    if os.path.exists(".opencode"):
        shutil.rmtree(".opencode", ignore_errors=True)

    if tool_name in ["claude", "roo", "cline"]:
        with open(".clinerules", "w", encoding="utf-8") as f:
            f.write(POINTER_TEXT)
        print("✅ Arnés adaptado para Claude Code / Roo Code (Se generó .clinerules)")
        
    elif tool_name == "cursor":
        with open(".cursorrules", "w", encoding="utf-8") as f:
            f.write(POINTER_TEXT)
        print("✅ Arnés adaptado para Cursor (Se generó .cursorrules)")
        
    elif tool_name == "opencode":
        compile_for_opencode()
        print("✅ Arnés transpilado exitosamente a la estructura nativa de OpenCode.")
        
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

    if os.path.exists("AGENTS.md"):
        with open("AGENTS.md", "r", encoding="utf-8") as f:
            content = f.read()
            
        import re
        content = re.sub(r'(### Available Sub-Agents \(Roles\)\n).*?(?=\n##|\Z)', r'\1' + roles_text, content, flags=re.DOTALL)
        if "### Available Skills" not in content:
            content += "\n### Available Skills\n" + skills_text
        else:
            content = re.sub(r'(### Available Skills\n).*?(?=\n##|\Z)', r'\1' + skills_text, content, flags=re.DOTALL)

        with open("AGENTS.md", "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ AGENTS.md actualizado dinámicamente.")
    else:
        print("❌ No se encontró AGENTS.md para sincronizar.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Adapta el Harness a una herramienta de IA específica.")
    parser.add_argument("tool", choices=["claude", "cursor", "opencode", "sync"], help="La herramienta a usar")
    args = parser.parse_args()
    
    if args.tool == "sync":
        sync_manifest()
    else:
        adapt_to_tool(args.tool)
