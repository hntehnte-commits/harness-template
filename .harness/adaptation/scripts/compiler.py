# compiler.py
import os
import shutil
import re
import sys

from constants import POINTER_TEXT, POINTER_TEXT_OPENCODE, REPLACEMENTS
from translator import get_frontmatter, extract_metadata, translate_and_write
from sync import sync_manifest

def apply_profile_to_harness(profile):
    """Aplica perfil a la carpeta plantilla .harness/ (Claude/Cursor)"""
    profile_dir = os.path.join(".harness/profiles", profile)
    if not os.path.exists(profile_dir):
        print(f"❌ Perfil no encontrado: {profile}")
        return
        
    print(f"✨ Aplicando perfil '{profile}' a la plantilla de origen .harness/...")
    
    # 1. Copiar config.yaml del perfil
    profile_config = os.path.join(profile_dir, "config.yaml")
    if os.path.exists(profile_config):
        shutil.copy(profile_config, ".harness/config.yaml")
        print("  + Se sobreescribió .harness/config.yaml")
        
    # 2. Copiar memory del perfil
    profile_memory = os.path.join(profile_dir, "memory")
    if os.path.exists(profile_memory):
        for filename in os.listdir(profile_memory):
            if filename.endswith(".md"):
                shutil.copy(
                    os.path.join(profile_memory, filename),
                    os.path.join(".harness/memory", filename)
                )
                print(f"  + Se sobreescribió .harness/memory/{filename}")

    # 3. Copiar roles del perfil
    profile_roles = os.path.join(profile_dir, "roles")
    if os.path.exists(profile_roles):
        for filename in os.listdir(profile_roles):
            if filename.endswith(".md"):
                shutil.copy(
                    os.path.join(profile_roles, filename),
                    os.path.join(".harness/roles", filename)
                )
                print(f"  + Se sobreescribió .harness/roles/{filename}")

    # 4. Copiar skills del perfil
    profile_skills = os.path.join(profile_dir, "skills")
    if os.path.exists(profile_skills):
        for filename in os.listdir(profile_skills):
            if filename.endswith(".md"):
                shutil.copy(
                    os.path.join(profile_skills, filename),
                    os.path.join(".harness/skills", filename)
                )
                print(f"  + Se sobreescribió .harness/skills/{filename}")

    # 5. Copiar templates de artefactos del perfil
    profile_templates = os.path.join(profile_dir, "artifacts/templates")
    if os.path.exists(profile_templates):
        for filename in os.listdir(profile_templates):
            if filename.endswith((".yaml", ".yml", ".md")):
                os.makedirs(".harness/artifacts/templates", exist_ok=True)
                shutil.copy(
                    os.path.join(profile_templates, filename),
                    os.path.join(".harness/artifacts/templates", filename)
                )
                print(f"  + Se sobreescribió .harness/artifacts/templates/{filename}")

