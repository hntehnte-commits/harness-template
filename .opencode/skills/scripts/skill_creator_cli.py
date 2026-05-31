# skill_creator_cli.py
"""
skill_creator_cli.py - Script de automatización para la creación de nuevas Habilidades (Skills)
Para uso exclusivo del skill skill-creator.
"""
import os
import re
import sys
import subprocess
import argparse

# Localizar la raíz del workspace de forma dinámica
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", "..", ".."))


def sanitize_skill_name(title):
    """Genera un nombre seguro para el archivo/directorio de la skill a partir del título"""
    return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')


def create_skill(name, description, profile=None, with_assets=False):
    """Crea la estructura del skill y gatilla la recompilación del arnés"""
    # Determinar ruta base del skill
    harness_dir = os.path.join(WORKSPACE_ROOT, ".harness")
    
    # Validar si el perfil existe si se especificó
    if profile:
        profile_skills_dir = os.path.join(harness_dir, "profiles", profile, "skills")
        # Por ahora creamos skills globales en .opencode/skills si no existe el perfil en disco
        target_dir = os.path.join(harness_dir, "skills")
        print(f"[!] Perfiles directos aún no soportan sub-carpetas de skills. Creando skill globalmente.")
    else:
        target_dir = os.path.join(harness_dir, "skills")

    skill_folder_name = sanitize_skill_name(name)
    skill_dir = os.path.join(target_dir, skill_folder_name)
    
    if os.path.exists(skill_dir):
        print(f"[ERR] El skill '{name}' ya existe en {skill_dir}", file=sys.stderr)
        return False

    os.makedirs(skill_dir, exist_ok=True)
    
    # Crear SKILL.md
    skill_file_path = os.path.join(skill_dir, "SKILL.md")
    
    skill_content = f"""# Skill: {name}

## Purpose
{description}

---

## 1. Execution Procedure
1. **Initial Step**: Define the preconditions required for this skill to execute correctly.
2. **Sequential Step**: Describe the workflow in detail, the tools you should use, and the acceptance criteria.

---

## 2. Validation Rules
- **Rule 1**: Describe specific criteria to guarantee the quality and correctness of the result.
- **Rule 2**: Define limitations and exceptions where this skill should not be applied.

---

## 3. Self-Correction and Feedback
- **Detection**: If you encounter an error or inconsistency in the output, describe it here.
- **Resolution**: Explain the automatic correction steps to follow before interacting with the user again.
"""
    
    try:
        with open(skill_file_path, "w", encoding="utf-8") as f:
            f.write(skill_content)
        print(f"[OK] Estructura creada en: .opencode/skills/{skill_folder_name}/SKILL.md")
        
        # Crear sub-carpeta de assets (solo si se solicita)
        if with_assets:
            os.makedirs(os.path.join(skill_dir, "assets"), exist_ok=True)
            print(f"[OK] Carpeta de assets creada.")
        
        # Recompilar arnés
        print(f"[*] Recompilando el arnés para registrar el nuevo skill...")
        run_script = os.path.join(WORKSPACE_ROOT, "adapt_harness.py")
        
        res = subprocess.run(
            [sys.executable, run_script, "opencode"],
            cwd=WORKSPACE_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if res.returncode == 0:
            print(f"[OK] Arnés compilado y catalogado exitosamente.")
            print(f"[OK] El nuevo skill '{name}' ya está disponible en AGENTS.md.")
            return True
        else:
            print(f"[ERR] No se pudo recompilar el arnés: {res.stderr}", file=sys.stderr)
            return False
            
    except Exception as e:
        print(f"[ERR] Error inesperado creando el skill: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="CLI de Creación Rápida de Habilidades (Exclusivo de Skills)")
    parser.add_argument("--name", required=True, help="Nombre legible de la habilidad (ej: 'Git Management')")
    parser.add_argument("--description", required=True, help="Propósito corto y conciso de la habilidad")
    parser.add_argument("--profile", help="Opcional. Perfil específico bajo el cual crear el skill")
    parser.add_argument("--with-assets", action="store_true", help="Crear carpeta de assets para scripts propios del skill")
    
    args = parser.parse_args()
    
    success = create_skill(args.name, args.description, args.profile, args.with_assets)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
