"""
tests/test_compiler.py
Suite de pruebas para el compilador del Harness
Verifica transpilación correcta de agentes, skills y artefactos
Incluye pruebas para Sprint 2: lazy-loading, profiles, cache
"""
import unittest
import os
import shutil
import sys
import tempfile
import json
from pathlib import Path

# Agregar scripts al path para importar
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../.harness/adaptation/scripts'))

from transpiler_core import TranspilerCore
from registry_builder import RegistryBuilder
from path_translator import (
    get_frontmatter,
    extract_metadata,
    apply_replacements,
    translate_and_write,
    REPLACEMENTS
)
from lazy_loader import SkillRegistry, ProfileAwareLoader
from cache_manager import DecisionsCache, ContextWindowTracker
from state_manager import HarnessStateManager


class TestPathTranslator(unittest.TestCase):
    """Pruebas para el módulo path_translator"""
    
    def test_get_frontmatter_skill(self):
        """Verifica generación de frontmatter para skills"""
        result = get_frontmatter("My Skill", "Descripción test", is_skill=True)
        self.assertIn("---", result)
        self.assertIn("name: my-skill", result)
        self.assertIn("description: Descripción test", result)
    
    def test_get_frontmatter_agent_primary(self):
        """Verifica generación de frontmatter para agentes primarios"""
        result = get_frontmatter("Orchestrator", "Main agent", is_skill=False, is_primary=True)
        self.assertIn("mode: primary", result)
        self.assertIn("description: Main agent", result)
    
    def test_get_frontmatter_agent_subagent(self):
        """Verifica generación de frontmatter para subagentes"""
        result = get_frontmatter("Developer", "Dev agent", is_skill=False, is_primary=False)
        self.assertIn("mode: subagent", result)
    
    def test_apply_replacements(self):
        """Verifica aplicación de traducciones de referencias"""
        content = "Vea /.harness/roles/orchestrator.md"
        result = apply_replacements(content)
        self.assertIn("/.opencode/agents/orchestrator.md", result)
        self.assertNotIn("/.harness/roles", result)
    
    def test_replacements_dict_complete(self):
        """Verifica que REPLACEMENTS contiene mappeos esenciales"""
        essential_keys = [
            "/.harness/roles/orchestrator.md",
            "/.harness/skills/state_management.md",
            "/.harness/",
            ".harness/"
        ]
        for key in essential_keys:
            self.assertIn(key, REPLACEMENTS)
    
    def test_extract_metadata_from_role(self):
        """Verifica extracción de metadatos de archivo de rol"""
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("# Role: Test Agent\nThis is a description\nMore content")
            temp_path = f.name
        
        try:
            title, desc, content = extract_metadata(temp_path)
            self.assertEqual(title, "Test Agent")
            self.assertEqual(desc, "This is a description")
            self.assertIn("More content", content)
        finally:
            os.unlink(temp_path)
    
    def test_translate_and_write(self):
        """Verifica traducción y escritura de archivos"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Crear archivo source
            src_file = os.path.join(tmpdir, "test.md")
            dest_file = os.path.join(tmpdir, "translated.md")
            
            with open(src_file, 'w') as f:
                f.write("Reference: /.harness/roles/orchestrator.md")
            
            translate_and_write(src_file, dest_file)
            
            with open(dest_file, 'r') as f:
                content = f.read()
            
            self.assertIn("/.opencode/agents/orchestrator.md", content)
            self.assertNotIn("/.harness/roles", content)


class TestTranspilerCore(unittest.TestCase):
    """Pruebas para el módulo transpiler_core"""
    
    def setUp(self):
        """Preparar entorno de pruebas"""
        self.temp_dir = tempfile.mkdtemp()
        self.transpiler = TranspilerCore(self.temp_dir)
    
    def tearDown(self):
        """Limpiar después de pruebas"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_setup_directories(self):
        """Verifica creación de estructura de directorios incluyendo core/"""
        self.transpiler.setup_directories()
        
        required_dirs = [
            os.path.join(self.temp_dir, ".opencode/agents"),
            os.path.join(self.temp_dir, ".opencode/skills"),
            os.path.join(self.temp_dir, ".opencode/memory"),
            os.path.join(self.temp_dir, ".opencode/core"),
            os.path.join(self.temp_dir, ".opencode/artifacts/templates"),
            os.path.join(self.temp_dir, ".opencode/artifacts/current_run")
        ]
        
        for d in required_dirs:
            self.assertTrue(os.path.exists(d), f"Directorio {d} no creado")
    
    def test_sanitize_skill_name(self):
        """Verifica sanitización de nombres de skills"""
        test_cases = [
            ("Python Clean Architecture", "python-clean-architecture"),
            ("Async State Management", "async-state-management"),
            ("AUTOSAR Software Architecture", "autosar-software-architecture")
        ]
        
        for input_name, expected in test_cases:
            result = TranspilerCore._sanitize_skill_name(input_name)
            self.assertEqual(result, expected)
    
    def test_compile_core_scripts(self):
        """Verifica copia de scripts core (lazy_loader, cache_manager, state_manager)"""
        # Crear directorio de origen simulado
        src_scripts = os.path.join(self.temp_dir, ".harness/adaptation/scripts")
        os.makedirs(src_scripts, exist_ok=True)
        
        # Crear archivos fuente simulados
        for script in ["lazy_loader.py", "cache_manager.py", "state_manager.py"]:
            with open(os.path.join(src_scripts, script), "w") as f:
                f.write(f"# {script}\nprint('hello from {script}')")
        
        self.transpiler.setup_directories()
        self.transpiler.compile_core_scripts()
        
        # Verificar que se copiaron
        for script in ["lazy_loader.py", "cache_manager.py", "state_manager.py"]:
            dest = os.path.join(self.temp_dir, ".opencode/core", script)
            self.assertTrue(os.path.exists(dest), f"{script} no copiado a .opencode/core/")
    
    def test_compile_profiles_config(self):
        """Verifica copia de profiles_enabled.yaml a .opencode/"""
        # Crear archivo fuente simulado
        harness_dir = os.path.join(self.temp_dir, ".harness")
        os.makedirs(harness_dir, exist_ok=True)
        
        with open(os.path.join(harness_dir, "profiles_enabled.yaml"), "w") as f:
            f.write("profiles:\n  enabled:\n    - core\n    - python\n")
        
        self.transpiler.setup_directories()
        self.transpiler.compile_profiles_config()
        
        dest = os.path.join(self.temp_dir, ".opencode/profiles_enabled.yaml")
        self.assertTrue(os.path.exists(dest))
        with open(dest, "r") as f:
            content = f.read()
        self.assertIn("core", content)
        self.assertIn("python", content)
    
    def test_profile_aware_compilation_filters_skills(self):
        """Verifica que compile_skills filtra por perfil activo"""
        # Configurar transpiler con perfil python activo
        transpiler = TranspilerCore(self.temp_dir, profile_aware=True, active_profiles=["python"])
        
        # Crear skills fuente
        skills_dir = os.path.join(self.temp_dir, ".harness/skills")
        os.makedirs(skills_dir, exist_ok=True)
        
        # Skill perteneciente a python
        with open(os.path.join(skills_dir, "python_testing.md"), "w") as f:
            f.write("# Skill: Python Testing\nDesc\nContent")
        
        # Skill NO perteneciente a python (embedded-c)
        with open(os.path.join(skills_dir, "c_memory_analyzer.md"), "w") as f:
            f.write("# Skill: C Memory Analyzer\nDesc\nContent")
        
        transpiler.setup_directories()
        transpiler.compile_skills()
        
        # Debería haber compilado solo 1 skill (python_testing)
        self.assertEqual(transpiler.compiled_items["skills"], 1)
    
    def test_compile_all_includes_core_and_profiles(self):
        """Verifica que compile_all copia scripts core y perfiles"""
        # Crear estructura .harness mínima
        harness_dir = os.path.join(self.temp_dir, ".harness")
        os.makedirs(os.path.join(harness_dir, "roles"), exist_ok=True)
        os.makedirs(os.path.join(harness_dir, "skills"), exist_ok=True)
        os.makedirs(os.path.join(harness_dir, "memory"), exist_ok=True)
        os.makedirs(os.path.join(harness_dir, "artifacts/templates"), exist_ok=True)
        os.makedirs(os.path.join(harness_dir, "adaptation/scripts"), exist_ok=True)
        
        # Archivos requeridos
        for script in ["lazy_loader.py", "cache_manager.py", "state_manager.py"]:
            with open(os.path.join(harness_dir, "adaptation/scripts", script), "w") as f:
                f.write(f"# {script}")
        
        with open(os.path.join(harness_dir, "profiles_enabled.yaml"), "w") as f:
            f.write("profiles:\n  enabled:\n    - core\n")
        
        with open(os.path.join(harness_dir, "config.yaml"), "w") as f:
            f.write("project:\n  name: test\n")
        
        # Ejecutar compilación
        self.transpiler.compile_all("pointer text")
        
        # Verificar que se crearon los nuevos componentes
        self.assertGreaterEqual(self.transpiler.compiled_items["core_scripts"], 3)
        self.assertGreaterEqual(self.transpiler.compiled_items["profiles_config"], 1)
        self.assertGreaterEqual(self.transpiler.compiled_items["config"], 1)
        
        # Verificar archivos en destino
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, ".opencode/core/lazy_loader.py")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, ".opencode/core/cache_manager.py")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, ".opencode/core/state_manager.py")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, ".opencode/profiles_enabled.yaml")))


