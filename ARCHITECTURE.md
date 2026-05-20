# Arquitectura del Arnés Multi-Agente: Diseño Basado en Prompts y Transpilación Dinámica

Este documento define la arquitectura y el flujo de trabajo para el **Arnés Multi-Agente**, diseñado de forma modular en torno a **Markdown Prompts** y **Directivas de Contexto**. Este sistema transforma la autonomía de los modelos de IA en un ciclo de desarrollo de software estructurado, predecible y rigurosamente verificado mediante TDD.

---

## 1. Arquitectura de Directorios y Separación de Responsabilidades

El arnés se divide estrictamente en dos partes: la **Fuente de Verdad (Plantillas)** y el **Entorno Transpilado (Destino)**.

```text
/ (Raíz del Proyecto)
├── AGENTS.md                       # Manifiesto y Catálogo Central: Indexa los agentes y habilidades reales del espacio de trabajo
├── adapt_harness.py                # Redireccionador/Launcher ligero de la CLI
├── .gitignore                      # Configuración de exclusiones de control de versiones
│
├── .harness/                       # PLANTILLAS FUENTE (Source of Truth)
│   ├── config.yaml                 # Configuración por defecto (Stack, comandos de pruebas/linters)
│   ├── roles/                      # Prompts maestros para subagentes globales (Orchestrator, Dev, QA, Spec, Docs)
│   ├── skills/                     # Habilidades globales (state_management, tdd_gatekeeper)
│   ├── memory/                     # Archivos de memoria base compartida (ADR y lecciones aprendidas)
│   ├── artifacts/templates/        # Esquemas base de entregables (Planes, tareas, walkthroughs)
│   ├── profiles/                   # Perfiles por stack de desarrollo (embedded-c, python, javascript)
│   └── adaptation/                 # Transpilador y Entorno Virtual
│       ├── .venv/                  # Entorno virtual aislado y auto-gestionado
│       ├── requirements.txt        # Dependencias de Python del transpilador
│       └── scripts/                # Módulos descompuestos del transpilador (.py)
│
└── .opencode/                      # ENTORNO GENERADO (Transpiled Target)
    ├── config.yaml                 # Configuración del perfil de stack activo
    ├── agents/                     # Roles transpilados y traducidos al formato de la herramienta
    ├── skills/                     # Catálogo unificado y único de habilidades transpiladas (Core + Perfil)
    ├── memory/                     # Carpeta de persistencia activa del agente local
    └── artifacts/current_run/      # Máquina de estados (Esquemas YAML de la tarea activa)
```

---

## 2. Los 5 Pilares del Diseño Técnico

### 2.1. Orquestación Rigurosa (Orchestrator Role)
El **Orchestrator** actúa como el *Director del Proyecto* o *Engineering Manager*. Mantiene el contexto de alto nivel leyendo [`AGENTS.md`](file:///Users/hazaeltrejo/Documents/harness_template/AGENTS.md) y los artefactos de la tarea actual.
* **Regla de Oro**: Jamás ejecuta código de producción ni escribe parches directamente.
* **Mecanismo**: Delega la resolución de subtareas instruyendo al modelo a adoptar el rol de otros subagentes especializados (ej. `/.opencode/agents/dev.md`).

### 2.2. Máquina de Estados Guiada por Artefactos
El flujo de desarrollo se modela mediante una máquina de estados finitos basada en documentos y esquemas estructurados:
* `implementation_plan.md`: Requerimientos, criterios de aceptación, diseño técnico y riesgos.
* `task.md`: TODO list dinámico para hacer seguimiento exhaustivo y en tiempo real del progreso.
* `walkthrough.md`: Resumen detallado de cambios realizados y resultados de verificación.

### 2.3. Disciplina en Tiempo de Ejecución (Strict TDD Gatekeeper)
El *Dev Agent* opera bajo el control estricto de la habilidad `strict-tdd-gatekeeper`:
1. **Fase Roja (Red)**: Obliga a escribir una prueba que falle antes de programar la solución. Si la prueba pasa antes de tiempo, el agente debe rechazarla por ser una prueba falsa.
2. **Fase Verde (Green)**: Se programa la funcionalidad mínima necesaria para superar la prueba.
3. **Refactorización (Refactor)**: Optimización del código manteniendo las pruebas en verde.

### 2.4. Persistencia Segmentada (Sistema de Memoria)
La memoria del agente se divide para evitar alucinaciones:
* **Decisiones de Arquitectura (ADR)**: `architecture_decisions.md` (Constraints técnicos estáticos).
* **Memoria Dinámica**: `lessons_learned.md` (El agente de QA registra errores, bugs encontrados y parches aplicados para que futuras sesiones no los repitan).

### 2.5. Catálogo Modular de Habilidades (Skills Registry)
Las capacidades se registran como plugins o protocolos dentro de `/.opencode/skills/`. El Orquestador restringe el uso de estas habilidades al agente adecuado en la fase correcta.

---

## 3. Coexistencia Multi-Perfil y Transpilador Autogestionado

El transpilador descompuesto permite que múltiples perfiles tecnológicos (`embedded-c-developer`, `python-developer`, `javascript-developer`) coexistan de forma concurrente:

1. **Soportes Concurrentes**: El motor compila las plantillas transversales y monta individualmente las habilidades, memorias y configuraciones de cada perfil.
2. **Carga Dinámica en Caliente (Hot-Loading)**: Los agentes inspeccionan el tipo de archivos en el espacio de trabajo en tiempo de ejecución, detectando qué stack usar y parametrizando dinámicamente linters, suites de tests y modos de bypass (ej. `bypass_qa_execution` para compilaciones cruzadas complejas en sistemas embebidos).
3. **Limpieza y Gestión Atómica**: Las opciones de instalación y remoción aíslan perfiles sin dejar rastro de código no deseado, reduciendo drásticamente el uso de tokens y optimizando el contexto de los modelos locales.
