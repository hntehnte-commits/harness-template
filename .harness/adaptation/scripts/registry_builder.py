"""
registry_builder.py
Módulo de construcción y sincronización del registry.
Responsable de escanear agentes/skills y actualizar AGENTS.md automáticamente.
"""
import os
import re
from pathlib import Path


class RegistryBuilder:
    """Constructor del registry y sincronizador de AGENTS.md"""
    
    def __init__(self, harness_dir=".harness", opencode_dir=".opencode"):
        self.harness_dir = harness_dir
        self.opencode_dir = opencode_dir
        self.agents = {}
        self.skills = {}
        self.config = {}
    
    def scan_agents(self, use_opencode=True):
        """
        Escanea y carga todos los agentes disponibles.
        
        Args:
            use_opencode: Si True, escanea .opencode/agents, sino .harness/roles
        
        Returns:
            Dict con agentes encontrados
        """
        agents_dir = os.path.join(
            self.opencode_dir if use_opencode else self.harness_dir,
            "agents" if use_opencode else "roles"
        )
        
        if not os.path.exists(agents_dir):
            return self.agents
        
        for filename in sorted(os.listdir(agents_dir)):
            if not filename.endswith(".md"):
                continue
            
            filepath = os.path.join(agents_dir, filename)
            title = self._extract_first_heading(filepath)
            if not title:
                title = filename.replace(".md", "")
            
            base_path = f"/.opencode/agents" if use_opencode else f"/.harness/roles"
            self.agents[title] = f"{base_path}/{filename}"
        
        return self.agents
    
    def scan_skills(self, use_opencode=True):
        """
        Escanea y carga todas las habilidades disponibles.
        
        Args:
            use_opencode: Si True, escanea .opencode/skills, sino .harness/skills
        
        Returns:
            Dict con skills encontrados
        """
        skills_dir = os.path.join(
            self.opencode_dir if use_opencode else self.harness_dir,
            "skills"
        )
        
        if not os.path.exists(skills_dir):
            return self.skills
        
        for skill_item in sorted(os.listdir(skills_dir)):
            skill_path = os.path.join(skills_dir, skill_item)
            
            # Caso: Directorio con SKILL.md
            if os.path.isdir(skill_path):
                skill_md_path = os.path.join(skill_path, "SKILL.md")
                if os.path.exists(skill_md_path):
                    title = self._extract_first_heading(skill_md_path)
                    if not title:
                        title = skill_item
                    
                    base_path = f"/.opencode/skills/{skill_item}" if use_opencode else f"/.harness/skills/{skill_item}"
                    self.skills[title] = f"{base_path}/SKILL.md"
            
            # Caso: Archivo .md individual
            elif skill_item.endswith(".md"):
                title = self._extract_first_heading(skill_path)
                if not title:
                    title = skill_item.replace(".md", "")
                
                base_path = f"/.opencode/skills" if use_opencode else f"/.harness/skills"
                self.skills[title] = f"{base_path}/{skill_item}"
        
        return self.skills
    
    def load_config(self, use_opencode=True):
        """
        Carga la configuración del proyecto desde config.yaml.
        
        Args:
            use_opencode: Si True, lee .opencode/config.yaml, sino .harness/config.yaml
        
        Returns:
            Dict con valores de configuración
        """
        config_path = os.path.join(
            self.opencode_dir if use_opencode else self.harness_dir,
            "config.yaml"
        )
        
        if not os.path.exists(config_path):
            return self.config
        
        with open(config_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Parse YAML simple (sin librerías externas)
        def extract_yaml_prop(prop_name, yaml_content):
            match = re.search(rf'{prop_name}:\s*(.*?)\s*(?:#|$)', yaml_content, re.MULTILINE)
            if not match:
                return None
            val = match.group(1).strip()
            # Remover comillas si existen
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1].strip()
            return val
        
        self.config = {
            "name": extract_yaml_prop("name", content) or "My AI Harnessed Project",
            "stack": extract_yaml_prop("stack", content) or "python",
            "test_command": extract_yaml_prop("test_command", content) or "pytest",
            "lint_command": extract_yaml_prop("lint_command", content) or "flake8",
        }
        
        return self.config
    
    def build_agents_section(self):
        """Construye la sección de agentes para AGENTS.md"""
        if not self.agents:
            return ""
        
        lines = ["### Available Sub-Agents (Roles)"]
        for title, path in sorted(self.agents.items()):
            lines.append(f"- **{title}** (`{path}`)")
        
        return "\n".join(lines) + "\n"
    
    def build_skills_section(self):
        """Construye la sección de skills para AGENTS.md"""
        if not self.skills:
            return ""
        
        lines = ["### Available Skills"]
        for title, path in sorted(self.skills.items()):
            lines.append(f"- **{title}** (`{path}`)")
        
        return "\n".join(lines) + "\n"
    
    def build_project_info_section(self):
        """Construye la sección de información del proyecto"""
        cfg = self.config or {}
        lines = ["## 1. Project Information"]
        
        lines.append(f"- **Project Name**: {cfg.get('name', 'My AI Harnessed Project')}")
        lines.append(f"- **Active Profile / Stack**: {cfg.get('stack', 'python')}")
        lines.append(f"- **Test Command**: `{cfg.get('test_command', 'pytest')}`")
        lines.append(f"- **Lint Command**: `{cfg.get('lint_command', 'flake8')}`")
        lines.append("- **Source Code Location**: `/src/` (Asegúrate de cambiar esto a tu carpeta real de código)")
        lines.append("- **Tests Location**: `/tests/` (Asegúrate de cambiar esto a tu carpeta real de tests)")
        
        return "\n".join(lines) + "\n"
    
    def sync_agents_md(self, agents_md_path="AGENTS.md", use_opencode=True):
        """
        Sincroniza el archivo AGENTS.md con el estado actual de agentes y skills.
        
        Args:
            agents_md_path: Ruta del archivo AGENTS.md
            use_opencode: Si True, usa paths de .opencode, sino .harness
        """
        if not os.path.exists(agents_md_path):
            print(f"❌ No se encontró {agents_md_path}")
            return False
        
        # Escanear y construir
        self.scan_agents(use_opencode=use_opencode)
        self.scan_skills(use_opencode=use_opencode)
        self.load_config(use_opencode=use_opencode)
        
        with open(agents_md_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Actualizar sección de información del proyecto
        project_info = self.build_project_info_section()
        content = re.sub(
            r'## 1\. Project Information\n.*?(?=\n##|\Z)',
            project_info,
            content,
            flags=re.DOTALL
        )
        
        # Actualizar sección de agentes
        agents_section = self.build_agents_section()
        content = re.sub(
            r'### Available Sub-Agents \(Roles\)\n.*?(?=\n###|\n##|\Z)',
            agents_section,
            content,
            flags=re.DOTALL
        )
        
        # Actualizar sección de skills
        skills_section = self.build_skills_section()
        if "### Available Skills" in content:
            content = re.sub(
                r'### Available Skills\n.*?(?=\n##|\Z)',
                skills_section,
                content,
                flags=re.DOTALL
            )
        else:
            content += "\n" + skills_section
        
        # Actualizar referencias de rutas si es necesario
        if use_opencode:
            content = content.replace("/.harness/roles/orchestrator.md", "/.opencode/agents/orchestrator.md")
            content = content.replace(".harness/", ".opencode/")
        else:
            content = content.replace("/.opencode/agents/orchestrator.md", "/.harness/roles/orchestrator.md")
            content = content.replace(".opencode/", ".harness/")
        
        with open(agents_md_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"✅ AGENTS.md sincronizado:")
        print(f"   + {len(self.agents)} agentes")
        print(f"   + {len(self.skills)} skills")
        
        return True
    
    @staticmethod
    def _extract_first_heading(filepath):
        """Extrae el primer heading de un archivo Markdown"""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("# "):
                        return line.replace("# Role: ", "").replace("# Skill: ", "").replace("# ", "").strip()
        except:
            pass
        return None