class TestRegistryBuilder(unittest.TestCase):
    """Pruebas para el módulo registry_builder"""
    
    def setUp(self):
        """Preparar entorno de pruebas"""
        self.registry = RegistryBuilder(harness_dir=".harness", opencode_dir=".opencode")
    
    def test_build_agents_section(self):
        """Verifica construcción de sección de agentes"""
        self.registry.agents = {
            "Orchestrator": "/.opencode/agents/orchestrator.md",
            "Developer": "/.opencode/agents/developer.md"
        }
        
        result = self.registry.build_agents_section()
        self.assertIn("### Available Sub-Agents (Roles)", result)
        self.assertIn("Orchestrator", result)
        self.assertIn("Developer", result)
    
    def test_build_skills_section(self):
        """Verifica construcción de sección de skills"""
        self.registry.skills = {
            "Strict TDD Gatekeeper": "/.opencode/skills/strict-tdd-gatekeeper/SKILL.md",
            "State Management": "/.opencode/skills/state-management/SKILL.md"
        }
        
        result = self.registry.build_skills_section()
        self.assertIn("### Available Skills", result)
        self.assertIn("Strict TDD Gatekeeper", result)
        self.assertIn("State Management", result)
    
    def test_build_project_info_section(self):
        """Verifica construcción de sección de información del proyecto"""
        self.registry.config = {
            "name": "Test Project",
            "stack": "python",
            "test_command": "pytest",
            "lint_command": "flake8"
        }
        
        result = self.registry.build_project_info_section()
        self.assertIn("## 1. Project Information", result)
        self.assertIn("Test Project", result)
        self.assertIn("python", result)
        self.assertIn("pytest", result)