def compile_profile_overlay(profile, is_default=False):
    """Copia la sobrecapa del perfil hacia la estructura de .opencode/"""
    profile_dir = os.path.join(".harness/profiles", profile)
    if not os.path.exists(profile_dir):
        print(f"❌ Perfil no encontrado: {profile}")
        return
        
    print(f"✨ Aplicando perfil '{profile}' (por defecto: {is_default}) en .opencode/...")
    
    # Asegurar existencia de directorios de destino
    os.makedirs(".opencode/memory", exist_ok=True)
    os.makedirs(".opencode/agents", exist_ok=True)
    os.makedirs(".opencode/skills", exist_ok=True)
    os.makedirs(".opencode/artifacts/templates", exist_ok=True)
    
    # 1. Copiar config.yaml del perfil
    dest_profile_dir = os.path.join(".opencode/profiles", profile)
    os.makedirs(dest_profile_dir, exist_ok=True)
    profile_config = os.path.join(profile_dir, "config.yaml")
    if os.path.exists(profile_config):
        translate_and_write(profile_config, os.path.join(dest_profile_dir, "config.yaml"))
        if is_default:
            shutil.copy(profile_config, ".opencode/config.yaml")
            print(f"  + Se sobreescribió .opencode/config.yaml con el de {profile}")

    # 2. Copiar memory del perfil
    profile_memory = os.path.join(profile_dir, "memory")
    if os.path.exists(profile_memory):
        for filename in os.listdir(profile_memory):
            if filename.endswith(".md"):
                translate_and_write(
                    os.path.join(profile_memory, filename),
                    os.path.join(".opencode/memory", filename)
                )
                print(f"  + Memoria copiada por perfil: .opencode/memory/{filename}")

    # 3. Copiar roles del perfil
    profile_roles = os.path.join(profile_dir, "roles")
    if os.path.exists(profile_roles):
        for filename in os.listdir(profile_roles):
            if filename.endswith(".md"):
                filepath = os.path.join(profile_roles, filename)
                title, desc, content = extract_metadata(filepath)
                is_primary = (filename == "orchestrator.md")
                frontmatter = get_frontmatter(title, desc, is_skill=False, is_primary=is_primary)
                agent_name = filename.replace("_agent", "").replace("_", "-")
                dest_path = os.path.join(".opencode/agents", agent_name)
                
                for k, v in REPLACEMENTS.items():
                    content = content.replace(k, v)
                
                with open(dest_path, "w", encoding="utf-8") as f:
                    f.write(frontmatter + "\n" + content)
                print(f"  + Agente sobreescrito por perfil: .opencode/agents/{agent_name}")

    # 4. Copiar skills del perfil
    profile_skills = os.path.join(profile_dir, "skills")
    if os.path.exists(profile_skills):
        for filename in os.listdir(profile_skills):
            filepath = os.path.join(profile_skills, filename)
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
                    print(f"  + Skill de perfil generada (directorio): .opencode/skills/{skill_name}/SKILL.md")
                    
                    # Copiar recursivamente el resto del directorio
                    for root, dirs, files in os.walk(filepath):
                        for file in files:
                            src_file = os.path.join(root, file)
                            rel_path = os.path.relpath(src_file, filepath)
                            if rel_path in ["SKILL.md", f"{filename}.md"]:
                                continue
                            dest_file = os.path.join(skill_dir, rel_path)
                            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                            shutil.copy2(src_file, dest_file)
                            print(f"    + Archivo de skill de perfil copiado: {dest_file}")
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
                print(f"  + Skill copiada por perfil: .opencode/skills/{skill_name}/SKILL.md")

    # 5. Copiar templates de artefactos del perfil
    profile_templates = os.path.join(profile_dir, "artifacts/templates")
    if os.path.exists(profile_templates):
        for filename in os.listdir(profile_templates):
            if filename.endswith((".yaml", ".yml", ".md")):
                translate_and_write(
                    os.path.join(profile_templates, filename),
                    os.path.join(".opencode/artifacts/templates", filename)
                )
                print(f"  + Plantilla sobreescrita por perfil: .opencode/artifacts/templates/{filename}")

