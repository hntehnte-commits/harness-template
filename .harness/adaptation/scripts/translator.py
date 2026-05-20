# translator.py
import re
from constants import REPLACEMENTS

def get_frontmatter(title, desc, is_skill=False, is_primary=False):
    """Genera el Frontmatter YAML nativo de OpenCode"""
    if is_skill:
        safe_name = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        return f"---\nname: {safe_name}\ndescription: {desc}\n---\n"
    else:
        mode = "primary" if is_primary else "subagent"
        return f"---\ndescription: {desc}\nmode: {mode}\n---\n"

def extract_metadata(filepath):
    """Extrae el título y una descripción corta del Markdown del Arnés"""
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

def translate_and_write(src_path, dest_path):
    """Traduce referencias de .harness a .opencode y escribe el archivo resultante"""
    with open(src_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    for k, v in REPLACEMENTS.items():
        content = content.replace(k, v)
        
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(content)