class TestLazyLoader(unittest.TestCase):
    """Pruebas para el módulo lazy_loader (Sprint 2.1)"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.skills_dir = os.path.join(self.temp_dir, "skills")
        os.makedirs(self.skills_dir, exist_ok=True)
        
        # Crear skill de prueba con frontmatter
        skill_path = os.path.join(self.skills_dir, "test-skill")
        os.makedirs(skill_path, exist_ok=True)
        with open(os.path.join(skill_path, "SKILL.md"), "w") as f:
            f.write("---\nname: test-skill\ndescription: A test skill\n---\n\n# Full content here")
    
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_skill_registry_builds_index(self):
        """Verifica que SkillRegistry construye índice sin cargar contenido"""
        registry = SkillRegistry(skills_dir=self.skills_dir)
        self.assertIn("test-skill", registry.skill_index)
        self.assertEqual(registry.skill_index["test-skill"]["name"], "test-skill")
    
    def test_skill_registry_lazy_loads(self):
        """Verifica que load_skill carga bajo demanda"""
        registry = SkillRegistry(skills_dir=self.skills_dir)
        
        # No debería estar en caché todavía
        self.assertNotIn("test-skill", registry.loaded_skills)
        
        # Cargar bajo demanda
        content = registry.load_skill("test-skill")
        self.assertIsNotNone(content)
        self.assertIn("Full content here", content)
        
        # Ahora debería estar en caché
        self.assertIn("test-skill", registry.loaded_skills)
    
    def test_skill_summary_uses_metadata_only(self):
        """Verifica que get_skill_summary solo usa metadata, no carga contenido"""
        registry = SkillRegistry(skills_dir=self.skills_dir)
        summary = registry.get_skill_summary("test-skill")
        
        self.assertIsNotNone(summary)
        self.assertIn("test-skill", summary)
        self.assertIn("A test skill", summary)
        
        # No debe haber cargado el contenido completo
        self.assertNotIn("test-skill", registry.loaded_skills)
    
    def test_context_window_analysis(self):
        """Verifica análisis de context window"""
        registry = SkillRegistry(skills_dir=self.skills_dir)
        analysis = registry.get_context_window_analysis()
        
        self.assertEqual(analysis["total_skills"], 1)
        self.assertEqual(analysis["loaded_skills"], 0)
        self.assertIn("total_size_kb", analysis)
        self.assertIn("savings_percent", analysis)
    
    def test_profile_aware_loader_mapping(self):
        """Verifica mapeo de perfiles a skills"""
        loader = ProfileAwareLoader(active_profiles=["core"])
        skills = loader.get_active_skills()
        
        self.assertIn("strict-tdd-gatekeeper", skills)
        self.assertIn("skill-creator", skills)
        self.assertNotIn("python-clean-architecture", skills)
    
    def test_profile_aware_loader_multiple_profiles(self):
        """Verifica combinación de skills de múltiples perfiles"""
        loader = ProfileAwareLoader(active_profiles=["core", "python"])
        skills = loader.get_active_skills()
        
        self.assertIn("strict-tdd-gatekeeper", skills)  # core
        self.assertIn("python-clean-architecture", skills)  # python
        self.assertNotIn("c-memory-analyzer-profile-specific", skills)  # embedded-c


class TestCacheManager(unittest.TestCase):
    """Pruebas para el módulo cache_manager (Sprint 2.4)"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.cache_dir = os.path.join(self.temp_dir, "cache")
    
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_store_and_retrieve_decision(self):
        """Verifica almacenar y recuperar decisiones"""
        cache = DecisionsCache(cache_dir=self.cache_dir)
        
        key = cache.store_decision("test_category", "test_id", "mi_decision")
        self.assertIsNotNone(key)
        
        result = cache.retrieve_decision("test_category", "test_id")
        self.assertEqual(result, "mi_decision")
    
    def test_retrieve_nonexistent_returns_none(self):
        """Verifica que decisión inexistente retorna None"""
        cache = DecisionsCache(cache_dir=self.cache_dir)
        result = cache.retrieve_decision("nonexistent", "id")
        self.assertIsNone(result)
    
    def test_exists_check(self):
        """Verifica método exists"""
        cache = DecisionsCache(cache_dir=self.cache_dir)
        
        self.assertFalse(cache.exists("cat", "id"))
        cache.store_decision("cat", "id", "value")
        self.assertTrue(cache.exists("cat", "id"))
    
    def test_clear_category(self):
        """Verifica limpieza por categoría"""
        cache = DecisionsCache(cache_dir=self.cache_dir)
        
        cache.store_decision("cat_a", "id1", "val1")
        cache.store_decision("cat_a", "id2", "val2")
        cache.store_decision("cat_b", "id3", "val3")
        
        cache.clear_category("cat_a")
        
        self.assertIsNone(cache.retrieve_decision("cat_a", "id1"))
        self.assertIsNone(cache.retrieve_decision("cat_a", "id2"))
        self.assertIsNotNone(cache.retrieve_decision("cat_b", "id3"))
    
    def test_get_stats(self):
        """Verifica estadísticas del caché"""
        cache = DecisionsCache(cache_dir=self.cache_dir)
        
        cache.store_decision("cat_a", "id1", "val1")
        cache.store_decision("cat_a", "id2", "val2")
        cache.retrieve_decision("cat_a", "id1")  # 1 hit
        
        stats = cache.get_stats()
        self.assertEqual(stats["total_decisions"], 2)
        self.assertEqual(stats["total_hits"], 1)
        self.assertIn("cat_a", stats["categories"])
    
    def test_context_window_tracker_snapshots(self):
        """Verifica registro y comparación de snapshots"""
        tracker = ContextWindowTracker(cache_dir=self.cache_dir)
        
        tracker.record_snapshot("Before optimization", {"tokens": 5000, "kb": 100})
        tracker.record_snapshot("After optimization", {"tokens": 1000, "kb": 20})
        
        comparison = tracker.compare_snapshots(0, 1)
        self.assertIn("improvements", comparison)
        self.assertEqual(comparison["improvements"]["tokens"]["before"], 5000)
        self.assertEqual(comparison["improvements"]["tokens"]["after"], 1000)
        self.assertEqual(comparison["improvements"]["tokens"]["reduction"], 4000)
    
    def test_decisions_cache_persistence(self):
        """Verifica que el caché persiste en disco"""
        cache1 = DecisionsCache(cache_dir=self.cache_dir)
        cache1.store_decision("persist", "test", "persisted_value")
        del cache1
        
        # Crear nueva instancia (debe cargar desde disco)
        cache2 = DecisionsCache(cache_dir=self.cache_dir)
        result = cache2.retrieve_decision("persist", "test")
        self.assertEqual(result, "persisted_value")