def remove_profile_overlay(profile_name):
    """Limpia los archivos correspondientes a un perfil en .opencode/"""
    print(f"🧹 Removiendo perfil '{profile_name}' de .opencode/...")
    
    # 1. Eliminar directorio de perfil
    profile_dir = os.path.join(".opencode/profiles", profile_name)
    if os.path.exists(profile_dir):
        shutil.rmtree(profile_dir, ignore_errors=True)
        print(f"  - Perfil removido: .opencode/profiles/{profile_name}")
        
    # 2. Eliminar skills de ese perfil
    src_profile_skills = os.path.join(".harness/profiles", profile_name, "skills")
    if os.path.exists(src_profile_skills):
        for filename in os.listdir(src_profile_skills):
            filepath = os.path.join(src_profile_skills, filename)
            if os.path.isdir(filepath):
                skill_md_path = os.path.join(filepath, "SKILL.md")
                if not os.path.exists(skill_md_path):
                    skill_md_path = os.path.join(filepath, f"{filename}.md")
                if os.path.exists(skill_md_path):
                    title, desc, _ = extract_metadata(skill_md_path)
                    skill_name = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
                    skill_dir = os.path.join(".opencode/skills", skill_name)
                    if os.path.exists(skill_dir):
                        shutil.rmtree(skill_dir, ignore_errors=True)
                        print(f"  - Skill de perfil removida (directorio): .opencode/skills/{skill_name}")
            elif filename.endswith(".md"):
                title, desc, _ = extract_metadata(filepath)
                skill_name = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
                skill_dir = os.path.join(".opencode/skills", skill_name)
                if os.path.exists(skill_dir):
                    shutil.rmtree(skill_dir, ignore_errors=True)
                    print(f"  - Skill removida: .opencode/skills/{skill_name}")

    # 3. Eliminar memory de ese perfil
    src_profile_memory = os.path.join(".harness/profiles", profile_name, "memory")
    if os.path.exists(src_profile_memory):
        for filename in os.listdir(src_profile_memory):
            if filename.endswith(".md"):
                dest_filepath = os.path.join(".opencode/memory", filename)
                if os.path.exists(dest_filepath):
                    os.remove(dest_filepath)
                    print(f"  - Memoria removida: {dest_filepath}")

    # 4. Eliminar roles de ese perfil
    src_profile_roles = os.path.join(".harness/profiles", profile_name, "roles")
    if os.path.exists(src_profile_roles):
        for filename in os.listdir(src_profile_roles):
            if filename.endswith(".md"):
                agent_name = filename.replace("_agent", "").replace("_", "-")
                dest_filepath = os.path.join(".opencode/agents", agent_name)
                if os.path.exists(dest_filepath):
                    os.remove(dest_filepath)
                    print(f"  - Agente removido: {dest_filepath}")

    # 5. Eliminar templates de ese perfil
    src_profile_templates = os.path.join(".harness/profiles", profile_name, "artifacts/templates")
    if os.path.exists(src_profile_templates):
        for filename in os.listdir(src_profile_templates):
            if filename.endswith((".yaml", ".yml", ".md")):
                dest_filepath = os.path.join(".opencode/artifacts/templates", filename)
                if os.path.exists(dest_filepath):
                    os.remove(dest_filepath)
                    print(f"  - Plantilla removida: {dest_filepath}")

def compile_for_opencode(profile=None):
    """Compila todo el arnés a estructura nativa de OpenCode"""
    print("⚙️ Compilando Arnés a formato nativo de OpenCode...")
    os.makedirs(".opencode/agents", exist_ok=True)
    os.makedirs(".opencode/skills", exist_ok=True)
    os.makedirs(".opencode/memory", exist_ok=True)
    os.makedirs(".opencode/artifacts/templates", exist_ok=True)
    os.makedirs(".opencode/artifacts/current_run", exist_ok=True)
    os.makedirs(".opencode/profiles", exist_ok=True)
    
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

    # --- 2. COMPILAR SOBRECAPAS (OVERLAYS) DE TODOS LOS PERFILES ---
    profiles_dir = ".harness/profiles"
    if os.path.exists(profiles_dir):
        for p in os.listdir(profiles_dir):
            p_path = os.path.join(profiles_dir, p)
            if os.path.isdir(p_path):
                is_default = (p == profile)
                compile_profile_overlay(p, is_default=is_default)

    # --- 3. INSTRUCCIONES POINTER ---
    with open(".opencode/instructions.md", "w", encoding="utf-8") as f:
        f.write(POINTER_TEXT_OPENCODE)

def adapt_to_tool(tool_name, profile=None):
    """Adapta el arnés de entrada a un formato específico de herramienta (Claude/Cursor/OpenCode)"""
    print(f"🧹 Limpiando adaptadores anteriores...")
    for f in [".clinerules", ".cursorrules"]:
        if os.path.exists(f): os.remove(f)
    if os.path.exists(".opencode"):
        shutil.rmtree(".opencode", ignore_errors=True)

    # Si hay perfil y herramienta claude o cursor, aplicar sobrecapa a .harness/ primero
    if profile and tool_name in ["claude", "roo", "cline", "cursor"]:
        apply_profile_to_harness(profile)

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
        compile_for_opencode(profile)
        sync_manifest(use_opencode=True)
        print("✅ Arnés transpilado exitosamente a la estructura nativa de OpenCode.")
        
    else:
        print(f"❌ Herramienta desconocida: {tool_name}")
        sys.exit(1)
