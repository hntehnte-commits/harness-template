"""
transpiler_core.py
Módulo de lógica principal de transpilación del Harness.
Responsable de compilar agentes, skills, memoria y artefactos.
"""
import os
import shutil
import sys
from pathlib import Path

from path_translator import extract_metadata, get_frontmatter, translate_and_write, apply_replacements


class TranspilerCore:
    """Compilador principal del Harness a formato OpenCode"""
    
    def __init__(self, base_dir="."):
        self.base_dir = base_dir
        self.harness_dir = os.path.join(base_dir, ".harness")
        self.opencode_dir = os.path.join(base_dir, ".opencode")
        self.compiled_items = {
            "agents": 0,
            "skills": 0,
            "memory": 0,
            "artifacts": 0,
            "config": 0
        }
        
    def setup_directories(self):
        """Crea la estructura de directorios necesaria en .opencode/"""
        dirs = [
            "agents",
            "skills",
            "memory",
            "artifacts/templates",
            "artifacts/current_run"
        ]
        for d in dirs:
            os.makedirs(os.path.join(self.opencode_dir, d), exist_ok=True)
    
    def compile_agents(self):
        """Transpila todos los agentes (roles) desde .harness/roles a .opencode/agents"""
        roles_dir = os.path.join(self.harness_dir, "roles")
        if not os.path.exists(roles_dir):
            print("  ⚠️  No se encontró directorio .harness/roles")
            return
        
        for filename in os.listdir(roles_dir):
            if not filename.endswith(".md"):
                continue
            
            filepath = os.path.join(roles_dir, filename)
            title, desc, content = extract_metadata(filepath)
            is_primary = (filename == "orchestrator.md")
            frontmatter = get_frontmatter(title, desc, is_skill=False, is_primary=is_primary)
            
            # Aplicar traducciones de referencias
            content = apply_replacements(content)
            
            # Generar nombre del agente (ej: developer_agent.md -> developer.md)
            agent_name = filename.replace("_agent", "").replace("_", "-")
            dest_path = os.path.join(self.opencode_dir, "agents", agent_name)
            
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(frontmatter + "\n" + content)
            
            self.compiled_items["agents"] += 1
            print(f"  + Agente transpilado: .opencode/agents/{agent_name}")
    
    def compile_skills(self):
        """Transpila todas las habilidades desde .harness/skills a .opencode/skills"""
        skills_dir = os.path.join(self.harness_dir, "skills")
        if not os.path.exists(skills_dir):
            print("  ⚠️  No se encontró directorio .harness/skills")
            return
        
        for filename in os.listdir(skills_dir):
            filepath = os.path.join(skills_dir, filename)
            
            # Caso 1: Directorio con SKILL.md
            if os.path.isdir(filepath):
                skill_md_path = os.path.join(filepath, "SKILL.md")
                if not os.path.exists(skill_md_path):
                    skill_md_path = os.path.join(filepath, f"{filename}.md")
                
                if not os.path.exists(skill_md_path):
                    continue
                
                title, desc, content = extract_metadata(skill_md_path)
                content = apply_replacements(content)
                
                # Generar nombre de skill seguro
                skill_name = self._sanitize_skill_name(title)
                skill_dir = os.path.join(self.opencode_dir, "skills", skill_name)
                os.makedirs(skill_dir, exist_ok=True)
                
                frontmatter = get_frontmatter(title, desc, is_skill=True)
                with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
                    f.write(frontmatter + "\n" + content)
                
                # Copiar archivos adicionales (assets, etc.)
                self._copy_skill_assets(filepath, skill_dir, [skill_md_path])
                
                self.compiled_items["skills"] += 1
                print(f"  + Skill transpilada (dir): .opencode/skills/{skill_name}/SKILL.md")
            
            # Caso 2: Archivo .md individual
            elif filename.endswith(".md"):
                title, desc, content = extract_metadata(filepath)
                content = apply_replacements(content)
                
                skill_name = self._sanitize_skill_name(title)
                skill_dir = os.path.join(self.opencode_dir, "skills", skill_name)
                os.makedirs(skill_dir, exist_ok=True)
                
                frontmatter = get_frontmatter(title, desc, is_skill=True)
                with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
                    f.write(frontmatter + "\n" + content)
                
                self.compiled_items["skills"] += 1
                print(f"  + Skill transpilada: .opencode/skills/{skill_name}/SKILL.md")
    
    def compile_memory(self):
        """Copia archivos de memoria desde .harness/memory a .opencode/memory"""
        memory_dir = os.path.join(self.harness_dir, "memory")
        if not os.path.exists(memory_dir):
            print("  ⚠️  No se encontró directorio .harness/memory")
            return
        
        for filename in os.listdir(memory_dir):
            if not filename.endswith(".md"):
                continue
            
            src = os.path.join(memory_dir, filename)
            dest = os.path.join(self.opencode_dir, "memory", filename)
            translate_and_write(src, dest)
            
            self.compiled_items["memory"] += 1
            print(f"  + Memoria copiada: .opencode/memory/{filename}")
    
    def compile_artifacts(self):
        """Copia plantillas de artefactos desde .harness/artifacts/templates"""
        templates_dir = os.path.join(self.harness_dir, "artifacts", "templates")
        if not os.path.exists(templates_dir):
            print("  ⚠️  No se encontró directorio .harness/artifacts/templates")
            return
        
        for filename in os.listdir(templates_dir):
            if not filename.endswith((".yaml", ".yml", ".md")):
                continue
            
            src = os.path.join(templates_dir, filename)
            dest = os.path.join(self.opencode_dir, "artifacts", "templates", filename)
            translate_and_write(src, dest)
            
            self.compiled_items["artifacts"] += 1
            print(f"  + Plantilla copiada: .opencode/artifacts/templates/{filename}")
    
    def compile_config(self):
        """Copia y traduce el archivo de configuración"""
        src = os.path.join(self.harness_dir, "config.yaml")
        dest = os.path.join(self.opencode_dir, "config.yaml")
        
        if os.path.exists(src):
            translate_and_write(src, dest)
            self.compiled_items["config"] += 1
            print(f"  + Configuración copiada: .opencode/config.yaml")
    
    def write_instructions(self, pointer_text):
        """Escribe el archivo de instrucciones del harness"""
        dest = os.path.join(self.opencode_dir, "instructions.md")
        with open(dest, "w", encoding="utf-8") as f:
            f.write(pointer_text)
        print(f"  + Instrucciones generadas: .opencode/instructions.md")
    
    def compile_all(self, pointer_text):
        """Ejecuta la compilación completa del harness"""
        print("⚙️  Compilando Arnés a formato nativo de OpenCode...\n")
        
        # Limpiar si existe
        if os.path.exists(self.opencode_dir):
            shutil.rmtree(self.opencode_dir, ignore_errors=True)
        
        # Crear estructura
        self.setup_directories()
        
        # Compilar componentes
        self.compile_agents()
        self.compile_skills()
        self.compile_memory()
        self.compile_artifacts()
        self.compile_config()
        self.write_instructions(pointer_text)
        
        # Resumen
        print(f"\n✅ Compilación exitosa:")
        print(f"   + {self.compiled_items['agents']} agentes")
        print(f"   + {self.compiled_items['skills']} skills")
        print(f"   + {self.compiled_items['memory']} archivos de memoria")
        print(f"   + {self.compiled_items['artifacts']} plantillas de artefactos")
        print(f"   + 1 configuración")
    
    @staticmethod
    def _sanitize_skill_name(title):
        """Genera un nombre seguro para skill a partir del título"""
        import re
        return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    
    @staticmethod
    def _copy_skill_assets(src_dir, dest_dir, exclude_files):
        """Copia archivos adicionales (assets) desde skill source"""
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                src_file = os.path.join(root, file)
                if src_file in exclude_files:
                    continue
                
                rel_path = os.path.relpath(src_file, src_dir)
                dest_file = os.path.join(dest_dir, rel_path)
                os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                shutil.copy2(src_file, dest_file)
                print(f"    + Asset copiado: {rel_path}")
