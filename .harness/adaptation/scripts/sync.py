# sync.py
import os
import re

def sync_manifest(use_opencode=None):
    """Sincroniza el manifiesto central AGENTS.md con los agentes y habilidades reales en el workspace"""
    if use_opencode is None:
        use_opencode = os.path.exists(".opencode")
        
    if use_opencode:
        print("🔄 Sincronizando AGENTS.md con los roles y skills disponibles en .opencode...")
        roles_text = ""
        if os.path.exists(".opencode/agents"):
            for filepath in sorted(os.listdir(".opencode/agents")):
                if filepath.endswith(".md"):
                    with open(os.path.join(".opencode/agents", filepath), "r", encoding="utf-8") as f:
                        first_line = ""
                        for line in f:
                            if line.strip().startswith("# Role:"):
                                first_line = line.strip().replace("# Role: ", "").replace("# Role:", "")
                                break
                        if not first_line:
                            first_line = filepath
                        roles_text += f"- **{first_line}** (`/.opencode/agents/{filepath}`)\n"

        skills_text = ""
        if os.path.exists(".opencode/skills"):
            for skill_dir in sorted(os.listdir(".opencode/skills")):
                skill_path = os.path.join(".opencode/skills", skill_dir)
                if os.path.isdir(skill_path):
                    skill_file = os.path.join(skill_path, "SKILL.md")
                    if os.path.exists(skill_file):
                        with open(skill_file, "r", encoding="utf-8") as f:
                            first_line = ""
                            for line in f:
                                if line.strip().startswith("# Skill:"):
                                    first_line = line.strip().replace("# Skill: ", "").replace("# Skill:", "")
                                    break
                            if not first_line:
                                first_line = skill_dir
                            skills_text += f"- **{first_line}** (`/.opencode/skills/{skill_dir}/SKILL.md`)\n"
    else:
        print("🔄 Sincronizando AGENTS.md con los roles y skills disponibles en .harness...")
        roles_text = ""
        if os.path.exists(".harness/roles"):
            for filepath in sorted(os.listdir(".harness/roles")):
                if filepath.endswith(".md"):
                    with open(os.path.join(".harness/roles", filepath), "r", encoding="utf-8") as f:
                        first_line = ""
                        for line in f:
                            if line.strip().startswith("# Role:"):
                                first_line = line.strip().replace("# Role: ", "").replace("# Role:", "")
                                break
                        if not first_line:
                            first_line = filepath
                        roles_text += f"- **{first_line}** (`/.harness/roles/{filepath}`)\n"

        skills_text = ""
        if os.path.exists(".harness/skills"):
            for filename in sorted(os.listdir(".harness/skills")):
                filepath = os.path.join(".harness/skills", filename)
                if os.path.isdir(filepath):
                    skill_md_path = os.path.join(filepath, "SKILL.md")
                    if not os.path.exists(skill_md_path):
                        skill_md_path = os.path.join(filepath, f"{filename}.md")
                    if os.path.exists(skill_md_path):
                        with open(skill_md_path, "r", encoding="utf-8") as f:
                            first_line = ""
                            for line in f:
                                if line.strip().startswith("# Skill:"):
                                    first_line = line.strip().replace("# Skill: ", "").replace("# Skill:", "")
                                    break
                            if not first_line:
                                first_line = filename
                            skills_text += f"- **{first_line}** (`/.harness/skills/{filename}/SKILL.md`)\n"
                elif filename.endswith(".md"):
                    with open(filepath, "r", encoding="utf-8") as f:
                        first_line = ""
                        for line in f:
                            if line.strip().startswith("# Skill:"):
                                first_line = line.strip().replace("# Skill: ", "").replace("# Skill:", "")
                                break
                        if not first_line:
                            first_line = filename
                        skills_text += f"- **{first_line}** (`/.harness/skills/{filename}`)\n"

    if os.path.exists("AGENTS.md"):
        with open("AGENTS.md", "r", encoding="utf-8") as f:
            content = f.read()
            
        # Leer configuración para actualizar sección de información del proyecto
        config_path = ".opencode/config.yaml" if use_opencode else ".harness/config.yaml"
        project_name = None
        project_stack = None
        test_command = None
        lint_command = None
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                config_content = f.read()
                
            def extract_yaml_prop(prop_name, yaml_content):
                match = re.search(rf'{prop_name}:\s*(.*?)\s*$', yaml_content, re.MULTILINE)
                if not match:
                    return None
                val = match.group(1).split('#')[0].strip()
                if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                    val = val[1:-1].strip()
                return val

            project_name = extract_yaml_prop("name", config_content)
            project_stack = extract_yaml_prop("stack", config_content)
            test_command = extract_yaml_prop("test_command", config_content)
            lint_command = extract_yaml_prop("lint_command", config_content)

        # Generar texto de la sección de Project Information
        project_info = "## 1. Project Information\n"
        if project_name:
            project_info += f"- **Project Name**: {project_name}\n"
        else:
            project_info += "- **Project Name**: [Nombre del Proyecto]\n"
        
        if project_stack:
            project_info += f"- **Active Profile / Stack**: {project_stack}\n"
            
        if test_command:
            project_info += f"- **Test Command**: `{test_command}`\n"
            
        if lint_command:
            project_info += f"- **Lint Command**: `{lint_command}`\n"
            
        project_info += "- **Source Code Location**: `/src/` (Asegúrate de cambiar esto a tu carpeta real de código)\n"
        project_info += "- **Tests Location**: `/tests/` (Asegúrate de cambiar esto a tu carpeta real de tests)\n"

        content = re.sub(r'## 1\. Project Information\n.*?(?=\n##|\Z)', project_info, content, flags=re.DOTALL)
            
        content = re.sub(r'(### Available Sub-Agents \(Roles\)\n).*?(?=\n##|\Z)', r'\1' + roles_text, content, flags=re.DOTALL)
        if "### Available Skills" not in content:
            content += "\n### Available Skills\n" + skills_text
        else:
            content = re.sub(r'(### Available Skills\n).*?(?=\n##|\Z)', r'\1' + skills_text, content, flags=re.DOTALL)

        # Reemplazar referencias generales de carpetas según el modo
        if use_opencode:
            content = content.replace("/.harness/roles/orchestrator.md", "/.opencode/agents/orchestrator.md")
            content = content.replace("/.opencode/roles/orchestrator.md", "/.opencode/agents/orchestrator.md")
            content = content.replace("/.harness/", "/.opencode/")
            content = content.replace(".harness/", ".opencode/")
        else:
            content = content.replace("/.opencode/agents/orchestrator.md", "/.harness/roles/orchestrator.md")
            content = content.replace("/.opencode/roles/orchestrator.md", "/.harness/roles/orchestrator.md")
            content = content.replace("/.opencode/", "/.harness/")
            content = content.replace(".opencode/", ".harness/")

        with open("AGENTS.md", "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ AGENTS.md actualizado dinámicamente.")
    else:
        print("❌ No se encontró AGENTS.md para sincronizar.")
