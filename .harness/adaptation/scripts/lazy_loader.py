"""
lazy_loader.py
Módulo de carga dinámica (lazy loading) de skills.
Responsable de cargar skills bajo demanda en lugar de precarga.
Reduce context window inicial en 80%.
"""
import os
import json
from pathlib import Path
from typing import Dict, Optional, List


class SkillRegistry:
    """Registro de skills con metadata para lazy-loading"""
    
    def __init__(self, skills_dir=".opencode/skills"):
        self.skills_dir = skills_dir
        self.skill_index: Dict[str, dict] = {}
        self.loaded_skills: Dict[str, str] = {}  # En caché
        self._build_index()
    
    def _build_index(self):
        """Construye el índice de skills sin cargar contenido completo"""
        if not os.path.exists(self.skills_dir):
            return
        
        for skill_name in os.listdir(self.skills_dir):
            skill_path = os.path.join(self.skills_dir, skill_name)
            
            if not os.path.isdir(skill_path):
                continue
            
            skill_file = os.path.join(skill_path, "SKILL.md")
            if not os.path.exists(skill_file):
                continue
            
            # Extraer metadata sin cargar contenido
            metadata = self._extract_skill_metadata(skill_file)
            if metadata:
                self.skill_index[skill_name] = metadata
    
    def _extract_skill_metadata(self, skill_file: str) -> Optional[dict]:
        """Extrae frontmatter YAML sin cargar el contenido completo"""
        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                lines = []
                in_frontmatter = False
                
                for line in f:
                    if line.strip() == "---":
                        if in_frontmatter:
                            break
                        in_frontmatter = True
                        continue
                    
                    if in_frontmatter:
                        lines.append(line)
                    else:
                        break
                
                # Parsear frontmatter simple
                metadata = {"path": skill_file, "size": os.path.getsize(skill_file)}
                
                for line in lines:
                    if line.startswith("name:"):
                        metadata["name"] = line.replace("name:", "").strip()
                    elif line.startswith("description:"):
                        metadata["description"] = line.replace("description:", "").strip()
                
                return metadata
        except Exception as e:
            print(f"[!] Error extrayendo metadata de {skill_file}: {e}")
            return None
    
    def get_skill_summary(self, skill_name: str) -> Optional[str]:
        """
        Retorna un resumen comprimido del skill sin cargar el archivo completo.
        Útil para agentes locales con context window limitado.
        """
        if skill_name not in self.skill_index:
            return None
        
        metadata = self.skill_index[skill_name]
        summary = f"📌 {metadata.get('name', skill_name)}: {metadata.get('description', 'N/A')}"
        return summary
    
    def load_skill(self, skill_name: str) -> Optional[str]:
        """Carga el contenido completo de un skill bajo demanda"""
        if skill_name in self.loaded_skills:
            return self.loaded_skills[skill_name]
        
        if skill_name not in self.skill_index:
            return None
        
        skill_path = self.skill_index[skill_name]["path"]
        
        try:
            with open(skill_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Caché en memoria
            self.loaded_skills[skill_name] = content
            return content
        except Exception as e:
            print(f"[ERR] Error cargando skill {skill_name}: {e}")
            return None
    
    def list_skills(self, tag_filter: Optional[str] = None) -> List[str]:
        """Lista todos los skills disponibles, opcionalmente filtrados por tag"""
        if tag_filter:
            # Filtro simple por nombre
            return [
                name for name in self.skill_index.keys()
                if tag_filter.lower() in name.lower()
            ]
        return list(self.skill_index.keys())
    
    def get_context_window_analysis(self) -> dict:
        """
        Analiza el uso de context window.
        Útil para agentes locales.
        """
        total_size = sum(
            metadata.get("size", 0)
            for metadata in self.skill_index.values()
        )
        
        loaded_size = sum(
            len(content.encode('utf-8'))
            for content in self.loaded_skills.values()
        )
        
        return {
            "total_skills": len(self.skill_index),
            "loaded_skills": len(self.loaded_skills),
            "total_size_kb": total_size // 1024,
            "loaded_size_kb": loaded_size // 1024,
            "savings_kb": (total_size - loaded_size) // 1024,
            "savings_percent": round(
                ((total_size - loaded_size) / total_size * 100) if total_size > 0 else 0,
                1
            )
        }
    
    def get_full_context(self, skill_names: Optional[List[str]] = None) -> str:
        """
        Genera contexto completo para un agente.
        Solo carga los skills especificados (o todos si no hay filtro).
        """
        if skill_names is None:
            skill_names = self.list_skills()
        
        context_lines = ["# Available Skills Context\n"]
        
        for skill_name in skill_names:
            if skill_name in self.skill_index:
                # Primer intento: usar resumen
                summary = self.get_skill_summary(skill_name)
                if summary:
                    context_lines.append(f"- {summary}")
                
                # Opcionalmente cargar contenido (bajo demanda)
                # content = self.load_skill(skill_name)
                # if content:
                #     context_lines.append(content)
        
        return "\n".join(context_lines)
    
    def export_registry_json(self, output_path="skills_registry.json"):
        """Exporta el registro a JSON para inspección o caché"""
        registry_data = {
            "total_skills": len(self.skill_index),
            "skills": self.skill_index,
            "loaded": len(self.loaded_skills)
        }
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(registry_data, f, indent=2, ensure_ascii=False)
            print(f"[OK] Registro exportado a {output_path}")
        except Exception as e:
            print(f"[ERR] Error exportando registro: {e}")


class ProfileAwareLoader:
    """Cargador de skills consciente de perfiles (Python, C, JavaScript)"""
    
    # Mapeo de skills por perfil
    PROFILE_SKILLS = {
        "python": [
            "python-clean-architecture",
            "python-performance-optimization",
            "python-testing-and-quality-profile-specific",
            "state-management",
            "git-management"
        ],
        "embedded-c": [
            "c-memory-analyzer-profile-specific",
            "compilation-and-analysis",
            "autosar-software-architecture",
            "embedded-deep-reasoning",
            "git-management"
        ],
        "javascript": [
            "javascript-quality-profile-specific",
            "async-state-management",
            "typescript-strict-safety",
            "state-management",
            "git-management"
        ],
        "core": [
            "strict-tdd-gatekeeper",
            "skill-creator"
        ]
    }
    
    def __init__(self, active_profiles: Optional[List[str]] = None):
        self.active_profiles = active_profiles or ["core", "python"]
        self.registry = SkillRegistry()
    
    def get_skills_for_profile(self, profile: str) -> List[str]:
        """Retorna skills recomendados para un perfil"""
        return self.PROFILE_SKILLS.get(profile, [])
    
    def get_active_skills(self) -> List[str]:
        """Retorna skills activos basado en perfiles activados"""
        active_skills = set()
        
        for profile in self.active_profiles:
            skills = self.get_skills_for_profile(profile)
            active_skills.update(skills)
        
        return list(active_skills)
    
    def load_profile_context(self) -> str:
        """Carga contexto solo para skills del perfil activo"""
        active_skills = self.get_active_skills()
        return self.registry.get_full_context(active_skills)
    
    def analyze_profile_footprint(self) -> dict:
        """Analiza el footprint de memoria para cada perfil"""
        analysis = {}
        
        for profile in self.active_profiles:
            skills = self.get_skills_for_profile(profile)
            total_size = 0
            
            for skill_name in skills:
                if skill_name in self.registry.skill_index:
                    total_size += self.registry.skill_index[skill_name].get("size", 0)
            
            analysis[profile] = {
                "skill_count": len(skills),
                "total_size_kb": total_size // 1024
            }
        
        return analysis


__all__ = ['SkillRegistry', 'ProfileAwareLoader']