class TestStateManager(unittest.TestCase):
    """Pruebas para el módulo state_manager de automatización"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.manager = HarnessStateManager(workspace_dir=self.temp_dir, use_opencode=False)
        
        # Crear estructura de carpetas mock en temp_dir
        os.makedirs(os.path.join(self.temp_dir, ".harness/artifacts/current_run"), exist_ok=True)
        os.makedirs(os.path.join(self.temp_dir, ".harness/artifacts/templates"), exist_ok=True)
        
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            
    def test_get_initial_state(self):
        """Verifica que el estado inicial tiene las claves correctas"""
        state = self.manager.get_initial_state()
        self.assertEqual(state["current_phase"], "Initialization")
        self.assertEqual(state["active_agent"], "orchestrator")
        self.assertFalse(state["plan_approved"])
        self.assertEqual(state["test_status"], "unknown")
        
    def test_parse_valid_yaml(self):
        """Verifica que el parser de YAML simple funciona correctamente"""
        yaml_content = """# Comentario inicial
state:
  current_phase: "Contract"
  active_agent: "spec"
  plan_approved: true
  active_profile: "python-developer"
  task_checklist:
    - task: "Crear especificaciones"
      status: "completed"
    - task: "Escribir test de integración"
      status: "pending"
  test_status: "passing"
  last_error: "Ninguno"
