# 📂 .harness - El Motor y Fuente de Verdad del Arnés

Este directorio constituye la **Fuente de Verdad Única (Single Source of Truth)** de todo tu sistema multi-agente. Es el lugar exclusivo donde debes realizar modificaciones a largo plazo en las directivas, roles, habilidades o perfiles de desarrollo. El script transpilador se encargará de compilar estos orígenes en el formato óptimo requerido por cada herramienta de IA.

---

## 🏗️ Estructura del Motor del Arnés

```
.harness/
├── config.yaml                     # Configuración general y stack por defecto del proyecto
├── roles/                          # Prompts maestros de subagentes globales (Orchestrator, Dev, QA, etc.)
├── skills/                         # Habilidades base transversales del arnés (ej. gestión de estados, TDD)
├── memory/                         # Archivos de memoria base compartidos (arquitectura y lecciones aprendidas)
├── artifacts/
│   └── templates/                  # Plantillas para planes de implementación, tareas y walkthroughs
├── profiles/                       # [NUEVO] Sobrecapas específicas por cada stack de desarrollo
│   ├── embedded-c-developer/       #   - Perfil para desarrollo de Sistemas Embebidos en C
│   ├── python-developer/           #   - Perfil para desarrollo en Python
│   └── javascript-developer/       #   - Perfil para desarrollo en JS / TS
└── adaptation/                     # Motor transpilador y entorno de ejecución aislado
    ├── requirements.txt            # Dependencias del motor
    └── scripts/                    # Scripts descompuestos modulares del transpilador
```

---

## 🎛️ Estructura Detallada de Componentes

### 1. `roles/` (Subagentes Core)
Prompts en formato Markdown que definen la personalidad, responsabilidades y restricciones estrictas de cada rol:
* `orchestrator.md`: Lanza subagentes, gestiona prioridades y valida el cumplimiento general de la meta.
* `spec_agent.md`: Valida requerimientos y redacta planes de diseño y especificaciones.
* `dev_agent.md`: Escribe el código fuente cumpliendo de manera estricta los estándares técnicos.
* `qa_agent.md`: Ejecuta linters, suites de pruebas e implementa el bypass opcional de QA.
* `docs_agent.md`: Genera documentación final limpia y walkthroughs de cambios.

### 2. `skills/` (Habilidades Core)
Directivas técnicas modulares que inyectan capacidades especiales:
* `state_management.md`: Reglas del flujo de estados mediante artefactos (`implementation_plan.md`, `task.md`, `walkthrough.md`).
* `tdd_gatekeeper.md`: Lógica rigurosa de desarrollo guiado por pruebas antes de proceder con el código de producción.

### 3. `profiles/` (Perfiles y Capas de Especialización)
Los perfiles permiten que coexistan concurrentemente múltiples stacks tecnológicos. Cada perfil puede extender el arnés core agregando:
* `config.yaml`: Sobreescribe variables del stack activo, comandos de tests (`pytest`, `make test`, `npm test`), linters (`flake8`, `cppcheck`, `eslint`) y configuraciones como `bypass_qa_execution`.
* `skills/`: Añade habilidades dedicadas a ese perfil (ej. `c_memory_analyzer.md` para el desarrollador de C). Estas se indexan automáticamente de manera unificada y única bajo `.opencode/skills/` y se listan en `AGENTS.md`.
* `memory/`: Inyecta directivas y trucos de diseño específicos a ese lenguaje.

---

## 🛠️ Cómo agregar un nuevo Perfil

Añadir soporte para un nuevo stack tecnológico (por ejemplo, `rust-developer`) es sumamente sencillo y limpio:

1. **Crea un directorio de perfil**:
   ```bash
   mkdir -p .harness/profiles/rust-developer/skills
   mkdir -p .harness/profiles/rust-developer/memory
   ```
2. **Crea su archivo `config.yaml`** especificando las particularidades:
   ```yaml
   name: Rust Developer Profile
   stack: rust
   test_command: cargo test
   lint_command: cargo clippy
   bypass_qa_execution: false
   ```
3. **Agrega habilidades específicas** (ej. `rust_borrow_checker.md`) dentro de su carpeta `skills/`.
4. **Re-compila el arnés**:
   ```bash
   python3 adapt_harness.py opencode
   ```
   *El motor de compilación modular automáticamente:*
   * Copiará el perfil de manera no destructiva concurrentemente en `.opencode/profiles/rust-developer/`.
   * Registrará y transpilará su skill específica de Rust bajo `.opencode/skills/rust-borrow-checker/SKILL.md`.
   * Re-sincronizará `AGENTS.md` catalogando y enlazando de forma limpia las nuevas habilidades integradas.
