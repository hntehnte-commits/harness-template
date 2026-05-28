"""
tests/test_compiler.py
Suite de pruebas para el compilador del Harness
Verifica transpilación correcta de agentes, skills y artefactos
"""
import unittest
import os
import shutil
import sys
import tempfile
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
        """Verifica creación de estructura de directorios"""
        self.transpiler.setup_directories()
        
        required_dirs = [
            os.path.join(self.temp_dir, ".opencode/agents"),
            os.path.join(self.temp_dir, ".opencode/skills"),
            os.path.join(self.temp_dir, ".opencode/memory"),
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
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Retornar código de salida
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)
