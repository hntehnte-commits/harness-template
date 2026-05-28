"""
path_translator.py
Módulo de traducción de rutas y metadatos.
Responsable de extraer metadatos, generar frontmatter y aplicar traducciones de referencias.
"""
import re
from pathlib import Path


# Diccionario de reemplazos de rutas (centralizado)
REPLACEMENTS = {
    "/.harness/roles/orchestrator.md": "/.opencode/agents/orchestrator.md",
    "/.harness/roles/spec_agent.md": "/.opencode/agents/spec.md",
    "/.harness/roles/developer_agent.md": "/.opencode/agents/developer.md",
    "/.harness/roles/dev_agent.md": "/.opencode/agents/dev.md",
    "/.harness/roles/qa_agent.md": "/.opencode/agents/qa.md",
    "/.harness/roles/python_developer_agent.md": "/.opencode/agents/python-developer.md",
    "/.harness/roles/embedded_developer_agent.md": "/.opencode/agents/embedded-developer.md",
    "/.harness/roles/javascript_developer_agent.md": "/.opencode/agents/javascript-developer.md",
    "/.harness/roles/docs_agent.md": "/.opencode/agents/docs.md",
    "/.harness/skills/state_management.md": "/.opencode/skills/state-management/SKILL.md",
    "/.harness/skills/tdd_gatekeeper.md": "/.opencode/skills/strict-tdd-gatekeeper/SKILL.md",
    "/.harness/": "/.opencode/",
    ".harness/": ".opencode/"
}


def get_frontmatter(title, desc, is_skill=False, is_primary=False):
    """
    Genera el Frontmatter YAML nativo de OpenCode.
    
    Args:
        title: Título del componente
        desc: Descripción corta
        is_skill: Si es True, genera frontmatter para skill
        is_primary: Si es True, establece modo 'primary' para agentes
    
    Returns:
        String con el frontmatter YAML
    """
    if is_skill:
        safe_name = _sanitize_name(title)
        return f"---\nname: {safe_name}\ndescription: {desc}\n---\n"
    else:
        mode = "primary" if is_primary else "subagent"
        return f"---\ndescription: {desc}\nmode: {mode}\n---\n"


def extract_metadata(filepath):
    """
    Extrae el título, descripción y contenido de un archivo Markdown del Harness.
    
    Args:
        filepath: Ruta del archivo
    
    Returns:
        Tupla (title, description, content)
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Extrae título de la primera línea
    title = lines[0].replace("# Role: ", "").replace("# Skill: ", "").strip()
    if not title:
        title = Path(filepath).stem
    
    # Busca descripción en las primeras líneas de contenido real
    desc = "Harness component"
    for line in lines[1:]:
        if line.strip() and not line.startswith("#"):
            # Extraer descripción completa, buscando primera frase o límite razonable
            desc = line.strip()
            
            # Si hay punto, truncar ahí (fin de frase natural)
            if '.' in desc:
                desc = desc[:desc.index('.') + 1]
            # Si no hay punto pero es muy largo (>250 chars), limitar
            elif len(desc) > 250:
                desc = desc[:250] + "..."
            break
    
    return title, desc, content


def apply_replacements(content):
    """
    Aplica todas las traducciones de referencias de .harness a .opencode.
    
    Args:
        content: Contenido del archivo
    
    Returns:
        Contenido con traducciones aplicadas
    """
    for k, v in REPLACEMENTS.items():
        content = content.replace(k, v)
    return content


def translate_and_write(src_path, dest_path):
    """
    Lee un archivo, aplica traducciones y escribe el resultado.
    
    Args:
        src_path: Ruta origen
        dest_path: Ruta destino
    """
    with open(src_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    content = apply_replacements(content)
    
    # Crear directorio destino si no existe
    Path(dest_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(content)


def _sanitize_name(title):
    """Genera un nombre seguro para skill a partir del título"""
    return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')


# Exportar constantes
__all__ = ['get_frontmatter', 'extract_metadata', 'apply_replacements', 
           'translate_and_write', 'REPLACEMENTS']