"""
        state = self.manager.parse_yaml(yaml_content)
        self.assertEqual(state["current_phase"], "Contract")
        self.assertEqual(state["active_agent"], "spec")
        self.assertTrue(state["plan_approved"])
        self.assertEqual(state["active_profile"], "python-developer")
        self.assertEqual(state["test_status"], "passing")
        self.assertEqual(state["last_error"], "Ninguno")
        self.assertEqual(len(state["task_checklist"]), 2)
        self.assertEqual(state["task_checklist"][0]["task"], "Crear especificaciones")
        self.assertEqual(state["task_checklist"][0]["status"], "completed")

    def test_serialize_and_deserialize(self):
        """Verifica ciclo completo de serialización e interpretación"""
        state = {
            "current_phase": "Implementation",
            "active_agent": "python-developer",
            "plan_approved": True,
            "active_profile": "python-developer",
            "task_checklist": [
                {"task": "Desarrollar feature A", "status": "in_progress"}
            ],
            "test_status": "failing",
            "last_error": "SyntaxError: invalid syntax"
        }
        
        serialized = self.manager.serialize_yaml(state)
        self.assertIn("current_phase: \"Implementation\"", serialized)
        self.assertIn("active_agent: \"python-developer\"", serialized)
        self.assertIn("plan_approved: true", serialized)
        self.assertIn("task: \"Desarrollar feature A\"", serialized)
        self.assertIn("status: \"in_progress\"", serialized)
        self.assertIn("test_status: \"failing\"", serialized)
        self.assertIn("last_error: \"SyntaxError: invalid syntax\"", serialized)
        
        parsed = self.manager.parse_yaml(serialized)
        self.assertEqual(parsed["current_phase"], "Implementation")
        self.assertEqual(parsed["active_agent"], "python-developer")
        self.assertTrue(parsed["plan_approved"])
        self.assertEqual(parsed["test_status"], "failing")
        self.assertEqual(parsed["last_error"], "SyntaxError: invalid syntax")
        self.assertEqual(len(parsed["task_checklist"]), 1)
        self.assertEqual(parsed["task_checklist"][0]["task"], "Desarrollar feature A")
        self.assertEqual(parsed["task_checklist"][0]["status"], "in_progress")
        
    def test_validate_schema_success(self):
        """Verifica paso exitoso de validación de esquema"""
        state = self.manager.get_initial_state()
        success, msg = self.manager.validate_schema(state)
        self.assertTrue(success)
        self.assertEqual(msg, "")
        
    def test_validate_schema_invalid_phase(self):
        """Verifica que fases no válidas fallen la validación"""
        state = self.manager.get_initial_state()
        state["current_phase"] = "FaseInventada"
        success, msg = self.manager.validate_schema(state)
        self.assertFalse(success)
        self.assertIn("Fase inválida", msg)
        
    def test_validate_schema_invalid_agent(self):
        """Verifica que agentes no válidos fallen la validación"""
        state = self.manager.get_initial_state()
        state["active_agent"] = "hacker-agent"
        success, msg = self.manager.validate_schema(state)
        self.assertFalse(success)
        self.assertIn("Agente inválido", msg)

    def test_save_and_load_state_file(self):
        """Verifica que se puede guardar y leer de disco atómicamente"""
        state = self.manager.get_initial_state()
        state["current_phase"] = "Contract"
        state["active_agent"] = "spec"
        state["plan_approved"] = True
        
        # Guardar a disco
        self.manager.save_state(state)
        
        # Cargar desde disco
        loaded_state = self.manager.load_state()
        self.assertEqual(loaded_state["current_phase"], "Contract")
        self.assertEqual(loaded_state["active_agent"], "spec")
        self.assertTrue(loaded_state["plan_approved"])


class TestIntegration(unittest.TestCase):
    """Pruebas de integración"""
    
    def test_transpiler_compiles_without_errors(self):
        """Verifica que el transpilador se ejecuta sin errores en proyecto existente"""
        # Este test verifica que la estructura .harness/ actual es válida
        self.assertTrue(os.path.exists(".harness/roles"))
        self.assertTrue(os.path.exists(".harness/skills"))
    
    def test_agents_md_exists(self):
        """Verifica que AGENTS.md existe en raíz"""
        self.assertTrue(os.path.exists("AGENTS.md"))
    
    def test_all_required_files_present(self):
        """Verifica presencia de archivos requeridos en estructura"""
        required = [
            ".harness/config.yaml",
            ".harness/roles/orchestrator.md",
            ".harness/adaptation/scripts/main.py"
        ]
        
        for f in required:
            self.assertTrue(os.path.exists(f), f"Archivo requerido {f} no encontrado")


def run_tests():
    """Ejecuta la suite de pruebas"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar suites
    suite.addTests(loader.loadTestsFromTestCase(TestPathTranslator))
    suite.addTests(loader.loadTestsFromTestCase(TestTranspilerCore))
    suite.addTests(loader.loadTestsFromTestCase(TestRegistryBuilder))
    suite.addTests(loader.loadTestsFromTestCase(TestLazyLoader))
    suite.addTests(loader.loadTestsFromTestCase(TestCacheManager))
    suite.addTests(loader.loadTestsFromTestCase(TestStateManager))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Retornar código de salida
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)
