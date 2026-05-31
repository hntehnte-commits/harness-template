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


def create_skill(name, description, profile=None):
    """Crea la estructura del skill y gatilla la recompilación del arnés"""
    # Determinar ruta base del skill
    harness_dir = os.path.join(WORKSPACE_ROOT, ".harness")
    
    # Validar si el perfil existe si se especificó
    if profile:
        profile_skills_dir = os.path.join(harness_dir, "profiles", profile, "skills")
        # Por ahora creamos skills globales en .harness/skills si no existe el perfil en disco
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

## 1. Procedimiento de Ejecución
1. **Paso Inicial**: Define las precondiciones necesarias para que esta habilidad se ejecute correctamente.
2. **Paso Secuencial**: Describe detalladamente el flujo de trabajo, las herramientas que debes usar y los criterios de aceptación.

---

## 2. Reglas de Validación
* **Regla 1**: Describe criterios específicos que garanticen la calidad y exactitud del resultado.
* **Regla 2**: Define límites y excepciones donde esta habilidad no deba ser aplicada.

---

## 3. Auto-Corrección y Feedback
* **Detección**: Si encuentras un error o inconsistencia en la salida, descríbelo aquí.
* **Resolución**: Explica los pasos automáticos de corrección que debes seguir antes de interactuar de nuevo con el usuario.
"""
    
    try:
        with open(skill_file_path, "w", encoding="utf-8") as f:
            f.write(skill_content)
        print(f"[OK] Estructura creada en: .harness/skills/{skill_folder_name}/SKILL.md")
        
        # Crear sub-carpeta de assets
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
    
    args = parser.parse_args()
    
    success = create_skill(args.name, args.description, args.profile)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
