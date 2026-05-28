# compiler.py
import os
import shutil
import re
import sys

from constants import POINTER_TEXT, POINTER_TEXT_OPENCODE, REPLACEMENTS
from translator import get_frontmatter, extract_metadata, translate_and_write
from sync import sync_manifest

def compile_for_opencode():
    """Compila todo el arnés a estructura nativa de OpenCode"""
    print("⚙️ Compilando Arnés a formato nativo de OpenCode...")
    os.makedirs(".opencode/agents", exist_ok=True)
    os.makedirs(".opencode/skills", exist_ok=True)
    os.makedirs(".opencode/memory", exist_ok=True)
    os.makedirs(".opencode/artifacts/templates", exist_ok=True)
    os.makedirs(".opencode/artifacts/current_run", exist_ok=True)
    
    # --- 1. COMPILAR ARCHIVOS CORE ---
    
    # 1.1. Transpilar Agentes Core (Roles)
    if os.path.exists(".harness/roles"):
        for filename in os.listdir(".harness/roles"):
            if filename.endswith(".md"):
                filepath = os.path.join(".harness/roles", filename)
                title, desc, content = extract_metadata(filepath)
                is_primary = (filename == "orchestrator.md")
                frontmatter = get_frontmatter(title, desc, is_skill=False, is_primary=is_primary)
                agent_name = filename.replace("_agent", "").replace("_", "-")
                dest_path = os.path.join(".opencode/agents", agent_name)
                
                for k, v in REPLACEMENTS.items():
                    content = content.replace(k, v)
                
                with open(dest_path, "w", encoding="utf-8") as f:
                    f.write(frontmatter + "\n" + content)
                print(f"  + Agente core generado: .opencode/agents/{agent_name}")

    # 1.2. Transpilar Skills Core
    if os.path.exists(".harness/skills"):
        for filename in os.listdir(".harness/skills"):
            filepath = os.path.join(".harness/skills", filename)
            if os.path.isdir(filepath):
                skill_md_path = os.path.join(filepath, "SKILL.md")
                if not os.path.exists(skill_md_path):
                    skill_md_path = os.path.join(filepath, f"{filename}.md")
                
                if os.path.exists(skill_md_path):
                    title, desc, content = extract_metadata(skill_md_path)
                    skill_name = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
                    skill_dir = os.path.join(".opencode/skills", skill_name)
                    os.makedirs(skill_dir, exist_ok=True)
                    
                    for k, v in REPLACEMENTS.items():
                        content = content.replace(k, v)
                    
                    frontmatter = get_frontmatter(title, desc, is_skill=True)
                    with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
                        f.write(frontmatter + "\n" + content)
                    print(f"  + Skill core generada (directorio): .opencode/skills/{skill_name}/SKILL.md")
                    
                    # Copiar otros archivos recursivamente, preservando subdirectorios (ej. assets)
                    for root, dirs, files in os.walk(filepath):
                        for file in files:
                            src_file = os.path.join(root, file)
                            rel_path = os.path.relpath(src_file, filepath)
                            if rel_path in ["SKILL.md", f"{filename}.md"]:
                                continue
                            dest_file = os.path.join(skill_dir, rel_path)
                            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                            shutil.copy2(src_file, dest_file)
                            print(f"    + Archivo copiado: {dest_file}")
            elif filename.endswith(".md"):
                title, desc, content = extract_metadata(filepath)
                skill_name = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
                skill_dir = os.path.join(".opencode/skills", skill_name)
                os.makedirs(skill_dir, exist_ok=True)
                
                for k, v in REPLACEMENTS.items():
                    content = content.replace(k, v)
                
                frontmatter = get_frontmatter(title, desc, is_skill=True)
                with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
                    f.write(frontmatter + "\n" + content)
                print(f"  + Skill core generada: .opencode/skills/{skill_name}/SKILL.md")
                
    # 1.3. Copiar Memory Core
    if os.path.exists(".harness/memory"):
        for filename in os.listdir(".harness/memory"):
            if filename.endswith(".md"):
                translate_and_write(
                    os.path.join(".harness/memory", filename),
                    os.path.join(".opencode/memory", filename)
                )
                print(f"  + Memoria core copiada: .opencode/memory/{filename}")
                
    # 1.4. Copiar Plantillas Core
    if os.path.exists(".harness/artifacts/templates"):
        for filename in os.listdir(".harness/artifacts/templates"):
            if filename.endswith((".yaml", ".yml", ".md")):
                translate_and_write(
                    os.path.join(".harness/artifacts/templates", filename),
                    os.path.join(".opencode/artifacts/templates", filename)
                )
                print(f"  + Plantilla core copiada: .opencode/artifacts/templates/{filename}")

    # 1.5. Copiar Config Core
    if os.path.exists(".harness/config.yaml"):
        translate_and_write(".harness/config.yaml", ".opencode/config.yaml")
        print("  + Configuración core copiada: .opencode/config.yaml")

    # --- 2. INSTRUCCIONES POINTER ---
    with open(".opencode/instructions.md", "w", encoding="utf-8") as f:
        f.write(POINTER_TEXT_OPENCODE)

def adapt_to_tool(tool_name):
    """Adapta el arnés de entrada a un formato específico de herramienta (Claude/Cursor/OpenCode)"""
    print(f"🧹 Limpiando adaptadores anteriores...")
    for f in [".clinerules", ".cursorrules"]:
        if os.path.exists(f): os.remove(f)
    if os.path.exists(".opencode"):
        shutil.rmtree(".opencode", ignore_errors=True)

    if tool_name in ["claude", "roo", "cline"]:
        sync_manifest(use_opencode=False)
        with open(".clinerules", "w", encoding="utf-8") as f:
            f.write(POINTER_TEXT)
        print("✅ Arnés adaptado para Claude Code / Roo Code (Se generó .clinerules)")
        
    elif tool_name == "cursor":
        sync_manifest(use_opencode=False)
        with open(".cursorrules", "w", encoding="utf-8") as f:
            f.write(POINTER_TEXT)
        print("✅ Arnés adaptado para Cursor (Se generó .cursorrules)")
        
    elif tool_name == "opencode":
        compile_for_opencode()
        sync_manifest(use_opencode=True)
        print("✅ Arnés transpilado exitosamente a la estructura nativa de OpenCode.")
        
    else:
        print(f"❌ Herramienta desconocida: {tool_name}")
        sys.exit(1)
