"""
benchmark_context.py
Mide el uso de context window antes/después de lazy-loading.
Compara el footprint de skills cargados vs. disponibles.
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../.opencode/core'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../.harness/adaptation/scripts'))

from lazy_loader import SkillRegistry, ProfileAwareLoader


def measure_skill_footprint():
    """Mide el footprint total de skills sin lazy-loading"""
    print("\n[BENCHMARK] Footprint de Skills")
    print("=" * 50)

    # Sin lazy-loading: asumir que todos los skills se cargan
    skills_dir = os.path.join(os.path.dirname(__file__), '../.opencode/skills')
    total_size = 0
    skill_count = 0

    if os.path.exists(skills_dir):
        for skill_name in os.listdir(skills_dir):
            skill_path = os.path.join(skills_dir, skill_name, "SKILL.md")
            if os.path.exists(skill_path):
                total_size += os.path.getsize(skill_path)
                skill_count += 1

    print(f"   Skills totales: {skill_count}")
    print(f"   Tamaño total:   {total_size // 1024} KB ({total_size} bytes)")
    return {"skill_count": skill_count, "total_size_bytes": total_size}


def measure_lazy_footprint():
    """Mide el footprint con lazy-loading (solo metadata)"""
    print("\n[BENCHMARK] Footprint con Lazy-Loading")
    print("=" * 50)

    registry = SkillRegistry(
        skills_dir=os.path.join(os.path.dirname(__file__), '../.opencode/skills')
    )
    analysis = registry.get_context_window_analysis()

    print(f"   Skills indexados: {analysis['total_skills']}")
    print(f"   Skills cargados:  {analysis['loaded_skills']}")
    print(f"   Tamaño total:     {analysis['total_size_kb']} KB")
    print(f"   Tamaño cargado:   {analysis['loaded_size_kb']} KB")
    print(f"   Ahorro:           {analysis['savings_kb']} KB ({analysis['savings_percent']}%)")
    return analysis


def measure_profile_footprint():
    """Mide el footprint por perfil activo"""
    print("\n[BENCHMARK] Footprint por Perfil")
    print("=" * 50)

    loader = ProfileAwareLoader(active_profiles=["core", "python"])
    analysis = loader.analyze_profile_footprint()

    for profile, data in analysis.items():
        print(f"   Perfil '{profile}': {data['skill_count']} skills, {data['total_size_kb']} KB")
    return analysis


def run_benchmarks():
    """Ejecuta todos los benchmarks y retorna resultados"""
    print("[*] INICIANDO BENCHMARKS DE CONTEXT WINDOW")
    print("=" * 50)

    before = time.time()

    results = {
        "full_footprint": measure_skill_footprint(),
        "lazy_footprint": measure_lazy_footprint(),
        "profile_footprint": measure_profile_footprint(),
    }

    elapsed = time.time() - before
    print(f"\n[TIME] Tiempo total: {elapsed:.3f}s")
    print("=" * 50)

    if results["full_footprint"].get("total_size_bytes", 0) > 0:
        savings = results["lazy_footprint"].get("savings_percent", 0)
        print(f"\n[RESULT] {savings}% de ahorro en context window")
    else:
        print("\n[RESULT] No hay skills para comparar (ejecuta compilacion primero)")

    return results


if __name__ == "__main__":
    run_benchmarks()
